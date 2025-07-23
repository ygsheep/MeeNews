<template>
  <view class="mini-player" v-if="currentContent" :class="{ expanded: isExpanded }">
    <!-- 进度条 -->
    <view class="mini-progress">
      <view 
        class="progress-fill" 
        :style="{ width: `${progressPercent}%` }"
      ></view>
    </view>

    <!-- 主要内容区域 -->
    <view class="mini-content" @click="expandPlayer">
      <!-- 内容信息 -->
      <view class="content-info">
        <image 
          :src="currentContent.cover_url || currentContent.thumbnail_url" 
          class="content-thumb"
          :class="contentType"
          @error="handleImageError"
        />
        
        <view class="content-details">
          <text class="content-title">{{ currentContent.title }}</text>
          <view class="content-meta">
            <text class="content-author">{{ getAuthorName() }}</text>
            <view class="content-type-badge" :class="contentType">
              <fui-icon :name="getTypeIcon()" size="12" color="#fff" />
              <text class="type-text">{{ getTypeLabel() }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 播放控制 -->
      <view class="play-controls">
        <!-- 主播放按钮 -->
        <view class="main-control" @click.stop="togglePlay">
          <view class="play-button" :class="{ playing: isPlaying }">
            <fui-icon 
              :name="getPlayIcon()" 
              color="#fff" 
              size="20"
            />
          </view>
        </view>

        <!-- 次要控制 -->
        <view class="secondary-controls" v-if="!isExpanded">
          <fui-icon 
            name="skip-next" 
            :color="canPlayNext ? '#2c3038' : '#8d96a0'" 
            size="18"
            @click.stop="playNext"
            :class="{ disabled: !canPlayNext }"
          />
          <fui-icon 
            name="close" 
            color="#8d96a0" 
            size="18"
            @click.stop="closePlayer"
          />
        </view>
      </view>
    </view>

    <!-- 展开状态下的额外控制 -->
    <view class="expanded-controls" v-if="isExpanded">
      <view class="expanded-info">
        <!-- 播放时间 -->
        <view class="time-display">
          <text class="current-time">{{ formattedCurrentTime }}</text>
          <text class="separator">/</text>
          <text class="total-time">{{ formattedDuration }}</text>
        </view>

        <!-- 播放模式指示 -->
        <view class="mode-indicators">
          <view class="mode-item" v-if="shuffleMode">
            <fui-icon name="shuffle" color="#4CD964" size="14" />
          </view>
          <view class="mode-item" v-if="repeatMode !== 'none'">
            <fui-icon 
              :name="repeatMode === 'one' ? 'repeat-one' : 'repeat'" 
              color="#4CD964" 
              size="14" 
            />
          </view>
          <view class="mode-item" v-if="contentType === 'article' && articleTTSEnabled">
            <fui-icon name="volume-up" color="#4CD964" size="14" />
          </view>
        </view>
      </view>

      <!-- 进度控制 -->
      <ProgressBar 
        :current="currentTime"
        :total="duration"
        :buffered="bufferedTime"
        @seek="handleSeek"
        :height="'4rpx'"
        :show-thumb="false"
        :show-tooltip="false"
        class="mini-progress-bar"
      />

      <!-- 完整控制栏 -->
      <view class="full-controls">
        <fui-icon 
          name="skip-previous" 
          :color="canPlayPrevious ? '#2c3038' : '#8d96a0'" 
          size="20"
          @click.stop="playPrevious"
          :class="{ disabled: !canPlayPrevious }"
        />
        
        <view class="control-group">
          <fui-icon 
            name="skip-back-15" 
            color="#2c3038" 
            size="18"
            @click.stop="skipBackward"
            v-if="contentType !== 'article'"
          />
          
          <view class="main-play-button" @click.stop="togglePlay">
            <fui-icon 
              :name="getPlayIcon()" 
              color="#fff" 
              size="24"
            />
          </view>
          
          <fui-icon 
            name="skip-forward-30" 
            color="#2c3038" 
            size="18"
            @click.stop="skipForward"
            v-if="contentType !== 'article'"
          />
        </view>
        
        <fui-icon 
          name="skip-next" 
          :color="canPlayNext ? '#2c3038' : '#8d96a0'" 
          size="20"
          @click.stop="playNext"
          :class="{ disabled: !canPlayNext }"
        />
      </view>

      <!-- 快捷操作 -->
      <view class="quick-actions">
        <view class="action-item" @click.stop="toggleLike">
          <fui-icon 
            :name="currentContent.is_liked ? 'heart-fill' : 'heart'" 
            :color="currentContent.is_liked ? '#ff3b30' : '#8d96a0'" 
            size="16"
          />
        </view>
        
        <view class="action-item" @click.stop="addToPlaylist">
          <fui-icon name="playlist-add" color="#8d96a0" size="16" />
        </view>
        
        <view class="action-item" @click.stop="shareContent">
          <fui-icon name="share" color="#8d96a0" size="16" />
        </view>
        
        <view class="action-item" @click.stop="showMoreActions">
          <fui-icon name="more" color="#8d96a0" size="16" />
        </view>
      </view>

      <!-- 收起按钮 -->
      <view class="collapse-button" @click.stop="collapsePlayer">
        <fui-icon name="chevron-down" color="#8d96a0" size="20" />
      </view>
    </view>

    <!-- 内容类型特定的状态指示 -->
    <view class="status-indicators">
      <!-- 音频波形指示 -->
      <view class="audio-waves" v-if="contentType === 'audio' && isPlaying">
        <view 
          v-for="i in 4" 
          :key="i" 
          class="wave"
          :style="{ animationDelay: `${i * 0.1}s` }"
        ></view>
      </view>
      
      <!-- 视频播放指示 -->
      <view class="video-indicator" v-if="contentType === 'video' && isPlaying">
        <fui-icon name="video" color="#007aff" size="12" />
      </view>
      
      <!-- 文章阅读指示 -->
      <view class="reading-indicator" v-if="contentType === 'article' && isPlaying">
        <view class="reading-progress-ring">
          <view 
            class="progress-ring-fill"
            :style="{ transform: `rotate(${(currentTime / duration) * 360}deg)` }"
          ></view>
        </view>
      </view>
    </view>

    <!-- 错误状态 -->
    <view class="error-state" v-if="error">
      <fui-icon name="alert-circle" color="#ff3b30" size="16" />
      <text class="error-text">{{ error }}</text>
      <text class="retry-button" @click.stop="retryPlay">重试</text>
    </view>

    <!-- 加载状态 -->
    <view class="loading-state" v-if="isLoading">
      <fui-loading size="small" color="#4CD964" />
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { usePlayerStore } from '@/store/modules/player'
import ProgressBar from './ProgressBar.vue'

const playerStore = usePlayerStore()

// 数据
const isExpanded = ref(false)

// 计算属性
const currentContent = computed(() => playerStore.currentContent)
const isPlaying = computed(() => playerStore.isPlaying)
const currentTime = computed(() => playerStore.currentTime)
const duration = computed(() => playerStore.duration)
const bufferedTime = computed(() => playerStore.bufferedTime)
const progressPercent = computed(() => playerStore.progressPercent)
const contentType = computed(() => playerStore.contentType)
const canPlayPrevious = computed(() => playerStore.canPlayPrevious)
const canPlayNext = computed(() => playerStore.canPlayNext)
const shuffleMode = computed(() => playerStore.shuffleMode)
const repeatMode = computed(() => playerStore.repeatMode)
const articleTTSEnabled = computed(() => playerStore.articleTTSEnabled)
const error = computed(() => playerStore.error)
const isLoading = computed(() => playerStore.isLoading)
const formattedCurrentTime = computed(() => playerStore.formattedCurrentTime)
const formattedDuration = computed(() => playerStore.formattedDuration)

// 方法
const togglePlay = () => {
  playerStore.togglePlay()
}

const playNext = () => {
  if (canPlayNext.value) {
    playerStore.playNext()
  }
}

const playPrevious = () => {
  if (canPlayPrevious.value) {
    playerStore.playPrevious()
  }
}

const skipForward = () => {
  const newTime = Math.min(duration.value, currentTime.value + 30)
  playerStore.seek(newTime)
}

const skipBackward = () => {
  const newTime = Math.max(0, currentTime.value - 15)
  playerStore.seek(newTime)
}

const handleSeek = (time) => {
  playerStore.seek(time)
}

const expandPlayer = () => {
  if (contentType.value === 'article') {
    // 文章内容直接跳转到阅读页面
    uni.navigateTo({
      url: `/pages/content/article?id=${currentContent.value.id}`
    })
  } else {
    // 音频和视频展开迷你播放器
    isExpanded.value = true
  }
}

const collapsePlayer = () => {
  isExpanded.value = false
}

const closePlayer = () => {
  playerStore.stop()
  playerStore.currentContent = null
}

const retryPlay = () => {
  if (currentContent.value) {
    playerStore.playContent(currentContent.value)
  }
}

const toggleLike = async () => {
  try {
    await api.content.toggleLike(currentContent.value.id)
    currentContent.value.is_liked = !currentContent.value.is_liked
  } catch (error) {
    uni.showToast({
      title: '操作失败',
      icon: 'error'
    })
  }
}

const addToPlaylist = () => {
  uni.showActionSheet({
    itemList: ['添加到我喜欢', '添加到播放列表', '创建新播放列表'],
    success: (res) => {
      switch (res.tapIndex) {
        case 0:
          toggleLike()
          break
        case 1:
          // 显示播放列表选择
          break
        case 2:
          // 创建新播放列表
          break
      }
    }
  })
}

const shareContent = () => {
  const content = currentContent.value
  uni.share({
    provider: 'weixin',
    scene: 'WXSceneTimeline',
    type: 0,
    title: content.title,
    summary: content.description || content.summary,
    imageUrl: content.cover_url || content.thumbnail_url,
    href: `https://app.yangmie.com/${contentType.value}/${content.id}`
  })
}

const showMoreActions = () => {
  uni.showActionSheet({
    itemList: ['收藏', '下载', '举报', '不感兴趣'],
    success: (res) => {
      // 处理更多操作
    }
  })
}

const getAuthorName = () => {
  const content = currentContent.value
  if (!content) return ''
  
  return content.author?.name || 
         content.artist?.name || 
         content.creator?.name || 
         content.source?.name ||
         '未知作者'
}

const getTypeIcon = () => {
  switch (contentType.value) {
    case 'audio': return 'headphones'
    case 'video': return 'video'
    case 'article': return 'file-text'
    default: return 'play'
  }
}

const getTypeLabel = () => {
  switch (contentType.value) {
    case 'audio': return '音频'
    case 'video': return '视频'
    case 'article': return '文章'
    default: return '内容'
  }
}

const getPlayIcon = () => {
  if (isLoading.value) return 'more-horizontal'
  if (contentType.value === 'article' && !articleTTSEnabled.value) {
    return isPlaying.value ? 'pause' : 'book-open'
  }
  return isPlaying.value ? 'pause' : 'play'
}

const handleImageError = () => {
  // 处理图片加载失败
}
</script>

<style lang="scss" scoped>
.mini-player {
  position: fixed;
  bottom: 100rpx; // 为底部导航栏留空间
  left: 16rpx;
  right: 16rpx;
  background: #ffffff;
  border-radius: 16rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
  z-index: 1000;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  &.expanded {
    bottom: 16rpx;
    border-radius: 24rpx;
    box-shadow: 0 16rpx 48rpx rgba(0, 0, 0, 0.2);
  }
}

.mini-progress {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4rpx;
  background: rgba(76, 217, 100, 0.1);
  z-index: 1;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4CD964, #00d2ff);
  transition: width 0.3s ease;
}

.mini-content {
  display: flex;
  align-items: center;
  padding: 16rpx 24rpx;
  gap: 16rpx;
}

.content-info {
  display: flex;
  align-items: center;
  flex: 1;
  min-width: 0;
  gap: 16rpx;
}

.content-thumb {
  width: 64rpx;
  height: 64rpx;
  border-radius: 8rpx;
  flex-shrink: 0;
  
  &.audio {
    border-radius: 50%;
  }
  
  &.video {
    border-radius: 8rpx;
  }
  
  &.article {
    border-radius: 12rpx;
  }
}

.content-details {
  flex: 1;
  min-width: 0;
}

.content-title {
  display: block;
  font-size: 28rpx;
  font-weight: 500;
  color: #2c3038;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 6rpx;
}

.content-meta {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.content-author {
  font-size: 24rpx;
  color: #8d96a0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.content-type-badge {
  display: flex;
  align-items: center;
  gap: 4rpx;
  padding: 4rpx 8rpx;
  border-radius: 8rpx;
  
  &.audio {
    background: #ff9500;
  }
  
  &.video {
    background: #007aff;
  }
  
  &.article {
    background: #34c759;
  }
}

.type-text {
  font-size: 20rpx;
  color: #fff;
}

.play-controls {
  display: flex;
  align-items: center;
  gap: 16rpx;
  flex-shrink: 0;
}

.main-control {
  position: relative;
}

.play-button {
  width: 56rpx;
  height: 56rpx;
  border-radius: 50%;
  background: #4CD964;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  
  &.playing {
    background: #ff9500;
    transform: scale(0.9);
  }
}

.secondary-controls {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.disabled {
  opacity: 0.5;
}

.expanded-controls {
  padding: 0 24rpx 24rpx;
  border-top: 1px solid #f0f0f0;
}

.expanded-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
  padding-top: 16rpx;
}

.time-display {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.current-time,
.total-time {
  font-size: 24rpx;
  color: #2c3038;
}

.separator {
  font-size: 24rpx;
  color: #8d96a0;
}

.mode-indicators {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.mode-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32rpx;
  height: 32rpx;
  border-radius: 50%;
  background: rgba(76, 217, 100, 0.1);
}

.mini-progress-bar {
  margin-bottom: 16rpx;
}

.full-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.main-play-button {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  background: #4CD964;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4rpx 16rpx rgba(76, 217, 100, 0.3);
}

.quick-actions {
  display: flex;
  justify-content: center;
  gap: 48rpx;
  margin-bottom: 16rpx;
}

.action-item {
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.collapse-button {
  display: flex;
  justify-content: center;
  padding: 8rpx 0;
}

.status-indicators {
  position: absolute;
  top: 20rpx;
  right: 20rpx;
  z-index: 2;
}

.audio-waves {
  display: flex;
  align-items: center;
  gap: 2rpx;
}

.wave {
  width: 3rpx;
  height: 12rpx;
  background: #4CD964;
  border-radius: 2rpx;
  animation: wave 1.2s infinite ease-in-out;
}

@keyframes wave {
  0%, 100% {
    transform: scaleY(0.4);
  }
  50% {
    transform: scaleY(1);
  }
}

.video-indicator {
  width: 24rpx;
  height: 24rpx;
  border-radius: 50%;
  background: rgba(0, 122, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.reading-indicator {
  width: 24rpx;
  height: 24rpx;
  position: relative;
}

.reading-progress-ring {
  width: 100%;
  height: 100%;
  border: 2rpx solid rgba(52, 199, 89, 0.2);
  border-radius: 50%;
  position: relative;
  overflow: hidden;
}

.progress-ring-fill {
  position: absolute;
  top: -1rpx;
  left: 50%;
  width: 2rpx;
  height: 50%;
  background: #34c759;
  transform-origin: bottom center;
  transition: transform 0.3s ease;
}

.error-state {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  gap: 12rpx;
  background: rgba(255, 59, 48, 0.1);
  padding: 16rpx 24rpx;
  border-radius: 20rpx;
  border: 1px solid rgba(255, 59, 48, 0.3);
}

.error-text {
  font-size: 24rpx;
  color: #ff3b30;
}

.retry-button {
  font-size: 24rpx;
  color: #4CD964;
  text-decoration: underline;
}

.loading-state {
  position: absolute;
  top: 50%;
  right: 24rpx;
  transform: translateY(-50%);
}
</style>