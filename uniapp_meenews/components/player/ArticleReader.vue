<template>
  <view class="article-reader">
    <!-- 文章头部 -->
    <view class="article-header">
      <text class="article-title">{{ content.title }}</text>
      
      <view class="article-meta">
        <view class="author-info">
          <image 
            :src="content.author?.avatar_url" 
            class="author-avatar"
            @error="handleAvatarError"
          />
          <view class="author-details">
            <text class="author-name">{{ content.author?.name || '未知作者' }}</text>
            <text class="publish-info">
              {{ formatPublishTime(content.created_at) }} · 
              {{ estimatedReadTime }}分钟阅读
            </text>
          </view>
        </view>
        
        <view class="article-actions">
          <fui-icon 
            :name="content.is_liked ? 'heart-fill' : 'heart'" 
            :color="content.is_liked ? '#ff3b30' : '#8d96a0'" 
            size="24"
            @click="toggleLike"
          />
          <fui-icon 
            name="bookmark" 
            :color="content.is_bookmarked ? '#4CD964' : '#8d96a0'" 
            size="24"
            @click="toggleBookmark"
          />
          <fui-icon 
            name="share" 
            color="#8d96a0" 
            size="24"
            @click="shareArticle"
          />
        </view>
      </view>

      <!-- 文章标签 -->
      <view class="article-tags" v-if="content.tags && content.tags.length">
        <text 
          v-for="tag in content.tags"
          :key="tag.id"
          class="article-tag"
          @click="searchByTag(tag)"
        >
          #{{ tag.name }}
        </text>
      </view>
    </view>

    <!-- 阅读控制栏 -->
    <view class="reading-controls" :class="{ sticky: controlsSticky }">
      <view class="reading-progress">
        <view class="progress-info">
          <text class="progress-text">阅读进度 {{ readingProgress }}%</text>
          <text class="time-info">已读 {{ formatTime(readingTime) }}</text>
        </view>
        <view class="progress-bar">
          <view 
            class="progress-fill" 
            :style="{ width: `${readingProgress}%` }"
          ></view>
        </view>
      </view>

      <view class="reading-options">
        <!-- TTS控制 -->
        <view class="tts-control">
          <fui-icon 
            :name="ttsEnabled ? 'volume-up' : 'volume-off'" 
            :color="ttsEnabled ? '#4CD964' : '#8d96a0'" 
            size="20"
            @click="toggleTTS"
          />
          <text class="control-label">语音播放</text>
        </view>

        <!-- 字体大小 -->
        <view class="font-control" @click="showFontSettings">
          <fui-icon name="text-size" color="#8d96a0" size="20" />
          <text class="control-label">字体</text>
        </view>

        <!-- 阅读模式 -->
        <view class="theme-control" @click="toggleReadingTheme">
          <fui-icon 
            :name="isDarkMode ? 'sun' : 'moon'" 
            color="#8d96a0" 
            size="20"
          />
          <text class="control-label">{{ isDarkMode ? '日间' : '夜间' }}</text>
        </view>

        <!-- 全屏阅读 -->
        <view class="fullscreen-control" @click="toggleFullscreen">
          <fui-icon 
            :name="isFullscreen ? 'minimize' : 'maximize'" 
            color="#8d96a0" 
            size="20"
          />
          <text class="control-label">全屏</text>
        </view>
      </view>
    </view>

    <!-- 文章内容 -->
    <scroll-view 
      scroll-y 
      class="article-content"
      :class="{ 
        fullscreen: isFullscreen,
        'dark-mode': isDarkMode,
        [`font-size-${fontSize}`]: true,
        [`line-height-${lineHeight}`]: true
      }"
      :scroll-top="scrollTop"
      @scroll="onScroll"
      enhanced
      show-scrollbar
    >
      <view class="content-container" :style="contentStyles">
        <!-- 文章封面 -->
        <image 
          v-if="content.cover_url && showCover"
          :src="content.cover_url"
          class="article-cover"
          mode="aspectFill"
          @error="handleCoverError"
        />

        <!-- 文章摘要 -->
        <view class="article-summary" v-if="content.summary">
          <text class="summary-label">摘要</text>
          <text class="summary-text">{{ content.summary }}</text>
        </view>

        <!-- 富文本内容 -->
        <rich-text 
          :nodes="formattedContent" 
          class="article-body"
          @itemclick="onContentClick"
        ></rich-text>

        <!-- 图片查看器 -->
        <view class="image-gallery" v-if="articleImages.length">
          <text class="gallery-title">相关图片</text>
          <view class="image-grid">
            <image 
              v-for="(img, index) in articleImages"
              :key="index"
              :src="img.src"
              class="gallery-image"
              @click="previewImage(index)"
            />
          </view>
        </view>

        <!-- 引用和链接 -->
        <view class="article-references" v-if="content.references">
          <text class="references-title">参考链接</text>
          <view 
            v-for="ref in content.references"
            :key="ref.id"
            class="reference-item"
            @click="openReference(ref.url)"
          >
            <text class="reference-title">{{ ref.title }}</text>
            <text class="reference-url">{{ ref.url }}</text>
          </view>
        </view>

        <!-- 文章结尾 -->
        <view class="article-footer">
          <text class="footer-text">— 全文完 —</text>
          <view class="reading-stats">
            <text class="stats-text">
              全文共 {{ wordCount }} 字 · 预计阅读时间 {{ estimatedReadTime }} 分钟
            </text>
          </view>
        </view>
      </view>
    </scroll-view>

    <!-- TTS播放控制 -->
    <view class="tts-player" v-if="ttsEnabled && ttsStatus.audioUrl">
      <view class="tts-controls">
        <fui-icon 
          :name="isPlaying ? 'pause' : 'play'" 
          color="#4CD964" 
          size="24"
          @click="toggleTTSPlay"
        />
        
        <view class="tts-progress">
          <text class="tts-text">{{ currentTTSText }}</text>
          <view class="tts-progress-bar">
            <view 
              class="tts-progress-fill"
              :style="{ width: `${ttsProgress}%` }"
            ></view>
          </view>
        </view>

        <view class="tts-speed">
          <text class="speed-label">{{ ttsSpeed }}x</text>
        </view>
      </view>
    </view>

    <!-- 字体设置弹窗 -->
    <fui-bottom-popup v-model:visible="showFontPanel">
      <view class="font-settings">
        <text class="settings-title">阅读设置</text>
        
        <!-- 字体大小 -->
        <view class="setting-group">
          <text class="setting-label">字体大小</text>
          <view class="font-size-options">
            <text 
              v-for="size in fontSizeOptions"
              :key="size.value"
              class="size-option"
              :class="{ active: fontSize === size.value }"
              @click="setFontSize(size.value)"
            >
              {{ size.label }}
            </text>
          </view>
        </view>

        <!-- 行间距 -->
        <view class="setting-group">
          <text class="setting-label">行间距</text>
          <view class="line-height-options">
            <text 
              v-for="height in lineHeightOptions"
              :key="height.value"
              class="height-option"
              :class="{ active: lineHeight === height.value }"
              @click="setLineHeight(height.value)"
            >
              {{ height.label }}
            </text>
          </view>
        </view>

        <!-- 阅读主题 -->
        <view class="setting-group">
          <text class="setting-label">阅读主题</text>
          <view class="theme-options">
            <view 
              v-for="theme in themeOptions"
              :key="theme.value"
              class="theme-option"
              :class="{ active: currentTheme === theme.value }"
              :style="{ backgroundColor: theme.bg, color: theme.color }"
              @click="setTheme(theme.value)"
            >
              {{ theme.label }}
            </view>
          </view>
        </view>

        <!-- TTS设置 -->
        <view class="setting-group">
          <text class="setting-label">语音播放</text>
          <view class="tts-settings">
            <view class="tts-voice">
              <text class="voice-label">声音</text>
              <picker 
                :range="voiceOptions" 
                range-key="name"
                @change="onVoiceChange"
              >
                <text class="voice-picker">{{ currentVoice.name }}</text>
              </picker>
            </view>
            
            <view class="tts-speed-control">
              <text class="speed-label">语速</text>
              <slider 
                :value="ttsSpeed * 100"
                min="50"
                max="200"
                @change="onTTSSpeedChange"
                class="speed-slider"
              />
              <text class="speed-value">{{ ttsSpeed }}x</text>
            </view>
          </view>
        </view>
      </view>
    </fui-bottom-popup>

    <!-- 目录导航 -->
    <fui-bottom-popup v-model:visible="showTableOfContents">
      <view class="table-of-contents">
        <text class="toc-title">目录</text>
        <scroll-view scroll-y class="toc-list">
          <view 
            v-for="heading in tableOfContents"
            :key="heading.id"
            class="toc-item"
            :class="[`level-${heading.level}`, { active: heading.id === currentHeading }]"
            @click="scrollToHeading(heading)"
          >
            <text class="toc-text">{{ heading.text }}</text>
          </view>
        </scroll-view>
      </view>
    </fui-bottom-popup>
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
  readingTime: {
    type: Number,
    default: 0
  },
  estimatedDuration: {
    type: Number,
    default: 0
  },
  ttsEnabled: {
    type: Boolean,
    default: false
  },
  scrollPosition: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits([
  'play', 'tts-toggle', 'scroll', 'next', 'previous'
])

// 数据
const controlsSticky = ref(false)
const scrollTop = ref(0)
const readingProgress = ref(0)
const isFullscreen = ref(false)
const isDarkMode = ref(false)
const currentTheme = ref('light')
const fontSize = ref('medium')
const lineHeight = ref('normal')
const showCover = ref(true)
const showFontPanel = ref(false)
const showTableOfContents = ref(false)

// TTS相关
const ttsStatus = ref({
  audioUrl: null,
  duration: 0,
  currentTime: 0
})
const currentTTSText = ref('')
const ttsProgress = ref(0)
const ttsSpeed = ref(1.0)
const currentVoice = ref({ name: '小云', value: 'xiaoyun' })

// 文章解析
const articleImages = ref([])
const tableOfContents = ref([])
const currentHeading = ref('')

// 设置选项
const fontSizeOptions = [
  { label: '小', value: 'small' },
  { label: '中', value: 'medium' },
  { label: '大', value: 'large' },
  { label: '超大', value: 'xlarge' }
]

const lineHeightOptions = [
  { label: '紧凑', value: 'compact' },
  { label: '标准', value: 'normal' },
  { label: '宽松', value: 'loose' }
]

const themeOptions = [
  { label: '日间', value: 'light', bg: '#ffffff', color: '#2c3038' },
  { label: '夜间', value: 'dark', bg: '#1a1a1a', color: '#ffffff' },
  { label: '护眼', value: 'sepia', bg: '#f5f1e8', color: '#5c4a37' },
  { label: '粉色', value: 'pink', bg: '#fdf2f8', color: '#831843' }
]

const voiceOptions = [
  { name: '小云', value: 'xiaoyun' },
  { name: '小明', value: 'xiaoming' },
  { name: '小美', value: 'xiaomei' },
  { name: '小强', value: 'xiaoqiang' }
]

// 计算属性
const wordCount = computed(() => {
  const content = props.content.article_content || props.content.text_content || ''
  return content.length
})

const estimatedReadTime = computed(() => {
  return Math.ceil(wordCount.value / 250) // 假设每分钟250字
})

const formattedContent = computed(() => {
  let content = props.content.article_content || props.content.text_content || ''
  
  // 解析HTML内容
  content = content.replace(/\n/g, '<br/>')
  
  // 提取图片
  const imgRegex = /<img[^>]+src="([^"]+)"[^>]*>/g
  let match
  const images = []
  while ((match = imgRegex.exec(content)) !== null) {
    images.push({ src: match[1] })
  }
  articleImages.value = images
  
  // 提取标题生成目录
  const headingRegex = /<h([1-6])[^>]*>(.*?)<\/h[1-6]>/g
  const headings = []
  while ((match = headingRegex.exec(content)) !== null) {
    headings.push({
      id: `heading-${headings.length}`,
      level: parseInt(match[1]),
      text: match[2].replace(/<[^>]*>/g, '')
    })
  }
  tableOfContents.value = headings
  
  return content
})

const contentStyles = computed(() => {
  const theme = themeOptions.find(t => t.value === currentTheme.value)
  return {
    backgroundColor: theme?.bg || '#ffffff',
    color: theme?.color || '#2c3038'
  }
})

// 方法
const toggleTTS = () => {
  emit('tts-toggle')
}

const toggleTTSPlay = () => {
  emit('play')
}

const toggleLike = async () => {
  try {
    await api.content.toggleLike(props.content.id)
    props.content.is_liked = !props.content.is_liked
  } catch (error) {
    uni.showToast({
      title: '操作失败',
      icon: 'error'
    })
  }
}

const toggleBookmark = async () => {
  try {
    await api.content.toggleBookmark(props.content.id)
    props.content.is_bookmarked = !props.content.is_bookmarked
  } catch (error) {
    uni.showToast({
      title: '操作失败',
      icon: 'error'
    })
  }
}

const shareArticle = () => {
  uni.share({
    provider: 'weixin',
    scene: 'WXSceneTimeline',
    type: 0,
    title: props.content.title,
    summary: props.content.summary || props.content.description,
    href: `https://app.yangmie.com/article/${props.content.id}`
  })
}

const searchByTag = (tag) => {
  uni.navigateTo({
    url: `/pages/discover/search?q=${encodeURIComponent(tag.name)}&type=article`
  })
}

const onScroll = (e) => {
  scrollTop.value = e.detail.scrollTop
  
  // 计算阅读进度
  const scrollHeight = e.detail.scrollHeight
  const clientHeight = e.detail.height
  const progress = (scrollTop.value / (scrollHeight - clientHeight)) * 100
  readingProgress.value = Math.min(100, Math.max(0, progress))
  
  // 控制栏粘性
  controlsSticky.value = scrollTop.value > 200
  
  emit('scroll', scrollTop.value)
}

const showFontSettings = () => {
  showFontPanel.value = true
}

const toggleReadingTheme = () => {
  isDarkMode.value = !isDarkMode.value
  currentTheme.value = isDarkMode.value ? 'dark' : 'light'
}

const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value
}

const setFontSize = (size) => {
  fontSize.value = size
  saveReadingSettings()
}

const setLineHeight = (height) => {
  lineHeight.value = height
  saveReadingSettings()
}

const setTheme = (theme) => {
  currentTheme.value = theme
  isDarkMode.value = theme === 'dark'
  saveReadingSettings()
}

const onVoiceChange = (e) => {
  currentVoice.value = voiceOptions[e.detail.value]
}

const onTTSSpeedChange = (e) => {
  ttsSpeed.value = e.detail.value / 100
}

const scrollToHeading = (heading) => {
  // 滚动到指定标题
  const element = document.getElementById(heading.id)
  if (element) {
    scrollTop.value = element.offsetTop
  }
  showTableOfContents.value = false
}

const onContentClick = (e) => {
  // 处理富文本内容点击
  if (e.detail.node.name === 'img') {
    const src = e.detail.node.attrs.src
    previewImage(src)
  }
}

const previewImage = (indexOrSrc) => {
  let urls, current
  
  if (typeof indexOrSrc === 'number') {
    urls = articleImages.value.map(img => img.src)
    current = indexOrSrc
  } else {
    urls = [indexOrSrc]
    current = 0
  }
  
  uni.previewImage({
    urls,
    current
  })
}

const openReference = (url) => {
  uni.setClipboardData({
    data: url,
    success: () => {
      uni.showToast({
        title: '链接已复制',
        icon: 'success'
      })
    }
  })
}

const handleAvatarError = () => {
  // 头像加载失败处理
}

const handleCoverError = () => {
  showCover.value = false
}

const formatPublishTime = (time) => {
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  
  if (diff < 24 * 60 * 60 * 1000) {
    return '今天'
  } else if (diff < 2 * 24 * 60 * 60 * 1000) {
    return '昨天'
  } else {
    return date.toLocaleDateString()
  }
}

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const saveReadingSettings = () => {
  const settings = {
    fontSize: fontSize.value,
    lineHeight: lineHeight.value,
    theme: currentTheme.value
  }
  uni.setStorageSync('reading_settings', settings)
}

const loadReadingSettings = () => {
  try {
    const settings = uni.getStorageSync('reading_settings')
    if (settings) {
      fontSize.value = settings.fontSize || 'medium'
      lineHeight.value = settings.lineHeight || 'normal'
      currentTheme.value = settings.theme || 'light'
      isDarkMode.value = currentTheme.value === 'dark'
    }
  } catch (error) {
    console.error('加载阅读设置失败:', error)
  }
}

// 监听器
watch(() => props.scrollPosition, (newPos) => {
  scrollTop.value = newPos
})

// 生命周期
onMounted(() => {
  loadReadingSettings()
})
</script>

<style lang="scss" scoped>
.article-reader {
  min-height: 100vh;
  background: #ffffff;
  
  &.fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 9999;
  }
}

.article-header {
  padding: 32rpx;
  border-bottom: 1px solid #eaedf0;
}

.article-title {
  display: block;
  font-size: 48rpx;
  font-weight: 700;
  color: #2c3038;
  line-height: 1.4;
  margin-bottom: 24rpx;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.author-avatar {
  width: 60rpx;
  height: 60rpx;
  border-radius: 30rpx;
}

.author-details {
  flex: 1;
}

.author-name {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: #2c3038;
  margin-bottom: 4rpx;
}

.publish-info {
  display: block;
  font-size: 24rpx;
  color: #8d96a0;
}

.article-actions {
  display: flex;
  gap: 24rpx;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.article-tag {
  font-size: 24rpx;
  color: #4CD964;
  background: rgba(76, 217, 100, 0.1);
  padding: 8rpx 16rpx;
  border-radius: 16rpx;
  border: 1px solid rgba(76, 217, 100, 0.3);
}

.reading-controls {
  padding: 24rpx 32rpx;
  background: #ffffff;
  border-bottom: 1px solid #eaedf0;
  
  &.sticky {
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
  }
}

.reading-progress {
  margin-bottom: 16rpx;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8rpx;
}

.progress-text,
.time-info {
  font-size: 24rpx;
  color: #8d96a0;
}

.progress-bar {
  height: 4rpx;
  background: #eaedf0;
  border-radius: 2rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #4CD964;
  transition: width 0.3s ease;
}

.reading-options {
  display: flex;
  gap: 32rpx;
}

.tts-control,
.font-control,
.theme-control,
.fullscreen-control {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.control-label {
  font-size: 20rpx;
  color: #8d96a0;
}

.article-content {
  flex: 1;
  
  &.fullscreen {
    height: 100vh;
  }
  
  &.dark-mode {
    background: #1a1a1a;
    color: #ffffff;
  }
  
  &.font-size-small .article-body {
    font-size: 28rpx;
  }
  
  &.font-size-medium .article-body {
    font-size: 32rpx;
  }
  
  &.font-size-large .article-body {
    font-size: 36rpx;
  }
  
  &.font-size-xlarge .article-body {
    font-size: 40rpx;
  }
  
  &.line-height-compact .article-body {
    line-height: 1.4;
  }
  
  &.line-height-normal .article-body {
    line-height: 1.6;
  }
  
  &.line-height-loose .article-body {
    line-height: 1.8;
  }
}

.content-container {
  padding: 32rpx;
  min-height: 100%;
}

.article-cover {
  width: 100%;
  height: 400rpx;
  border-radius: 12rpx;
  margin-bottom: 32rpx;
}

.article-summary {
  background: rgba(76, 217, 100, 0.05);
  border-left: 4rpx solid #4CD964;
  padding: 24rpx;
  margin-bottom: 32rpx;
  border-radius: 0 8rpx 8rpx 0;
}

.summary-label {
  display: block;
  font-size: 24rpx;
  font-weight: 600;
  color: #4CD964;
  margin-bottom: 12rpx;
}

.summary-text {
  font-size: 28rpx;
  color: #5c6873;
  line-height: 1.6;
}

.article-body {
  font-size: 32rpx;
  line-height: 1.6;
  color: #2c3038;
  margin-bottom: 48rpx;
}

.image-gallery {
  margin: 48rpx 0;
}

.gallery-title {
  display: block;
  font-size: 32rpx;
  font-weight: 600;
  color: #2c3038;
  margin-bottom: 24rpx;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200rpx, 1fr));
  gap: 16rpx;
}

.gallery-image {
  width: 100%;
  height: 200rpx;
  border-radius: 8rpx;
  object-fit: cover;
}

.article-references {
  margin: 48rpx 0;
  padding-top: 24rpx;
  border-top: 1px solid #eaedf0;
}

.references-title {
  display: block;
  font-size: 32rpx;
  font-weight: 600;
  color: #2c3038;
  margin-bottom: 24rpx;
}

.reference-item {
  padding: 16rpx;
  background: #f8f9fa;
  border-radius: 8rpx;
  margin-bottom: 12rpx;
}

.reference-title {
  display: block;
  font-size: 28rpx;
  color: #4CD964;
  margin-bottom: 8rpx;
}

.reference-url {
  font-size: 24rpx;
  color: #8d96a0;
}

.article-footer {
  text-align: center;
  padding: 48rpx 0;
  border-top: 1px solid #eaedf0;
}

.footer-text {
  font-size: 28rpx;
  color: #8d96a0;
  margin-bottom: 16rpx;
}

.reading-stats {
  margin-top: 24rpx;
}

.stats-text {
  font-size: 24rpx;
  color: #8d96a0;
}

.tts-player {
  position: fixed;
  bottom: 100rpx;
  left: 32rpx;
  right: 32rpx;
  background: #ffffff;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.tts-controls {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.tts-progress {
  flex: 1;
  min-width: 0;
}

.tts-text {
  display: block;
  font-size: 24rpx;
  color: #2c3038;
  margin-bottom: 8rpx;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tts-progress-bar {
  height: 4rpx;
  background: #eaedf0;
  border-radius: 2rpx;
  overflow: hidden;
}

.tts-progress-fill {
  height: 100%;
  background: #4CD964;
  transition: width 0.3s ease;
}

.tts-speed {
  min-width: 60rpx;
  text-align: center;
}

.speed-label {
  font-size: 24rpx;
  color: #8d96a0;
}

.font-settings {
  padding: 32rpx;
  background: #ffffff;
  border-radius: 24rpx 24rpx 0 0;
  max-height: 80vh;
}

.settings-title {
  display: block;
  font-size: 36rpx;
  font-weight: 600;
  color: #2c3038;
  margin-bottom: 32rpx;
  text-align: center;
}

.setting-group {
  margin-bottom: 32rpx;
}

.setting-label {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: #2c3038;
  margin-bottom: 16rpx;
}

.font-size-options,
.line-height-options {
  display: flex;
  gap: 16rpx;
}

.size-option,
.height-option {
  flex: 1;
  text-align: center;
  padding: 16rpx;
  background: #f8f9fa;
  border-radius: 8rpx;
  font-size: 28rpx;
  color: #2c3038;
  
  &.active {
    background: #4CD964;
    color: #ffffff;
  }
}

.theme-options {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16rpx;
}

.theme-option {
  padding: 24rpx;
  border-radius: 12rpx;
  text-align: center;
  font-size: 28rpx;
  border: 2px solid transparent;
  
  &.active {
    border-color: #4CD964;
  }
}

.table-of-contents {
  padding: 32rpx;
  background: #ffffff;
  border-radius: 24rpx 24rpx 0 0;
  max-height: 70vh;
}

.toc-title {
  display: block;
  font-size: 36rpx;
  font-weight: 600;
  color: #2c3038;
  margin-bottom: 24rpx;
  text-align: center;
}

.toc-list {
  max-height: 500rpx;
}

.toc-item {
  padding: 16rpx 0;
  border-bottom: 1px solid #f0f0f0;
  
  &.level-1 {
    font-weight: 600;
    padding-left: 0;
  }
  
  &.level-2 {
    padding-left: 32rpx;
  }
  
  &.level-3 {
    padding-left: 64rpx;
  }
  
  &.active {
    color: #4CD964;
  }
}

.toc-text {
  font-size: 28rpx;
  color: #2c3038;
}
</style>