/**
 * 文本转语音 (TTS) 工具
 * 支持多种语音引擎和配置选项，适用于UniApp多端环境
 */

// TTS 引擎类型
export const TTS_ENGINES = {
  SYSTEM: 'system', // 系统内置TTS
  CLOUD: 'cloud',   // 云端TTS
  WEB: 'web'        // Web Speech API
}

// TTS 状态
export const TTS_STATES = {
  IDLE: 'idle',
  LOADING: 'loading',
  PLAYING: 'playing',
  PAUSED: 'paused',
  ERROR: 'error'
}

/**
 * TTS 播放器类
 */
export class TTSPlayer {
  constructor(options = {}) {
    this.options = {
      engine: TTS_ENGINES.WEB,
      voice: 'xiaoyun',
      speed: 1.0,
      volume: 0.8,
      pitch: 1.0,
      language: 'zh-CN',
      enableChunking: true,
      chunkSize: 200,
      autoPlay: false,
      ...options
    }
    
    this.state = TTS_STATES.IDLE
    this.currentTime = 0
    this.duration = 0
    this.chunks = []
    this.currentChunkIndex = 0
    this.audioContext = null
    this.speechUtterance = null
    this.callbacks = {}
    this.progressTimer = null
    
    this.init()
  }

  /**
   * 初始化 TTS 播放器
   */
  async init() {
    try {
      // 检查 TTS 支持
      if (!this.isTTSSupported()) {
        throw new Error('当前设备不支持TTS功能')
      }
      
      // 根据环境选择引擎
      this.selectEngine()
      
      // 初始化对应引擎
      await this.initEngine()
      
      this.emit('ready')
    } catch (error) {
      this.handleError(error)
    }
  }

  /**
   * 检查 TTS 支持
   */
  isTTSSupported() {
    // #ifdef H5
    return typeof window !== 'undefined' && window.speechSynthesis
    // #endif
    
    // #ifdef APP-PLUS || MP
    return typeof uni !== 'undefined' && uni.createInnerAudioContext
    // #endif
    
    return false
  }

  /**
   * 选择合适的引擎
   */
  selectEngine() {
    // #ifdef H5
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      this.options.engine = TTS_ENGINES.WEB
    }
    // #endif
    
    // #ifdef APP-PLUS || MP
    this.options.engine = TTS_ENGINES.SYSTEM
    // #endif
  }

  /**
   * 初始化引擎
   */
  async initEngine() {
    switch (this.options.engine) {
      case TTS_ENGINES.WEB:
        await this.initWebEngine()
        break
      case TTS_ENGINES.SYSTEM:
        await this.initSystemEngine()
        break
      case TTS_ENGINES.CLOUD:
        await this.initCloudEngine()
        break
    }
  }

  /**
   * 初始化Web引擎
   */
  async initWebEngine() {
    // #ifdef H5
    if (window.speechSynthesis) {
      // 等待语音列表加载
      if (speechSynthesis.getVoices().length === 0) {
        await new Promise(resolve => {
          speechSynthesis.addEventListener('voiceschanged', resolve, { once: true })
        })
      }
    }
    // #endif
  }

  /**
   * 初始化系统引擎
   */
  async initSystemEngine() {
    // #ifdef APP-PLUS || MP
    if (this.audioContext) {
      this.audioContext.destroy()
    }
    
    this.audioContext = uni.createInnerAudioContext()
    this.setupAudioEvents()
    // #endif
  }

  /**
   * 初始化云端引擎
   */
  async initCloudEngine() {
    // 初始化云端TTS配置
    await this.initSystemEngine() // 作为备选方案
  }

  /**
   * 设置音频事件监听
   */
  setupAudioEvents() {
    if (!this.audioContext) return
    
    this.audioContext.onPlay(() => {
      this.state = TTS_STATES.PLAYING
      this.startProgressTimer()
      this.emit('play')
    })
    
    this.audioContext.onPause(() => {
      this.state = TTS_STATES.PAUSED
      this.stopProgressTimer()
      this.emit('pause')
    })
    
    this.audioContext.onStop(() => {
      this.state = TTS_STATES.IDLE
      this.stopProgressTimer()
      this.emit('stop')
    })
    
    this.audioContext.onEnded(() => {
      this.handleChunkEnd()
    })
    
    this.audioContext.onError((error) => {
      this.handleError(error)
    })
  }

  /**
   * 设置文本内容
   */
  async setText(text) {
    try {
      if (!text || typeof text !== 'string') {
        throw new Error('文本内容无效')
      }
      
      this.state = TTS_STATES.LOADING
      this.emit('loading')
      
      // 清理文本
      const cleanText = TTSUtils.cleanTextForTTS(text)
      
      // 处理文本分块
      this.chunks = this.options.enableChunking ? 
        this.splitTextToChunks(cleanText) : [cleanText]
      
      // 预处理音频
      await this.preprocessAudio()
      
      this.duration = TTSUtils.estimatePlaybackDuration(cleanText, this.options.speed)
      this.emit('textReady', { chunks: this.chunks.length, duration: this.duration })
      
    } catch (error) {
      this.handleError(error)
    }
  }

  /**
   * 将文本分割成块
   */
  splitTextToChunks(text) {
    const chunks = []
    const sentences = text.split(/[。！？.!?]/g).filter(s => s.trim())
    
    let currentChunk = ''
    
    for (const sentence of sentences) {
      if (currentChunk.length + sentence.length > this.options.chunkSize) {
        if (currentChunk) {
          chunks.push(currentChunk.trim())
          currentChunk = ''
        }
      }
      currentChunk += sentence + '。'
    }
    
    if (currentChunk.trim()) {
      chunks.push(currentChunk.trim())
    }
    
    return chunks.length > 0 ? chunks : [text]
  }

  /**
   * 预处理音频
   */
  async preprocessAudio() {
    switch (this.options.engine) {
      case TTS_ENGINES.CLOUD:
        await this.preprocessCloudTTS()
        break
      case TTS_ENGINES.WEB:
      case TTS_ENGINES.SYSTEM:
      default:
        // Web和系统TTS无需预处理
        this.chunks = this.chunks.map((chunk, index) => ({
          text: chunk,
          audioUrl: null,
          index: index
        }))
    }
  }

  /**
   * 预处理云端 TTS
   */
  async preprocessCloudTTS() {
    for (let i = 0; i < this.chunks.length; i++) {
      const chunk = this.chunks[i]
      try {
        const audioUrl = await this.generateCloudAudio(chunk, i)
        this.chunks[i] = {
          text: chunk,
          audioUrl: audioUrl,
          index: i
        }
      } catch (error) {
        console.warn(`云端TTS生成失败，块 ${i}:`, error)
        this.chunks[i] = {
          text: chunk,
          audioUrl: null,
          index: i
        }
      }
    }
  }

  /**
   * 生成云端音频
   */
  async generateCloudAudio(text, index) {
    try {
      const response = await uni.request({
        url: 'https://api.yangmie.com/v1/tts/generate',
        method: 'POST',
        data: {
          text: text,
          voice: this.options.voice,
          speed: this.options.speed,
          volume: this.options.volume,
          language: this.options.language
        },
        header: {
          'Content-Type': 'application/json'
        }
      })
      
      if (response.statusCode === 200 && response.data.success) {
        return response.data.data.audioUrl
      } else {
        throw new Error(response.data.message || 'TTS生成失败')
      }
    } catch (error) {
      throw new Error(`云端TTS生成失败: ${error.message}`)
    }
  }

  /**
   * 播放 TTS
   */
  async play() {
    try {
      if (this.state === TTS_STATES.PLAYING) return
      
      if (this.chunks.length === 0) {
        throw new Error('没有可播放的内容')
      }
      
      if (this.state === TTS_STATES.PAUSED) {
        // 恢复播放
        await this.resumePlay()
        return
      }
      
      // 开始播放第一个块
      await this.playChunk(this.currentChunkIndex)
      
    } catch (error) {
      this.handleError(error)
    }
  }

  /**
   * 恢复播放
   */
  async resumePlay() {
    switch (this.options.engine) {
      case TTS_ENGINES.WEB:
        // #ifdef H5
        if (window.speechSynthesis.paused) {
          window.speechSynthesis.resume()
        }
        // #endif
        break
      case TTS_ENGINES.SYSTEM:
        this.audioContext?.play()
        break
    }
  }

  /**
   * 播放指定块
   */
  async playChunk(chunkIndex) {
    if (chunkIndex < 0 || chunkIndex >= this.chunks.length) return
    
    const chunk = this.chunks[chunkIndex]
    this.currentChunkIndex = chunkIndex
    
    try {
      switch (this.options.engine) {
        case TTS_ENGINES.WEB:
          await this.playWebTTS(chunk.text)
          break
        case TTS_ENGINES.CLOUD:
          if (chunk.audioUrl) {
            await this.playAudioUrl(chunk.audioUrl)
          } else {
            await this.playWebTTS(chunk.text)
          }
          break
        case TTS_ENGINES.SYSTEM:
        default:
          await this.playSystemTTS(chunk.text)
          break
      }
    } catch (error) {
      console.error(`播放块 ${chunkIndex} 失败:`, error)
      // 尝试播放下一块
      this.playNext()
    }
  }

  /**
   * 播放Web TTS
   */
  async playWebTTS(text) {
    // #ifdef H5
    return new Promise((resolve, reject) => {
      try {
        if (this.speechUtterance) {
          window.speechSynthesis.cancel()
        }
        
        this.speechUtterance = new SpeechSynthesisUtterance(text)
        this.speechUtterance.lang = this.options.language
        this.speechUtterance.rate = this.options.speed
        this.speechUtterance.volume = this.options.volume
        this.speechUtterance.pitch = this.options.pitch
        
        // 设置语音
        const voices = speechSynthesis.getVoices()
        const selectedVoice = voices.find(voice => 
          voice.lang.includes(this.options.language.split('-')[0])
        )
        if (selectedVoice) {
          this.speechUtterance.voice = selectedVoice
        }
        
        this.speechUtterance.onstart = () => {
          this.state = TTS_STATES.PLAYING
          this.startProgressTimer()
          this.emit('play')
        }
        
        this.speechUtterance.onend = () => {
          this.stopProgressTimer()
          this.handleChunkEnd()
          resolve()
        }
        
        this.speechUtterance.onerror = (event) => {
          this.stopProgressTimer()
          reject(new Error(`Web TTS错误: ${event.error}`))
        }
        
        window.speechSynthesis.speak(this.speechUtterance)
        
      } catch (error) {
        reject(new Error(`Web TTS播放失败: ${error.message}`))
      }
    })
    // #endif
    
    // #ifndef H5
    throw new Error('Web TTS仅在H5环境下支持')
    // #endif
  }

  /**
   * 播放音频 URL
   */
  async playAudioUrl(audioUrl) {
    if (!this.audioContext) {
      await this.initSystemEngine()
    }
    
    this.audioContext.src = audioUrl
    this.audioContext.volume = this.options.volume
    this.audioContext.play()
  }

  /**
   * 播放系统 TTS
   */
  async playSystemTTS(text) {
    // 这里可以集成具体的系统TTS API
    // 目前使用模拟实现
    return new Promise((resolve) => {
      this.state = TTS_STATES.PLAYING
      this.startProgressTimer()
      this.emit('play')
      
      // 模拟播放时长
      const duration = TTSUtils.estimatePlaybackDuration(text, this.options.speed) * 1000
      
      setTimeout(() => {
        this.stopProgressTimer()
        this.handleChunkEnd()
        resolve()
      }, duration)
    })
  }

  /**
   * 暂停播放
   */
  pause() {
    if (this.state === TTS_STATES.PLAYING) {
      switch (this.options.engine) {
        case TTS_ENGINES.WEB:
          // #ifdef H5
          if (window.speechSynthesis.speaking) {
            window.speechSynthesis.pause()
          }
          // #endif
          break
        case TTS_ENGINES.SYSTEM:
          this.audioContext?.pause()
          break
      }
      
      this.state = TTS_STATES.PAUSED
      this.stopProgressTimer()
      this.emit('pause')
    }
  }

  /**
   * 停止播放
   */
  stop() {
    switch (this.options.engine) {
      case TTS_ENGINES.WEB:
        // #ifdef H5
        if (window.speechSynthesis.speaking) {
          window.speechSynthesis.cancel()
        }
        // #endif
        break
      case TTS_ENGINES.SYSTEM:
        this.audioContext?.stop()
        break
    }
    
    this.currentTime = 0
    this.currentChunkIndex = 0
    this.state = TTS_STATES.IDLE
    this.stopProgressTimer()
    this.emit('stop')
  }

  /**
   * 跳转到指定时间
   */
  seek(time) {
    const targetTime = Math.max(0, Math.min(time, this.duration))
    this.currentTime = targetTime
    this.emit('seek', targetTime)
    
    // Web TTS 不支持精确跳转，重新开始播放
    if (this.state === TTS_STATES.PLAYING) {
      this.stop()
      setTimeout(() => this.play(), 100)
    }
  }

  /**
   * 播放下一块
   */
  playNext() {
    if (this.canNext()) {
      this.playChunk(this.currentChunkIndex + 1)
    } else {
      this.emit('end')
      this.stop()
    }
  }

  /**
   * 播放上一块
   */
  playPrevious() {
    if (this.canPrevious()) {
      this.playChunk(this.currentChunkIndex - 1)
    }
  }

  /**
   * 检查是否可以播放下一块
   */
  canNext() {
    return this.currentChunkIndex < this.chunks.length - 1
  }

  /**
   * 检查是否可以播放上一块
   */
  canPrevious() {
    return this.currentChunkIndex > 0
  }

  /**
   * 设置语音
   */
  setVoice(voice) {
    this.options.voice = voice
    this.emit('voiceChange', voice)
  }

  /**
   * 设置语速
   */
  setSpeed(speed) {
    this.options.speed = Math.max(0.5, Math.min(2.0, speed))
    this.emit('speedChange', this.options.speed)
  }

  /**
   * 设置音量
   */
  setVolume(volume) {
    this.options.volume = Math.max(0, Math.min(1, volume))
    if (this.audioContext) {
      this.audioContext.volume = this.options.volume
    }
    this.emit('volumeChange', this.options.volume)
  }

  /**
   * 开始进度定时器
   */
  startProgressTimer() {
    this.stopProgressTimer()
    this.progressTimer = setInterval(() => {
      this.currentTime += 0.1
      this.emit('timeUpdate', this.currentTime, this.duration)
    }, 100)
  }

  /**
   * 停止进度定时器
   */
  stopProgressTimer() {
    if (this.progressTimer) {
      clearInterval(this.progressTimer)
      this.progressTimer = null
    }
  }

  /**
   * 处理块播放结束
   */
  handleChunkEnd() {
    if (this.canNext()) {
      this.playNext()
    } else {
      this.emit('end')
      this.stop()
    }
  }

  /**
   * 处理错误
   */
  handleError(error) {
    this.state = TTS_STATES.ERROR
    this.stopProgressTimer()
    this.emit('error', error)
    console.error('TTS Error:', error)
  }

  /**
   * 事件监听
   */
  on(event, callback) {
    if (!this.callbacks[event]) {
      this.callbacks[event] = []
    }
    this.callbacks[event].push(callback)
  }

  /**
   * 移除事件监听
   */
  off(event, callback) {
    if (this.callbacks[event]) {
      const index = this.callbacks[event].indexOf(callback)
      if (index > -1) {
        this.callbacks[event].splice(index, 1)
      }
    }
  }

  /**
   * 触发事件
   */
  emit(event, ...args) {
    if (this.callbacks[event]) {
      this.callbacks[event].forEach(callback => {
        try {
          callback(...args)
        } catch (error) {
          console.error('TTS callback error:', error)
        }
      })
    }
  }

  /**
   * 销毁播放器
   */
  destroy() {
    this.stop()
    
    if (this.audioContext) {
      this.audioContext.destroy()
      this.audioContext = null
    }
    
    this.callbacks = {}
    this.chunks = []
    this.state = TTS_STATES.IDLE
    this.stopProgressTimer()
  }
}

/**
 * 创建 TTS 播放器实例
 * @param {Object} options - 配置选项
 * @returns {Promise<TTSPlayer>} TTS 播放器实例
 */
export const createTTSPlayer = async (options = {}) => {
  const player = new TTSPlayer(options)
  
  // 等待初始化完成
  await new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      reject(new Error('TTS播放器初始化超时'))
    }, 5000)
    
    player.on('ready', () => {
      clearTimeout(timeout)
      resolve()
    })
    
    player.on('error', (error) => {
      clearTimeout(timeout)
      reject(error)
    })
  })
  
  // 设置文本内容
  if (options.text) {
    await player.setText(options.text)
  }
  
  return player
}

/**
 * TTS 工具函数
 */
export const TTSUtils = {
  /**
   * 检查 TTS 支持
   */
  isSupported() {
    // #ifdef H5
    return typeof window !== 'undefined' && window.speechSynthesis
    // #endif
    
    // #ifdef APP-PLUS || MP
    return typeof uni !== 'undefined' && uni.createInnerAudioContext
    // #endif
    
    return false
  },

  /**
   * 获取可用语音列表
   */
  async getAvailableVoices() {
    const voices = [
      { id: 'xiaoyun', name: '小云（女声）', gender: 'female', language: 'zh-CN' },
      { id: 'xiaogang', name: '小刚（男声）', gender: 'male', language: 'zh-CN' },
      { id: 'xiaomei', name: '小美（女声）', gender: 'female', language: 'zh-CN' },
      { id: 'xiaoli', name: '小李（男声）', gender: 'male', language: 'zh-CN' }
    ]
    
    // #ifdef H5
    if (window.speechSynthesis) {
      const webVoices = speechSynthesis.getVoices()
      const chineseVoices = webVoices.filter(voice => 
        voice.lang.includes('zh') || voice.lang.includes('cmn')
      )
      
      voices.push(...chineseVoices.map(voice => ({
        id: voice.name,
        name: voice.name,
        gender: voice.name.toLowerCase().includes('female') ? 'female' : 'male',
        language: voice.lang,
        isSystem: true
      })))
    }
    // #endif
    
    return voices
  },

  /**
   * 估算文本播放时长
   */
  estimatePlaybackDuration(text, speed = 1.0) {
    if (!text) return 0
    
    // 中文：约3字符/秒，英文：约5字符/秒
    const isEnglish = /^[a-zA-Z\s,.!?]+$/.test(text)
    const charsPerSecond = (isEnglish ? 5 : 3) * speed
    
    return Math.ceil(text.length / charsPerSecond)
  },

  /**
   * 清理文本内容
   */
  cleanTextForTTS(text) {
    if (!text) return ''
    
    return text
      .replace(/<[^>]*>/g, '') // 移除 HTML 标签
      .replace(/&nbsp;/g, ' ') // 替换 HTML 实体
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&amp;/g, '&')
      .replace(/&quot;/g, '"')
      .replace(/&#x27;/g, "'")
      .replace(/\s+/g, ' ') // 合并多个空格
      .replace(/\n+/g, '。') // 换行转句号
      .replace(/[^\u4e00-\u9fa5a-zA-Z0-9.,!?;:()""''【】《》，。！？；：（）]/g, '') // 保留常用字符
      .trim()
  },

  /**
   * 验证 TTS 配置
   */
  validateConfig(config) {
    const errors = []
    
    if (config.speed && (config.speed < 0.5 || config.speed > 2.0)) {
      errors.push('语速必须在 0.5 到 2.0 之间')
    }
    
    if (config.volume && (config.volume < 0 || config.volume > 1)) {
      errors.push('音量必须在 0 到 1 之间')
    }
    
    if (config.pitch && (config.pitch < 0.5 || config.pitch > 2.0)) {
      errors.push('音调必须在 0.5 到 2.0 之间')
    }
    
    return {
      isValid: errors.length === 0,
      errors
    }
  }
}

// 兼容旧API
export function speak(text, options = {}) {
  if (!TTSUtils.isSupported()) {
    console.warn('当前环境不支持TTS')
    return
  }
  
  // #ifdef H5
  if (typeof window !== 'undefined' && window.speechSynthesis) {
    const utter = new window.SpeechSynthesisUtterance(text)
    utter.lang = options.lang || 'zh-CN'
    utter.rate = options.rate || 1
    utter.pitch = options.pitch || 1
    utter.volume = options.volume || 1
    window.speechSynthesis.speak(utter)
  }
  // #endif
}

export function stop() {
  // #ifdef H5
  if (typeof window !== 'undefined' && window.speechSynthesis) {
    window.speechSynthesis.cancel()
  }
  // #endif
}

// 默认导出
export default {
  TTSPlayer,
  createTTSPlayer,
  TTSUtils,
  TTS_ENGINES,
  TTS_STATES,
  speak,
  stop
}