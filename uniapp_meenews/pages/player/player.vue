<template>
  <view class="player-page">
    <!-- 顶部导航 -->
    <NavBar background="transparent">
      <template #left>
        <fui-icon name="arrow-down" color="#fff" size="24" @click="minimize" />
      </template>
      <template #center>
        <view class="player-header">
          <text class="playing-from">正在播放</text>
          <text class="source-name">{{ currentTrack?.album || '推荐音乐' }}</text>
        </view>
      </template>
      <template #right>
        <fui-icon name="more" color="#fff" size="24" @click="showMoreActions" />
      </template>
    </NavBar>

    <!-- 专辑封面 -->
    <view class="cover-section">
      <view class="cover-container" :class="{ playing: isPlaying }">
        <BaseImage :src="currentTrack?.coverUrl" class="cover-image" mode="aspectFill" />
      </view>
    </view>

    <!-- 歌曲信息 -->
    <view class="track-info">
      <text class="track-title">{{ currentTrack?.title }}</text>
      <text class="track-artist">{{ currentTrack?.artist }}</text>
    </view>

    <!-- 进度条 -->
    <view class="progress-section">
      <text class="time-text">{{ formatTime(currentTime) }}</text>
      <ProgressBar :current="currentTime" :total="duration" @seek="handleSeek" />
      <text class="time-text">{{ formatTime(duration) }}</text>
    </view>

    <!-- 播放控制 -->
    <PlayerControls :isPlaying="isPlaying" :repeatMode="repeatMode" :shuffleMode="shuffleMode"
      @togglePlay="togglePlay" @playPrevious="playPrevious" @playNext="playNext"
      @toggleRepeat="toggleRepeat" @toggleShuffle="toggleShuffle" />

    <!-- 底部功能区 -->
    <view class="bottom-actions">
      <fui-icon name="lyrics" color="#8d96a0" size="24" @click="showLyrics = true" />
      <fui-icon name="share" color="#8d96a0" size="24" @click="shareTrack" />
      <text class="swipe-hint">向上滑动查看歌词</text>
    </view>

    <!-- 歌词弹窗 -->
    <LyricsModal v-if="showLyrics" :lyrics="lyrics" :current-line="currentLyricLine" @close="showLyrics = false" />
  </view>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { usePlayerStore } from '@/store/player'
import NavBar from '@/components/common/NavBar.vue'
import ProgressBar from '@/components/player/ProgressBar.vue'
import PlayerControls from '@/components/player/PlayerControls.vue'
import LyricsModal from '@/components/player/LyricsModal.vue'
import BaseImage from '@/components/common/BaseImage.vue'

const playerStore = usePlayerStore()

export default {
  name: 'Player',
  components: { NavBar, ProgressBar, PlayerControls, LyricsModal, BaseImage },
  setup() {
    const showLyrics = ref(false)
    const currentTime = ref(0)
    const timer = ref(null)
    // 歌词 mock
    const lyrics = ref([
      { text: 'AI驱动的资讯音频社区平台' },
      { text: '专注于将最新资讯通过AI视频解说和音频形式呈现' },
      { text: '为用户提供个性化的资讯获取和社交体验' },
      { text: '羊咩快报，陪你每一天' }
    ])
    const currentLyricLine = ref(0)

    // 播放器状态
    const currentTrack = computed(() => playerStore.currentTrack)
    const isPlaying = computed(() => playerStore.isPlaying)
    const duration = computed(() => playerStore.duration)
    const repeatMode = ref('none') // 可与 store 联动
    const shuffleMode = ref(false) // 可与 store 联动

    // 格式化时间
    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins}:${secs.toString().padStart(2, '0')}`
    }

    // 播放控制
    const togglePlay = () => {
      if (isPlaying.value) playerStore.pause()
      else if (currentTrack.value) playerStore.playTrack(currentTrack.value)
    }
    const playPrevious = () => {
      // 可扩展上一首逻辑
    }
    const playNext = () => {
      // 可扩展下一首逻辑
    }
    const toggleRepeat = () => {
      // 可扩展循环模式
    }
    const toggleShuffle = () => {
      // 可扩展随机模式
    }
    const handleSeek = (time) => {
      playerStore.setCurrentTime(time)
      currentTime.value = time
    }
    const minimize = () => {
      uni.navigateBack()
    }
    const showMoreActions = () => {
      uni.showToast({ title: '更多功能开发中', icon: 'none' })
    }
    const shareTrack = () => {
      uni.showToast({ title: '分享功能开发中', icon: 'none' })
    }

    // 歌词高亮模拟
    const updateLyricLine = () => {
      if (!lyrics.value.length) return
      const idx = Math.floor((currentTime.value / (duration.value || 1)) * lyrics.value.length)
      currentLyricLine.value = Math.min(idx, lyrics.value.length - 1)
    }

    onMounted(() => {
      timer.value = setInterval(() => {
        if (isPlaying.value) {
          currentTime.value = playerStore.currentTime
          updateLyricLine()
        }
      }, 1000)
    })
    onUnmounted(() => {
      if (timer.value) clearInterval(timer.value)
    })

    return {
      currentTrack,
      isPlaying,
      duration,
      currentTime,
      repeatMode,
      shuffleMode,
      showLyrics,
      lyrics,
      currentLyricLine,
      formatTime,
      togglePlay,
      playPrevious,
      playNext,
      toggleRepeat,
      toggleShuffle,
      handleSeek,
      minimize,
      showMoreActions,
      shareTrack
    }
  }
}
</script>

<style lang="scss" scoped>
.player-page {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0 32rpx;
  display: flex;
  flex-direction: column;
}
.player-header {
  text-align: center;
  .playing-from {
    display: block;
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.8);
  }
  .source-name {
    display: block;
    font-size: 28rpx;
    color: #fff;
    font-weight: 500;
  }
}
.cover-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80rpx 0;
}
.cover-container {
  width: 560rpx;
  height: 560rpx;
  position: relative;
  border-radius: 24rpx;
  overflow: hidden;
  box-shadow: 0 20rpx 60rpx rgba(0, 0, 0, 0.3);
  &.playing {
    animation: pulse 2s infinite ease-in-out;
  }
}
.cover-image {
  width: 100%;
  height: 100%;
}
.track-info {
  text-align: center;
  margin-bottom: 60rpx;
  .track-title {
    display: block;
    font-size: 48rpx;
    font-weight: 600;
    color: #fff;
    margin-bottom: 16rpx;
  }
  .track-artist {
    display: block;
    font-size: 32rpx;
    color: rgba(255, 255, 255, 0.8);
  }
}
.progress-section {
  display: flex;
  align-items: center;
  margin-bottom: 80rpx;
  .time-text {
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.8);
    min-width: 80rpx;
    text-align: center;
  }
}
.bottom-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 60rpx;
  .swipe-hint {
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.6);
  }
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
</style> 