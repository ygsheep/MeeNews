<template>
  <view class="video-player-simple" :class="{ fullscreen: fullscreen }">
    <view class="video-center-container">
      <video
        :src="content.video_content.video_url"
        ref="videoRef"
        :autoplay="autoplay"
        :poster="content.cover_url || content.source_url"
        :muted="muted"
        :controls="false"
        :loop="false"
        :show-center-play-btn="false"
        :show-play-btn="false"
        :show-fullscreen-btn="false"
        :enable-progress-gesture="true"
        :page-gesture="true"
        object-fit="contain"
        class="video-element-simple"
        @play="onVideoPlay"
        @pause="onVideoPause"
        @ended="onVideoEnded"
        @timeupdate="onTimeUpdate"
        @loadedmetadata="onLoadedMetadata"
        @error="onVideoError"
        @waiting="onVideoWaiting"
        @canplay="onVideoCanplay"
        @fullscreenchange="onFullscreenChange"
      />
      <!-- 居中播放/暂停按钮 -->
      <view class="center-play-btn" @click="togglePlay">
        <view class="play-btn-circle">
          <fui-icon :name="isPlaying ? 'pause' : 'play'" color="#fff" size="44" />
        </view>
      </view>
    </view>
    <!-- 进度条和全屏按钮 -->
    <view class="video-bottom-bar">
      <view class="progress-section">
        <text class="time-display">{{ formattedCurrentTime }}</text>
        <ProgressBar 
          :current="currentTime"
          :total="duration"
          :buffered="bufferedTime"
          @seek="handleSeek"
          class="video-progress-simple"
        />
        <text class="time-display">{{ formattedDuration }}</text>
      </view>
      <view class="fullscreen-btn-dark" @click="toggleFullscreen">
        <fui-icon :name="fullscreen ? 'minimize' : 'maximize'" color="#fff" size="22" />
        <text class="fullscreen-btn-text">全屏观看</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import ProgressBar from './ProgressBar.vue'

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
  bufferedTime: {
    type: Number,
    default: 0
  },
  volume: {
    type: Number,
    default: 1
  },
  fullscreen: {
    type: Boolean,
    default: false
  },
  muted: {
    type: Boolean,
    default: false
  },
  playbackRate: {
    type: Number,
    default: 1
  }
})

const emit = defineEmits([
  'play', 'seek', 'volume-change', 'fullscreen-change',
  'next', 'previous', 'quality-change', 'mute-change'
])

// 数据
const showControls = ref(true)
const controlsTimer = ref(null)
const isLoading = ref(false)
const isBuffering = ref(false)
const showGestureHints = ref(false)
const descriptionExpanded = ref(false)
const showQualitySelector = ref(false)
const subtitleEnabled = ref(false)
const autoplayNext = ref(true)
const currentQuality = ref({ label: '高清', value: 'hd' })
const relatedVideos = ref([])
const autoplay = ref(true)

// 监听内容切换后自动播放
const videoRef = ref(null)
watch(() => props.content && props.content.video_content && props.content.video_content.video_url, async (newUrl, oldUrl) => {
  if (autoplay.value && newUrl && newUrl !== oldUrl) {
    await nextTick()
    try {
      videoRef.value && videoRef.value.play && videoRef.value.play()
    } catch (e) {}
  }
})

const speedOptions = ['0.5x', '0.75x', '1x', '1.25x', '1.5x', '2x']

const gestureAction = ref({
  show: false,
  icon: '',
  text: '',
  timer: null
})

// 计算属性
const qualityOptions = computed(() => {
  return props.content.quality_options || [
    { label: '流畅', value: 'sd', description: '360P' },
    { label: '标清', value: 'md', description: '480P' },
    { label: '高清', value: 'hd', description: '720P' },
    { label: '超清', value: 'fhd', description: '1080P' },
    { label: '4K', value: '4k', description: '2160P' }
  ]
})

const formattedCurrentTime = computed(() => {
  return formatTime(props.currentTime)
})

const formattedDuration = computed(() => {
  return formatTime(props.duration)
})

// 方法
const togglePlay = () => {
  emit('play')
  showControlsTemporarily()
}

const handleSeek = (time) => {
  emit('seek', time)
  showControlsTemporarily()
}

const toggleMute = () => {
  emit('mute-change', !props.muted)
  showGestureAction('volume-off', props.muted ? '取消静音' : '静音')
}

const toggleFullscreen = () => {
  emit('fullscreen-change', !props.fullscreen)
}

const onVolumeChange = (e) => {
  const volume = e.detail.value / 100
  emit('volume-change', volume)
  showGestureAction('volume-up', `音量 ${Math.round(volume * 100)}%`)
}

const onSpeedChange = (e) => {
  const speedValue = speedOptions[e.detail.value]
  const rate = parseFloat(speedValue.replace('x', ''))
  emit('rate-change', rate)
  showGestureAction('fast-forward', `播放速度 ${speedValue}`)
}

const selectQuality = (quality) => {
  currentQuality.value = quality
  emit('quality-change', quality)
  showQualitySelector.value = false
  showGestureAction('video', `切换至${quality.label}`)
}

const showQualityPicker = () => {
  showQualitySelector.value = true
}

const showSubtitleSettings = () => {
  // 实现字幕设置
  uni.showActionSheet({
    itemList: ['开启字幕', '关闭字幕', '字幕样式'],
    success: (res) => {
      if (res.tapIndex === 0) {
        subtitleEnabled.value = true
      } else if (res.tapIndex === 1) {
        subtitleEnabled.value = false
      }
    }
  })
}

const onAutoplayChange = (e) => {
  autoplayNext.value = e.detail.value
}

const toggleDescription = () => {
  descriptionExpanded.value = !descriptionExpanded.value
}

const searchByTag = (tag) => {
  uni.navigateTo({
    url: `/pages/discover/search?q=${encodeURIComponent(tag.name)}&type=video`
  })
}

const playRelatedVideo = (video) => {
  emit('switch-content', video)
}

const shareVideo = () => {
  uni.share({
    provider: 'weixin',
    scene: 'WXSceneTimeline',
    type: 5,
    title: props.content.title,
    summary: props.content.description,
    imageUrl: props.content.thumbnail_url,
    href: `https://app.yangmie.com/video/${props.content.id}`
  })
}

const showMoreActions = () => {
  uni.showActionSheet({
    itemList: ['收藏', '下载', '举报', '不感兴趣'],
    success: (res) => {
      switch (res.tapIndex) {
        case 0:
          // 收藏
          break
        case 1:
          // 下载
          break
        case 2:
          // 举报
          break
        case 3:
          // 不感兴趣
          break
      }
    }
  })
}

const showControlsTemporarily = () => {
  showControls.value = true
  
  if (controlsTimer.value) {
    clearTimeout(controlsTimer.value)
  }
  
  controlsTimer.value = setTimeout(() => {
    if (props.isPlaying) {
      showControls.value = false
    }
  }, 3000)
}

const showGestureAction = (icon, text) => {
  gestureAction.value.show = true
  gestureAction.value.icon = icon
  gestureAction.value.text = text
  
  if (gestureAction.value.timer) {
    clearTimeout(gestureAction.value.timer)
  }
  
  gestureAction.value.timer = setTimeout(() => {
    gestureAction.value.show = false
  }, 1500)
}

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  
  if (hours > 0) {
    return `${hours}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const formatDuration = (seconds) => {
  return formatTime(seconds)
}

// 视频事件处理
const onVideoPlay = () => {
  isLoading.value = false
}

const onVideoPause = () => {
  showControls.value = true
}

const onVideoEnded = () => {
  emit('ended')
}

const onTimeUpdate = (e) => {
  // 视频时间更新通过props传入，这里不需要处理
}

const onLoadedMetadata = (e) => {
  isLoading.value = false
}

const onVideoError = (e) => {
  console.error('视频播放错误:', e)
  emit('error', e)
}

const onVideoWaiting = () => {
  isBuffering.value = true
}

const onVideoCanplay = () => {
  isBuffering.value = false
}

const onFullscreenChange = (e) => {
  emit('fullscreen-change', e.detail.fullScreen)
}

// 触摸手势处理
const onTouchStart = (e) => {
  // 记录触摸开始位置
}

const onTouchMove = (e) => {
  // 处理手势操作
}

const onTouchEnd = (e) => {
  // 处理手势结束
}

// 监听器
watch(() => props.isPlaying, (playing) => {
  if (playing) {
    showControlsTemporarily()
  }
})

// 生命周期
onMounted(() => {
  // 加载相关视频
  loadRelatedVideos()
  
  // 设置手势提示
  setTimeout(() => {
    showGestureHints.value = true
    setTimeout(() => {
      showGestureHints.value = false
    }, 3000)
  }, 1000)
})

onUnmounted(() => {
  if (controlsTimer.value) {
    clearTimeout(controlsTimer.value)
  }
  if (gestureAction.value.timer) {
    clearTimeout(gestureAction.value.timer)
  }
})

const loadRelatedVideos = async () => {
  // 加载相关视频列表
  try {
    // 这里调用API获取相关视频
    relatedVideos.value = []
  } catch (error) {
    console.error('加载相关视频失败:', error)
  }
}
</script>

<style lang="scss" scoped>
.video-player-simple {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100vw;
  height: 100vh;
  background: transparent;
  &.fullscreen {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: 9999;
    background: #000;
  }
}
.video-center-container {
  width: 90vw;
  max-width: 600px;
  aspect-ratio: 16/9;
  background: #000;
  border-radius: 18px;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.video-element-simple {
  width: 100%;
  height: 100%;
  background: #000;
}
.center-play-btn {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
}
.play-btn-circle {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(0,0,0,0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255,255,255,0.18);
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
.video-bottom-bar {
  width: 90vw;
  max-width: 600px;
  margin: 0 auto;
  margin-top: 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
}
.progress-section {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
}
.video-progress-simple {
  flex: 1;
}
.time-display {
  color: #fff;
  font-size: 16px;
  min-width: 48px;
  text-align: center;
}
.fullscreen-btn-dark {
  margin: 0 auto;
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #222;
  border-radius: 22px;
  padding: 0 22px;
  height: 44px;
  min-width: 120px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.18);
  cursor: pointer;
  font-weight: bold;
  color: #fff;
  font-size: 18px;
}
.fullscreen-btn-text {
  margin-left: 8px;
  font-size: 18px;
  font-weight: bold;
  color: #fff;
}
</style>