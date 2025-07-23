<template>
  <view class="audio-player">
    <!-- 音频可视化 -->
    <view class="audio-visualizer" v-if="isPlaying">
      <view class="wave-container">
        <view 
          v-for="i in 20" 
          :key="i" 
          class="wave-bar"
          :style="{ 
            animationDelay: `${i * 0.1}s`,
            height: `${Math.random() * 60 + 20}rpx`
          }"
        ></view>
      </view>
    </view>

    <!-- 专辑封面 -->
    <view class="cover-section">
      <view class="cover-container" :class="{ playing: isPlaying, loading: isLoading }">
        <image 
          :src="content.cover_url || content.thumbnail_url" 
          class="cover-image"
          mode="aspectFill"
          @error="handleImageError"
        />
        
        <!-- 播放状态指示器 -->
        <view class="play-indicator" v-if="isPlaying">
          <view class="pulse-ring"></view>
          <fui-icon name="volume-up" color="#4CD964" size="24" />
        </view>
        
        <!-- 暂停状态覆盖层 -->
        <view class="pause-overlay" v-else-if="currentTime > 0">
          <fui-icon name="play" color="#fff" size="32" />
        </view>
      </view>
    </view>

    <!-- 音频信息 -->
    <view class="audio-info">
      <text class="audio-title">{{ content.title }}</text>
      <text class="audio-description" v-if="content.description">
        {{ content.description }}
      </text>
      
      <!-- 音频标签 -->
      <view class="audio-tags" v-if="content.tags && content.tags.length">
        <text 
          v-for="tag in content.tags.slice(0, 3)" 
          :key="tag.id"
          class="tag"
        >
          {{ tag.name }}
        </text>
      </view>
    </view>

    <!-- 音频控制 -->
    <view class="audio-controls">
      <!-- 速度控制 -->
      <view class="speed-control">
        <text class="control-label">播放速度</text>
        <view class="speed-options">
          <text 
            v-for="speed in speedOptions"
            :key="speed"
            class="speed-option"
            :class="{ active: playbackRate === speed }"
            @click="setPlaybackRate(speed)"
          >
            {{ speed }}x
          </text>
        </view>
      </view>

      <!-- 音质选择 -->
      <view class="quality-control" v-if="content.quality_options">
        <text class="control-label">音质</text>
        <picker 
          :range="qualityOptions" 
          range-key="label"
          @change="onQualityChange"
        >
          <view class="quality-picker">
            <text>{{ currentQuality.label }}</text>
            <fui-icon name="arrow-down" color="#8d96a0" size="16" />
          </view>
        </picker>
      </view>

      <!-- 音效设置 -->
      <view class="audio-effects">
        <text class="control-label">音效</text>
        <view class="effect-buttons">
          <text 
            class="effect-button"
            :class="{ active: bassBoost }"
            @click="toggleBassBoost"
          >
            重低音
          </text>
          <text 
            class="effect-button"
            :class="{ active: virtualSurround }"
            @click="toggleVirtualSurround"
          >
            环绕声
          </text>
        </view>
      </view>
    </view>

    <!-- 频谱显示 -->
    <view class="spectrum-display" v-if="showSpectrum && isPlaying">
      <canvas 
        canvas-id="audioSpectrum"
        class="spectrum-canvas"
        @touchstart="onSpectrumTouch"
      ></canvas>
    </view>

    <!-- 歌词显示 -->
    <view class="lyrics-section" v-if="content.lyrics">
      <scroll-view 
        scroll-y 
        class="lyrics-scroll"
        :scroll-top="lyricsScrollTop"
        scroll-with-animation
      >
        <view class="lyrics-container">
          <view 
            v-for="(line, index) in parsedLyrics"
            :key="index"
            class="lyrics-line"
            :class="{ 
              active: currentLyricsIndex === index,
              passed: index < currentLyricsIndex
            }"
            @click="seekToLyrics(line.time)"
          >
            {{ line.text }}
          </view>
        </view>
      </scroll-view>

      <view class="lyrics-controls">
        <fui-icon 
          :name="showLyrics ? 'eye-off' : 'eye'" 
          color="#8d96a0" 
          size="20"
          @click="toggleLyrics"
        />
        <text class="lyrics-toggle-text">
          {{ showLyrics ? '隐藏歌词' : '显示歌词' }}
        </text>
      </view>
    </view>

    <!-- 定时关闭 -->
    <view class="sleep-timer" v-if="sleepTimer.enabled">
      <fui-icon name="clock" color="#ff9500" size="16" />
      <text class="timer-text">
        {{ formatSleepTimer(sleepTimer.remaining) }} 后停止播放
      </text>
      <text class="timer-cancel" @click="cancelSleepTimer">取消</text>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  content: {
    type: Object,
    required: true
  },
  isPlaying: {
    type: Boolean,
    default: false
  },
  currentTime: {
    type: Number,
    default: 0
  },
  duration: {
    type: Number,
    default: 0
  },
  volume: {
    type: Number,
    default: 1
  },
  playbackRate: {
    type: Number,
    default: 1
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'play', 'seek', 'volume-change', 'rate-change',
  'next', 'previous', 'quality-change'
])

// 数据
const speedOptions = [0.5, 0.75, 1, 1.25, 1.5, 2]
const bassBoost = ref(false)
const virtualSurround = ref(false)
const showSpectrum = ref(false)
const showLyrics = ref(true)
const currentQuality = ref({ label: '标准', value: 'standard' })
const currentLyricsIndex = ref(0)
const lyricsScrollTop = ref(0)
const sleepTimer = ref({
  enabled: false,
  remaining: 0,
  timer: null
})

// 计算属性
const qualityOptions = computed(() => {
  return props.content.quality_options || [
    { label: '标准', value: 'standard' },
    { label: '高清', value: 'high' },
    { label: '无损', value: 'lossless' }
  ]
})

const parsedLyrics = computed(() => {
  if (!props.content.lyrics) return []
  
  try {
    // 解析LRC格式歌词
    const lines = props.content.lyrics.split('\n')
    return lines.map(line => {
      const match = line.match(/\[(\d{2}):(\d{2})\.(\d{2})\](.*)/)
      if (match) {
        const minutes = parseInt(match[1])
        const seconds = parseInt(match[2])
        const centiseconds = parseInt(match[3])
        const time = minutes * 60 + seconds + centiseconds / 100
        return {
          time,
          text: match[4].trim()
        }
      }
      return {
        time: 0,
        text: line
      }
    }).filter(item => item.text)
  } catch (error) {
    console.error('歌词解析失败:', error)
    return []
  }
})

// 方法
const setPlaybackRate = (rate) => {
  emit('rate-change', rate)
}

const onQualityChange = (e) => {
  const selected = qualityOptions.value[e.detail.value]
  currentQuality.value = selected
  emit('quality-change', selected)
}

const toggleBassBoost = () => {
  bassBoost.value = !bassBoost.value
  // 这里可以调用音效API
}

const toggleVirtualSurround = () => {
  virtualSurround.value = !virtualSurround.value
  // 这里可以调用音效API
}

const toggleLyrics = () => {
  showLyrics.value = !showLyrics.value
}

const seekToLyrics = (time) => {
  emit('seek', time)
}

const handleImageError = () => {
  console.log('封面图片加载失败')
}

const onSpectrumTouch = (e) => {
  // 频谱触摸交互
  const x = e.touches[0].x
  const progress = x / e.currentTarget.offsetWidth
  const seekTime = progress * props.duration
  emit('seek', seekTime)
}

const formatSleepTimer = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const cancelSleepTimer = () => {
  if (sleepTimer.value.timer) {
    clearInterval(sleepTimer.value.timer)
  }
  sleepTimer.value.enabled = false
  sleepTimer.value.remaining = 0
}

// 监听器
watch(() => props.currentTime, (newTime) => {
  // 更新歌词位置
  if (parsedLyrics.value.length > 0) {
    for (let i = parsedLyrics.value.length - 1; i >= 0; i--) {
      if (newTime >= parsedLyrics.value[i].time) {
        currentLyricsIndex.value = i
        // 自动滚动歌词
        lyricsScrollTop.value = i * 60
        break
      }
    }
  }
})

// 生命周期
onMounted(() => {
  // 初始化音频可视化
  if (showSpectrum.value) {
    initSpectrum()
  }
})

onUnmounted(() => {
  cancelSleepTimer()
})

const initSpectrum = () => {
  // 初始化音频频谱显示
  const ctx = uni.createCanvasContext('audioSpectrum')
  // 这里实现频谱绘制逻辑
}
</script>

<style lang="scss" scoped>
.audio-player {
  padding: 32rpx;
}

.audio-visualizer {
  height: 120rpx;
  margin-bottom: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.wave-container {
  display: flex;
  align-items: flex-end;
  gap: 4rpx;
  height: 80rpx;
}

.wave-bar {
  width: 8rpx;
  background: linear-gradient(to top, #4CD964, #00d2ff);
  border-radius: 4rpx;
  animation: wave 1.5s infinite ease-in-out;
}

@keyframes wave {
  0%, 100% { 
    transform: scaleY(0.3);
    opacity: 0.8;
  }
  50% { 
    transform: scaleY(1);
    opacity: 1;
  }
}

.cover-section {
  display: flex;
  justify-content: center;
  margin-bottom: 32rpx;
}

.cover-container {
  width: 320rpx;
  height: 320rpx;
  position: relative;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 16rpx 40rpx rgba(0, 0, 0, 0.3);
  
  &.playing {
    animation: rotate 20s linear infinite;
  }
  
  &.loading::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.cover-image {
  width: 100%;
  height: 100%;
}

.play-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.pulse-ring {
  position: absolute;
  width: 80rpx;
  height: 80rpx;
  border: 2px solid #4CD964;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.8);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.pause-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(5px);
}

.audio-info {
  text-align: center;
  margin-bottom: 32rpx;
}

.audio-title {
  display: block;
  font-size: 36rpx;
  font-weight: 600;
  color: #fff;
  margin-bottom: 16rpx;
}

.audio-description {
  display: block;
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
  margin-bottom: 16rpx;
}

.audio-tags {
  display: flex;
  justify-content: center;
  gap: 16rpx;
  flex-wrap: wrap;
}

.tag {
  font-size: 24rpx;
  color: #4CD964;
  background: rgba(76, 217, 100, 0.2);
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  border: 1px solid rgba(76, 217, 100, 0.3);
}

.audio-controls {
  margin-bottom: 32rpx;
}

.speed-control,
.quality-control,
.audio-effects {
  margin-bottom: 24rpx;
}

.control-label {
  display: block;
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 16rpx;
}

.speed-options {
  display: flex;
  gap: 16rpx;
  justify-content: center;
}

.speed-option {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.7);
  padding: 12rpx 20rpx;
  border-radius: 20rpx;
  background: rgba(255, 255, 255, 0.1);
  
  &.active {
    color: #4CD964;
    background: rgba(76, 217, 100, 0.2);
    border: 1px solid rgba(76, 217, 100, 0.5);
  }
}

.quality-picker {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16rpx 24rpx;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12rpx;
  font-size: 28rpx;
  color: #fff;
}

.effect-buttons {
  display: flex;
  gap: 16rpx;
  justify-content: center;
}

.effect-button {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.7);
  padding: 12rpx 20rpx;
  border-radius: 20rpx;
  background: rgba(255, 255, 255, 0.1);
  
  &.active {
    color: #ff9500;
    background: rgba(255, 149, 0, 0.2);
    border: 1px solid rgba(255, 149, 0, 0.5);
  }
}

.spectrum-display {
  height: 120rpx;
  margin-bottom: 32rpx;
  border-radius: 12rpx;
  overflow: hidden;
}

.spectrum-canvas {
  width: 100%;
  height: 100%;
}

.lyrics-section {
  margin-bottom: 32rpx;
}

.lyrics-scroll {
  height: 300rpx;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12rpx;
  margin-bottom: 16rpx;
}

.lyrics-container {
  padding: 32rpx 24rpx;
}

.lyrics-line {
  font-size: 32rpx;
  color: rgba(255, 255, 255, 0.6);
  line-height: 60rpx;
  text-align: center;
  padding: 8rpx 0;
  transition: all 0.3s ease;
  
  &.active {
    color: #4CD964;
    font-weight: 600;
    transform: scale(1.1);
  }
  
  &.passed {
    color: rgba(255, 255, 255, 0.4);
  }
}

.lyrics-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
}

.lyrics-toggle-text {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
}

.sleep-timer {
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 16rpx 24rpx;
  background: rgba(255, 149, 0, 0.2);
  border-radius: 12rpx;
  border: 1px solid rgba(255, 149, 0, 0.3);
}

.timer-text {
  flex: 1;
  font-size: 24rpx;
  color: #ff9500;
}

.timer-cancel {
  font-size: 24rpx;
  color: #ff3b30;
  text-decoration: underline;
}
</style>