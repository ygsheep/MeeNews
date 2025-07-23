<template>
  <view class="media-player-fullscreen" v-if="currentContent">
    <!-- 视频内容专属弹窗布局 -->
    <template v-if="isVideoContent">
      <view class="player-bg">
        <image :src="currentContent.cover_url || currentContent.thumbnail_url" class="bg-image" mode="aspectFill" />
        <view class="bg-mask"></view>
      </view>
      <view class="player-content" style="margin-top:0;align-items:center;justify-content:center;">
        <!-- 只显示视频播放器 -->
        <VideoPlayer
          :content="currentContent"
          :is-playing="isPlaying"
          :current-time="currentTime"
          :duration="duration"
          :volume="volume"
          :fullscreen="videoFullscreen"
          :muted="videoMuted"
          @play="togglePlay"
          @seek="handleSeek"
          @volume-change="setVolume"
          @fullscreen-change="toggleFullscreen"
          @next="playNext"
          @previous="playPrevious"
        />
        <!-- 全屏按钮，居中显示 -->
        <!-- 已按用户要求删除全屏按钮 -->
      </view>
    </template>

    <!-- 音频内容专属弹窗布局 -->
    <template v-else-if="isAudioContent">
      <view class="player-bg">
        <image :src="currentContent.cover_url || currentContent.thumbnail_url" class="bg-image" mode="aspectFill" />
        <view class="bg-mask"></view>
      </view>
      <view class="player-content" style="margin-top:80rpx;align-items:center;justify-content:flex-start;">
        <!-- 居中显示文章内容（可滚动） -->
        <view style="width:100%;max-width:700rpx;min-height:400rpx;background:rgba(255,255,255,0.95);border-radius:24rpx;padding:32rpx 24rpx;box-shadow:0 8rpx 32rpx rgba(0,0,0,0.08);margin-bottom:32rpx;">
          <ArticleReader
            :content="currentContent"
            :is-playing="isPlaying"
            :reading-time="currentTime"
            :estimated-duration="duration"
            :tts-enabled="articleTTSEnabled"
            :scroll-position="articleScrollPosition"
            @play="togglePlay"
            @tts-toggle="toggleTTS"
            @scroll="handleArticleScroll"
            @next="playNext"
            @previous="playPrevious"
          />
        </view>
        <!-- 播放控制区 -->
        <view style="width:100%;display:flex;justify-content:center;align-items:center;margin-top:12rpx;">
          <fui-icon name="skip-previous" :color="canPlayPrevious ? '#4CD964' : '#8d96a0'" size="32" @click="playPrevious" :class="{ disabled: !canPlayPrevious }" />
          <view class="play-button" style="margin:0 32rpx;" @click="togglePlay">
            <fui-icon :name="isPlaying ? 'pause' : 'play'" color="#fff" size="40" />
          </view>
          <fui-icon name="skip-next" :color="canPlayNext ? '#4CD964' : '#8d96a0'" size="32" @click="playNext" :class="{ disabled: !canPlayNext }" />
        </view>
        <!-- 进度条 -->
        <view style="width:100%;margin-top:16rpx;">
          <ProgressBar
            :current="currentTime"
            :total="duration"
            :buffered="bufferedTime"
            @seek="handleSeek"
            class="progress-bar"
          />
          <view style="display:flex;justify-content:space-between;font-size:22rpx;color:#888;margin-top:4rpx;">
            <text>{{ formattedCurrentTime }}</text>
            <text>{{ formattedDuration }}</text>
          </view>
        </view>
      </view>
    </template>

    <!-- 其它内容类型（如文章）保持原有逻辑 -->
    <template v-else>
      <!-- 顶部透明渐变栏，可放返回/关闭按钮 -->
      <view class="player-header">
        <fui-icon name="arrow-down" color="#fff" size="28" @click="$emit('close')" />
        <text style="color:#fff;font-size:28rpx;margin-left:12rpx;" @click="$emit('close')">返回</text>
        <text class="player-title">{{ getContentTypeLabel() }}播放</text>
      </view>
      <view class="player-bg">
        <image :src="currentContent.cover_url || currentContent.thumbnail_url" class="bg-image" mode="aspectFill" />
        <view class="bg-mask"></view>
      </view>
      <view class="player-content">
        <!-- 调试信息 -->
        <view style="background:#222;color:#fff;padding:4px 8px;font-size:12px;opacity:0.85;">
          <text>type: {{ currentContent.type }}</text>
          <text> | isAudioContent: {{ isAudioContent }}</text>
          <text> | isVideoContent: {{ isVideoContent }}</text>
          <text> | isArticleContent: {{ isArticleContent }}</text>
        </view>
        <!-- 封面大图带旋转动画 -->
        <view class="cover-container" :class="{ 'rotating': isPlaying && isAudioContent }">
          <image :src="currentContent.cover_url || currentContent.thumbnail_url" class="main-cover" mode="aspectFill" />
          <!-- 播放指示器 -->
          <view class="play-indicator" v-if="isPlaying">
            <view class="play-icon">
              <fui-icon name="play" color="#fff" size="24" />
            </view>
          </view>
        </view>
        <!-- 标题、作者 -->
        <view class="main-info">
          <text class="main-title">{{ currentContent.title }}</text>
          <text class="main-author">{{ getAuthorName() }}</text>
          <view class="content-meta">
            <view class="content-type-badge" :class="currentContent.content_type">
              {{ getContentTypeLabel() }}
            </view>
            <text class="content-duration">{{ formattedDuration }}</text>
          </view>
        </view>
        <!-- 歌词/简介/正文（可选） -->
        <view class="main-desc" v-if="currentContent.summary || currentContent.lyrics">
          <text>{{ currentContent.summary || currentContent.lyrics }}</text>
        </view>
        <!-- 业务播放器区块（音频/视频/文章） -->
        <view class="player-core">
          <AudioPlayer 
            v-if="isAudioContent"
            :content="currentContent"
            :is-playing="isPlaying"
            :current-time="currentTime"
            :duration="duration"
            :volume="volume"
            @play="togglePlay"
            @seek="handleSeek"
            @volume-change="setVolume"
            @next="playNext"
            @previous="playPrevious"
          />

          <VideoPlayer 
            v-else-if="isVideoContent"
            :content="currentContent"
            :is-playing="isPlaying"
            :current-time="currentTime"
            :duration="duration"
            :volume="volume"
            :fullscreen="videoFullscreen"
            :muted="videoMuted"
            @play="togglePlay"
            @seek="handleSeek"
            @volume-change="setVolume"
            @fullscreen-change="toggleFullscreen"
            @next="playNext"
            @previous="playPrevious"
          />

          <ArticleReader 
            v-else-if="isArticleContent"
            :content="currentContent"
            :is-playing="isPlaying"
            :reading-time="currentTime"
            :estimated-duration="duration"
            :tts-enabled="articleTTSEnabled"
            :scroll-position="articleScrollPosition"
            @play="togglePlay"
            @tts-toggle="toggleTTS"
            @scroll="handleArticleScroll"
            @next="playNext"
            @previous="playPrevious"
          />
        </view>
        <!-- 操作栏/进度条 -->
        <view class="player-controls-full">
          <!-- 复用原有控制栏和进度条 -->
          <slot name="controls">
            <!-- 原有控制栏内容 -->
            <view class="player-controls" :class="{ 'video-mode': isVideoContent }">
              <view class="content-info">
                <image 
                  :src="currentContent.cover_url || currentContent.thumbnail_url" 
                  class="content-thumbnail"
                />
                <view class="content-details">
                  <text class="content-title">{{ currentContent.title }}</text>
                  <text class="content-author">{{ getAuthorName() }}</text>
                  <text class="content-type-label">{{ getContentTypeLabel() }}</text>
                </view>
              </view>

              <view class="playback-controls">
                <fui-icon 
                  name="skip-previous" 
                  :color="canPlayPrevious ? '#4CD964' : '#8d96a0'" 
                  size="20"
                  @click="playPrevious"
                  :class="{ disabled: !canPlayPrevious }"
                />
                
                <view class="play-button" @click="togglePlay">
                  <fui-icon 
                    :name="isPlaying ? 'pause' : 'play'" 
                    color="#fff" 
                    size="24"
                  />
                </view>
                
                <fui-icon 
                  name="skip-next" 
                  :color="canPlayNext ? '#4CD964' : '#8d96a0'" 
                  size="20"
                  @click="playNext"
                  :class="{ disabled: !canPlayNext }"
                />
              </view>

              <view class="additional-controls">
                <!-- 音频/视频特有控制 -->
                <template v-if="isAudioContent || isVideoContent">
                  <fui-icon 
                    :name="shuffleMode ? 'shuffle' : 'swap'" 
                    :color="shuffleMode ? '#4CD964' : '#8d96a0'" 
                    size="18"
                    @click="toggleShuffle"
                  />
                  
                  <fui-icon 
                    :name="getRepeatIcon()" 
                    :color="repeatMode !== 'none' ? '#4CD964' : '#8d96a0'" 
                    size="18"
                    @click="toggleRepeat"
                  />
                </template>

                <!-- 文章特有控制 -->
                <template v-if="isArticleContent">
                  <fui-icon 
                    :name="articleTTSEnabled ? 'volume-up' : 'volume-off'" 
                    :color="articleTTSEnabled ? '#4CD964' : '#8d96a0'" 
                    size="18"
                    @click="toggleTTS"
                  />
                  
                  <fui-icon 
                    name="text-size" 
                    color="#8d96a0" 
                    size="18"
                    @click="showFontSettings"
                  />
                </template>

                <fui-icon 
                  name="more" 
                  color="#8d96a0" 
                  size="18"
                  @click="showMoreActions"
                />
              </view>
            </view>

            <template v-if="!isVideoContent">
              <!-- 进度条 -->
              <view class="progress-container">
                <view class="progress-info">
                  <text class="time-text">{{ formattedCurrentTime }}</text>
                  <text class="time-text">{{ formattedDuration }}</text>
                </view>
                <ProgressBar 
                  :current="currentTime"
                  :total="duration"
                  :buffered="bufferedTime"
                  @seek="handleSeek"
                  class="progress-bar"
                />
              </view>

              <!-- 播放列表快速切换 -->
              <view class="playlist-quick-nav" v-if="playQueue && playQueue.length > 1">
                <scroll-view scroll-x class="playlist-scroll">
                  <view class="playlist-items">
                    <view 
                      v-for="(item, index) in playQueue"
                      :key="item.id"
                      class="playlist-item"
                      :class="{ active: index === currentIndex }"
                      @click="switchToContent(index)"
                    >
                      <image :src="item.cover_url || item.source_url" class="item-thumb" />
                      <text class="item-title">{{ item.title }}</text>
                      <view class="item-type-badge" :class="item.content_type">
                        {{ getContentTypeLabel(item.content_type) }}
                      </view>
                    </view>
                  </view>
                </scroll-view>
              </view>

              <!-- 错误提示 -->
              <view class="error-message" v-if="error">
                <fui-icon name="alert-circle" color="#ff3b30" size="20" />
                <text class="error-text">{{ error }}</text>
                <fui-button type="plain" size="small" @click="retryPlay">重试</fui-button>
              </view>

              <!-- 加载指示器 -->
              <view class="loading-overlay" v-if="isLoading">
                <fui-loading color="#4CD964" />
                <text class="loading-text">加载中...</text>
              </view>
            </template>
          </slot>
        </view>
      </view>
    </template>
  </view>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { usePlayerStore } from '@/store/modules/player'
import AudioPlayer from './AudioPlayer.vue'
import VideoPlayer from './VideoPlayer.vue'
import ArticleReader from './ArticleReader.vue'
import ProgressBar from './ProgressBar.vue'

const playerStore = usePlayerStore()

// 计算属性
const currentContent = computed(() => playerStore.currentContent)
const isPlaying = computed(() => playerStore.isPlaying)
const currentTime = computed(() => playerStore.currentTime)
const duration = computed(() => playerStore.duration)
const bufferedTime = computed(() => playerStore.bufferedTime)
const volume = computed(() => playerStore.volume)
const isAudioContent = computed(() => currentContent.value && currentContent.value.type === 'audio')
const isVideoContent = computed(() => currentContent.value && currentContent.value.type === 'video')
const isArticleContent = computed(() => currentContent.value && currentContent.value.type === 'article')
const videoFullscreen = computed(() => playerStore.videoFullscreen)
const videoMuted = computed(() => playerStore.videoMuted)
const articleTTSEnabled = computed(() => playerStore.articleTTSEnabled)
const articleScrollPosition = computed(() => playerStore.articleScrollPosition)
const canPlayPrevious = computed(() => playerStore.canPlayPrevious)
const canPlayNext = computed(() => playerStore.canPlayNext)
const shuffleMode = computed(() => playerStore.shuffleMode)
const repeatMode = computed(() => playerStore.repeatMode)
const playQueue = computed(() => playerStore.playQueue)
const currentIndex = computed(() => playerStore.currentIndex)
const error = computed(() => playerStore.error)
const isLoading = computed(() => playerStore.isLoading)
const formattedCurrentTime = computed(() => playerStore.formattedCurrentTime)
const formattedDuration = computed(() => playerStore.formattedDuration)

// 方法
const togglePlay = () => {
  playerStore.togglePlay()
}

const handleSeek = (time) => {
  playerStore.seek(time)
}

const setVolume = (volume) => {
  playerStore.setVolume(volume)
}

const playNext = () => {
  playerStore.playNext()
}

const playPrevious = () => {
  playerStore.playPrevious()
}

const toggleShuffle = () => {
  playerStore.toggleShuffle()
}

const toggleRepeat = () => {
  playerStore.toggleRepeat()
}

const toggleTTS = () => {
  playerStore.toggleTTS()
}

const toggleFullscreen = () => {
  playerStore.videoFullscreen = !playerStore.videoFullscreen
}

const handleArticleScroll = (position) => {
  playerStore.seek(position)
}

const switchToContent = (index) => {
  const content = Array.isArray(playQueue.value) ? playQueue.value[index] : undefined
  if (content) {
    playerStore.playContent(content, playerStore.currentPlaylist, index)
  }
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

const getContentTypeLabel = (type = null) => {
  const contentType = type || playerStore.contentType
  switch (contentType) {
    case 'audio': return '音频'
    case 'video': return '视频'
    case 'article': return '文章'
    default: return '内容'
  }
}

const getRepeatIcon = () => {
  switch (repeatMode.value) {
    case 'one': return 'repeat-one'
    case 'all': return 'repeat'
    default: return 'repeat-off'
  }
}

const showFontSettings = () => {
  uni.$emit('show-font-settings')
}

const showMoreActions = () => {
  uni.$emit('show-player-actions', currentContent.value)
}

const retryPlay = () => {
  if (currentContent.value) {
    playerStore.playContent(currentContent.value)
  }
}

// 生命周期
onMounted(() => {
  // 监听系统媒体控制
  const bgm = typeof uni.getBackgroundAudioManager === 'function' ? uni.getBackgroundAudioManager() : null
  if (bgm) {
    bgm.onPlay(() => {
      playerStore.isPlaying = true
    })
    bgm.onPause(() => {
      playerStore.isPlaying = false
    })
    bgm.onStop(() => {
      playerStore.isPlaying = false
      playerStore.currentTime = 0
    })
  }
})

onUnmounted(() => {
  // 清理事件监听
  // 小程序自动解绑，H5/APP如需解绑可在此处补充
})
</script>

<style lang="scss" scoped>
.media-player-fullscreen {
  position: fixed;
  left: 0; right: 0; top: 0; bottom: 0;
  z-index: 3000;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #222;
  overflow: hidden;
}
.player-header {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 120rpx;
  display: flex;
  align-items: center;
  padding: 0 32rpx;
  z-index: 10000;
  background: linear-gradient(180deg, rgba(0,0,0,0.85) 90%, transparent 100%) !important;
}
.player-title {
  color: #fff;
  font-size: 32rpx;
  margin-left: 24rpx;
}
.player-bg {
  position: absolute;
  left: 0; right: 0; top: 0; bottom: 0;
  z-index: 0;
  overflow: hidden;
}
.bg-image {
  width: 100vw;
  height: 100vh;
  filter: blur(32rpx) brightness(0.7);
  object-fit: cover;
}
.bg-mask {
  position: absolute;
  left: 0; right: 0; top: 0; bottom: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0.55) 60%, #222 100%);
}
.player-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 160rpx;
  width: 100%;
  height: 100%;

}
.cover-container {
  position: relative;
  width: 460rpx;
  height: 460rpx;
  margin-bottom: 40rpx;
}

.cover-container.rotating {
  animation: rotate 20s linear infinite;
}

.main-cover {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  box-shadow: 0 16rpx 64rpx rgba(0,0,0,0.4);
  object-fit: cover;
  border: 6rpx solid rgba(255,255,255,0.1);
}

.play-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(20rpx);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 2s infinite ease-in-out;
}

.play-icon {
  padding-left: 6rpx;
}
.main-info {
  text-align: center;
  margin-bottom: 32rpx;
}

.main-title {
  font-size: 36rpx;
  color: #fff;
  font-weight: bold;
  margin-bottom: 12rpx;
  line-height: 1.4;
}

.main-author {
  font-size: 26rpx;
  color: #e0e0e0;
  margin-bottom: 16rpx;
}

.content-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
}

.content-type-badge {
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  font-size: 20rpx;
  color: #fff;
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(10rpx);
  
  &.audio {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  &.video {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  }
  
  &.article {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  }
}

.content-duration {
  font-size: 22rpx;
  color: #ccc;
}
.main-desc {
  color: #e0e0e0;
  font-size: 24rpx;
  margin: 16rpx 0 32rpx;
  text-align: center;
  max-height: 120rpx;
  overflow: auto;
}
.player-core {
  width: 100%;
  margin-bottom: 32rpx;
}
.player-controls-full {
  width: 100%;
  position: absolute;
  left: 0; right: 0; bottom: 0;
  padding-bottom: env(safe-area-inset-bottom);
  z-index: 10;
  background: linear-gradient(180deg, transparent 0%, #222 100%);
}

.fullscreen-btn {
  margin: 24px auto 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 140px;
  height: 48px;
  background: #4f6ef7;
  color: #fff;
  font-size: 20px;
  border-radius: 16px;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(79,110,247,0.12);
  cursor: pointer;
  transition: background 0.2s;
}
.fullscreen-btn:active {
  background: #3a4db7;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
  50% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }
}
</style>