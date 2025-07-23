import { defineStore } from 'pinia'

export const usePlayerStore = defineStore('player', {
  state: () => ({
    // 当前播放内容
    currentContent: null,
    currentPlaylist: null,
    
    // 播放状态
    isPlaying: false,
    isPaused: false,
    isLoading: false,
    
    // 内容类型 - 关键变更：支持多种内容类型
    contentType: null, // 'audio' | 'video' | 'article'
    
    // 时间控制
    currentTime: 0,
    duration: 0,
    bufferedTime: 0,
    
    // 播放控制
    volume: 1.0,
    playbackRate: 1.0,
    
    // 播放模式
    shuffleMode: false,
    repeatMode: 'none', // none | one | all
    autoplayNext: true,
    
    // 播放列表和队列
    playQueue: [],
    currentIndex: 0,
    playHistory: [],
    
    // 媒体对象
    audioContext: null,
    videoContext: null,
    
    // 视频播放特定状态
    videoFullscreen: false,
    videoMuted: false,
    videoBrightness: 1.0,
    
    // 文章阅读特定状态
    articleScrollPosition: 0,
    articleReadingTime: 0,
    articleTTSEnabled: false,
    
    // 错误和网络状态
    error: null,
    networkType: 'unknown',
    isOnline: true,
    
    // 播放统计
    playStats: {
      totalPlayTime: 0,
      completionRate: 0,
      skipCount: 0
    }
  }),

  getters: {
    // 播放进度百分比
    progressPercent: (state) => {
      if (state.duration === 0) return 0
      return (state.currentTime / state.duration) * 100
    },
    
    // 缓冲进度百分比
    bufferedPercent: (state) => {
      if (state.duration === 0) return 0
      return (state.bufferedTime / state.duration) * 100
    },
    
    // 是否可以播放上一个
    canPlayPrevious: (state) => {
      return state.currentIndex > 0 || 
             state.repeatMode === 'all' || 
             state.playHistory.length > 0
    },
    
    // 是否可以播放下一个
    canPlayNext: (state) => {
      return state.currentIndex < state.playQueue.length - 1 || 
             state.repeatMode === 'all'
    },
    
    // 是否为音频内容
    isAudioContent: (state) => {
      return state.contentType === 'audio'
    },
    
    // 是否为视频内容
    isVideoContent: (state) => {
      return state.contentType === 'video'
    },
    
    // 是否为文章内容
    isArticleContent: (state) => {
      return state.contentType === 'article'
    },
    
    // 当前播放内容的标题
    currentTitle: (state) => {
      return state.currentContent?.title || ''
    },
    
    // 当前播放内容的描述
    currentDescription: (state) => {
      return state.currentContent?.description || state.currentContent?.summary || ''
    },
    
    // 格式化当前时间
    formattedCurrentTime: (state) => {
      return formatTime(state.currentTime)
    },
    
    // 格式化总时长
    formattedDuration: (state) => {
      return formatTime(state.duration)
    }
  },

  actions: {
    // 播放内容 - 核心方法，支持多种内容类型
    async playContent(content, playlist = null, index = 0) {
      try {
        this.isLoading = true
        this.error = null
        
        // 确定内容类型
        const contentType = this.determineContentType(content)
        
        // 如果是新的内容，需要重新初始化
        if (!this.currentContent || 
            this.currentContent.id !== content.id || 
            this.contentType !== contentType) {
          await this.initializeContent(content, contentType)
        }
        
        // 设置播放列表
        if (playlist) {
          this.currentPlaylist = playlist
          this.playQueue = playlist.contents || [content]
          this.currentIndex = index
        } else {
          this.playQueue = [content]
          this.currentIndex = 0
        }
        
        this.currentContent = content
        this.contentType = contentType
        
        // 根据内容类型开始播放
        await this.startPlayback()
        
        // 记录播放历史
        this.addToHistory(content)
        
        // 上报播放数据
        this.reportPlayStart(content)
        
      } catch (error) {
        this.handlePlayError(error)
      } finally {
        this.isLoading = false
      }
    },

    // 确定内容类型
    determineContentType(content) {
      if (content.content_type) {
        return content.content_type
      }
      
      if (content.audio_url) {
        return 'audio'
      } else if (content.video_url) {
        return 'video'
      } else if (content.article_content || content.text_content) {
        return 'article'
      }
      
      // 根据文件扩展名判断
      const url = content.media_url || content.file_url || ''
      if (/\.(mp3|wav|aac|flac|ogg)$/i.test(url)) {
        return 'audio'
      } else if (/\.(mp4|avi|mov|wmv|flv|webm)$/i.test(url)) {
        return 'video'
      }
      
      return 'article' // 默认为文章
    },

    // 初始化内容
    async initializeContent(content, contentType) {
      // 清理之前的媒体对象
      this.destroyCurrentMedia()
      
      switch (contentType) {
        case 'audio':
          await this.initializeAudio(content)
          break
        case 'video':
          await this.initializeVideo(content)
          break
        case 'article':
          await this.initializeArticle(content)
          break
        default:
          throw new Error('不支持的内容类型')
      }
    },

    // 初始化音频
    async initializeAudio(content) {
      this.audioContext = uni.createInnerAudioContext()
      
      this.audioContext.src = content.audio_url || content.media_url
      this.audioContext.volume = this.volume
      this.audioContext.playbackRate = this.playbackRate
      
      this.bindAudioEvents()
      
      return new Promise((resolve, reject) => {
        this.audioContext.onCanplay(() => {
          this.duration = this.audioContext.duration || content.duration || 0
          resolve()
        })
        
        this.audioContext.onError((error) => {
          reject(error)
        })
      })
    },

    // 初始化视频
    async initializeVideo(content) {
      // 视频播放通过video组件处理，这里主要设置状态
      this.duration = content.duration || 0
      this.videoMuted = false
      this.videoFullscreen = false
      
      // 触发视频组件初始化事件
      uni.$emit('video-initialize', {
        src: content.video_url || content.media_url,
        poster: content.cover_url || content.thumbnail_url
      })
      
      return Promise.resolve()
    },

    // 初始化文章
    async initializeArticle(content) {
      this.articleScrollPosition = 0
      this.articleReadingTime = 0
      
      // 估算阅读时长（基于字数，平均阅读速度）
      const wordCount = (content.article_content || content.text_content || '').length
      this.duration = Math.ceil(wordCount / 250 * 60) // 假设每分钟250字
      
      // 如果启用了TTS，初始化语音合成
      if (this.articleTTSEnabled) {
        await this.initializeTTS(content)
      }
      
      return Promise.resolve()
    },

    // 绑定音频事件
    bindAudioEvents() {
      if (!this.audioContext) return
      
      this.audioContext.onPlay(() => {
        this.isPlaying = true
        this.isPaused = false
      })
      
      this.audioContext.onPause(() => {
        this.isPlaying = false
        this.isPaused = true
      })
      
      this.audioContext.onStop(() => {
        this.isPlaying = false
        this.isPaused = false
      })
      
      this.audioContext.onTimeUpdate(() => {
        this.currentTime = this.audioContext.currentTime
        this.duration = this.audioContext.duration
        this.updatePlayStats()
      })
      
      this.audioContext.onEnded(() => {
        this.handleContentEnded()
      })
      
      this.audioContext.onError((error) => {
        this.handlePlayError(error)
      })
      
      this.audioContext.onWaiting(() => {
        this.isLoading = true
      })
      
      this.audioContext.onCanplay(() => {
        this.isLoading = false
      })
    },

    // 开始播放
    async startPlayback() {
      switch (this.contentType) {
        case 'audio':
          if (this.audioContext) {
            await this.audioContext.play()
          }
          break
        case 'video':
          uni.$emit('video-play')
          this.isPlaying = true
          break
        case 'article':
          this.isPlaying = true
          this.startArticleReading()
          break
      }
    },

    // 开始文章阅读
    startArticleReading() {
      // 开始计时阅读时间
      this.articleReadingTimer = setInterval(() => {
        if (this.isPlaying) {
          this.articleReadingTime += 1
          this.currentTime = this.articleReadingTime
          this.updatePlayStats()
        }
      }, 1000)
      
      // 如果启用TTS，开始语音播放
      if (this.articleTTSEnabled && this.audioContext) {
        this.audioContext.play()
      }
    },

    // 播放/暂停控制
    async togglePlay() {
      try {
        if (this.isPlaying) {
          await this.pause()
        } else {
          await this.play()
        }
      } catch (error) {
        this.handlePlayError(error)
      }
    },

    // 播放
    async play() {
      switch (this.contentType) {
        case 'audio':
          if (this.audioContext) {
            await this.audioContext.play()
          }
          break
        case 'video':
          uni.$emit('video-play')
          this.isPlaying = true
          break
        case 'article':
          this.isPlaying = true
          if (this.articleTTSEnabled && this.audioContext) {
            await this.audioContext.play()
          }
          break
      }
    },

    // 暂停
    pause() {
      switch (this.contentType) {
        case 'audio':
          if (this.audioContext) {
            this.audioContext.pause()
          }
          break
        case 'video':
          uni.$emit('video-pause')
          this.isPlaying = false
          this.isPaused = true
          break
        case 'article':
          this.isPlaying = false
          this.isPaused = true
          if (this.articleTTSEnabled && this.audioContext) {
            this.audioContext.pause()
          }
          break
      }
    },

    // 停止
    stop() {
      switch (this.contentType) {
        case 'audio':
          if (this.audioContext) {
            this.audioContext.stop()
          }
          break
        case 'video':
          uni.$emit('video-stop')
          break
        case 'article':
          if (this.articleReadingTimer) {
            clearInterval(this.articleReadingTimer)
            this.articleReadingTimer = null
          }
          if (this.articleTTSEnabled && this.audioContext) {
            this.audioContext.stop()
          }
          break
      }
      
      this.isPlaying = false
      this.isPaused = false
      this.currentTime = 0
    },

    // 跳转到指定时间/位置
    seek(position) {
      switch (this.contentType) {
        case 'audio':
          if (this.audioContext && position >= 0 && position <= this.duration) {
            this.audioContext.seek(position)
            this.currentTime = position
          }
          break
        case 'video':
          uni.$emit('video-seek', position)
          this.currentTime = position
          break
        case 'article':
          // 文章跳转到特定段落或百分比位置
          this.articleScrollPosition = position
          this.currentTime = position
          uni.$emit('article-scroll', position)
          break
      }
    },

    // 播放下一个内容
    async playNext() {
      let nextIndex = this.getNextContentIndex()
      
      if (nextIndex !== -1) {
        const nextContent = this.playQueue[nextIndex]
        await this.playContent(nextContent, this.currentPlaylist, nextIndex)
      }
    },

    // 播放上一个内容
    async playPrevious() {
      let prevIndex = this.getPreviousContentIndex()
      
      if (prevIndex !== -1) {
        const prevContent = this.playQueue[prevIndex]
        await this.playContent(prevContent, this.currentPlaylist, prevIndex)
      }
    },

    // 获取下一个内容索引
    getNextContentIndex() {
      if (this.shuffleMode) {
        const availableIndexes = this.playQueue
          .map((_, index) => index)
          .filter(index => index !== this.currentIndex)
        return availableIndexes[Math.floor(Math.random() * availableIndexes.length)]
      } else {
        if (this.currentIndex < this.playQueue.length - 1) {
          return this.currentIndex + 1
        } else if (this.repeatMode === 'all') {
          return 0
        }
      }
      return -1
    },

    // 获取上一个内容索引
    getPreviousContentIndex() {
      if (this.currentIndex > 0) {
        return this.currentIndex - 1
      } else if (this.repeatMode === 'all') {
        return this.playQueue.length - 1
      }
      return -1
    },

    // 处理内容播放结束
    async handleContentEnded() {
      this.reportPlayComplete()
      
      if (this.repeatMode === 'one') {
        this.seek(0)
        await this.play()
      } else if (this.autoplayNext) {
        await this.playNext()
      }
    },

    // 切换TTS模式（仅文章）
    async toggleTTS() {
      if (this.contentType !== 'article') return
      
      this.articleTTSEnabled = !this.articleTTSEnabled
      
      if (this.articleTTSEnabled) {
        await this.initializeTTS(this.currentContent)
      } else {
        if (this.audioContext) {
          this.audioContext.destroy()
          this.audioContext = null
        }
      }
    },

    // 初始化TTS
    async initializeTTS(content) {
      try {
        const ttsManager = await import('@/utils/tts.js')
        const taskId = await ttsManager.synthesizeText(
          content.article_content || content.text_content,
          {
            voice: 'standard_female',
            speed: this.playbackRate
          }
        )
        
        // 等待TTS完成
        const result = await this.waitForTTS(taskId)
        if (result.audioUrl) {
          this.audioContext = uni.createInnerAudioContext()
          this.audioContext.src = result.audioUrl
          this.bindAudioEvents()
        }
      } catch (error) {
        console.error('TTS初始化失败:', error)
      }
    },

    // 等待TTS完成
    waitForTTS(taskId) {
      return new Promise((resolve, reject) => {
        const checkStatus = () => {
          const status = ttsManager.getTaskStatus(taskId)
          if (status.status === 'completed') {
            resolve(status)
          } else if (status.status === 'failed') {
            reject(new Error(status.error))
          } else {
            setTimeout(checkStatus, 1000)
          }
        }
        checkStatus()
      })
    },

    // 更新播放统计
    updatePlayStats() {
      if (this.currentContent && this.isPlaying) {
        this.playStats.totalPlayTime += 1
        if (this.duration > 0) {
          this.playStats.completionRate = (this.currentTime / this.duration) * 100
        }
      }
    },

    // 添加到播放历史
    addToHistory(content) {
      const historyItem = {
        ...content,
        playedAt: new Date().toISOString(),
        contentType: this.contentType
      }
      
      const existingIndex = this.playHistory.findIndex(item => 
        item.id === content.id && item.contentType === this.contentType
      )
      
      if (existingIndex !== -1) {
        this.playHistory.splice(existingIndex, 1)
      }
      
      this.playHistory.unshift(historyItem)
      
      if (this.playHistory.length > 1000) {
        this.playHistory = this.playHistory.slice(0, 1000)
      }
      
      uni.setStorageSync('play_history', this.playHistory)
    },

    // 销毁当前媒体
    destroyCurrentMedia() {
      if (this.audioContext) {
        this.audioContext.destroy()
        this.audioContext = null
      }
      
      if (this.articleReadingTimer) {
        clearInterval(this.articleReadingTimer)
        this.articleReadingTimer = null
      }
      
      uni.$emit('video-destroy')
    },

    // 处理播放错误
    handlePlayError(error) {
      console.error('播放错误:', error)
      this.error = error.message || '播放失败'
      this.isPlaying = false
      this.isLoading = false
      
      uni.showToast({
        title: '播放失败',
        icon: 'error'
      })
    },

    // 上报播放开始
    async reportPlayStart(content) {
      try {
        await api.player.recordPlay({
          content_id: content.id,
          content_type: this.contentType,
          action: 'start',
          timestamp: new Date().toISOString(),
          device_type: this.getDeviceType()
        })
      } catch (error) {
        console.error('上报播放开始失败:', error)
      }
    },

    // 上报播放完成
    async reportPlayComplete() {
      if (this.currentContent) {
        try {
          await api.player.recordPlay({
            content_id: this.currentContent.id,
            content_type: this.contentType,
            action: 'complete',
            play_duration: this.currentTime,
            completion_rate: this.playStats.completionRate,
            timestamp: new Date().toISOString()
          })
        } catch (error) {
          console.error('上报播放完成失败:', error)
        }
      }
    },

    // 获取设备类型
    getDeviceType() {
      const systemInfo = uni.getSystemInfoSync()
      return systemInfo.platform || 'unknown'
    },

    // 销毁播放器
    destroy() {
      this.destroyCurrentMedia()
      this.currentContent = null
      this.isPlaying = false
      this.currentTime = 0
      this.duration = 0
      this.playStats = {
        totalPlayTime: 0,
        completionRate: 0,
        skipCount: 0
      }
    }
  }
})

// 时间格式化工具函数
function formatTime(seconds) {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}