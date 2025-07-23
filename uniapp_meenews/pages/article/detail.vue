<template>
  <view class="article-detail-page">
    <!-- 顶部导航栏 -->
    <NavBar :title="article?.title || '文章详情'" :show-back="true">
      <template #right>
        <view class="nav-actions">
          <fui-icon 
            name="share" 
            color="#333" 
            size="24" 
            @click="shareArticle"
          />
          <fui-icon 
            name="more" 
            color="#333" 
            size="24" 
            @click="showMoreActions"
            style="margin-left: 16rpx;"
          />
        </view>
      </template>
    </NavBar>

    <!-- 加载状态 -->
    <view v-if="isLoading" class="loading-container">
      <fui-loading color="#4CD964" />
      <text class="loading-text">加载中...</text>
    </view>

    <!-- 错误状态 -->
    <view v-else-if="error" class="error-container">
      <fui-icon name="alert-circle" color="#ff3b30" size="48" />
      <text class="error-title">加载失败</text>
      <text class="error-message">{{ error }}</text>
      <fui-button type="primary" @click="retryLoad">重试</fui-button>
    </view>

    <!-- 文章内容 -->
    <view v-else-if="article" class="article-content">
      <!-- 文章头部信息 -->
      <view class="article-header">
        <view class="article-meta">
          <view class="content-type-badge article">
            <fui-icon name="document" color="#fff" size="14" />
            <text>文章</text>
          </view>
          <text class="publish-time">{{ formatTime(article.published_at) }}</text>
          <text class="read-count">{{ formatNumber(article.view_count) }} 次阅读</text>
        </view>
        
        <text class="article-title">{{ article.title }}</text>
        
        <view class="article-summary" v-if="article.summary">
          <text>{{ article.summary }}</text>
        </view>

        <!-- 作者信息 -->
        <view class="author-info" v-if="article.author">
          <image 
            :src="article.author.avatar_url || '/static/images/common/img_logo.png'" 
            class="author-avatar"
          />
          <view class="author-details">
            <text class="author-name">{{ article.author.name }}</text>
            <text class="author-desc">{{ article.author.description || '暂无简介' }}</text>
          </view>
          <FollowButton 
            :is-following="article.author.is_following"
            @follow="handleFollow"
            @unfollow="handleUnfollow"
          />
        </view>

        <!-- TTS 控制栏 -->
        <view class="tts-controls" v-if="supportTTS">
          <view class="tts-info">
            <fui-icon 
              :name="isTTSPlaying ? 'volume-up' : 'volume-off'" 
              :color="isTTSPlaying ? '#4CD964' : '#8d96a0'" 
              size="20"
            />
            <text class="tts-label">{{ isTTSPlaying ? '正在朗读' : 'AI 朗读' }}</text>
            <text class="tts-duration" v-if="ttsDuration">
              {{ formatDuration(ttsCurrentTime) }} / {{ formatDuration(ttsDuration) }}
            </text>
          </view>
          <view class="tts-actions">
            <fui-icon 
              name="skip-previous" 
              color="#8d96a0" 
              size="18"
              @click="ttsPrevious"
              :class="{ disabled: !canTTSPrevious }"
            />
            <view class="tts-play-button" @click="toggleTTS">
              <fui-icon 
                :name="isTTSPlaying ? 'pause' : 'play'" 
                color="#fff" 
                size="16"
              />
            </view>
            <fui-icon 
              name="skip-next" 
              color="#8d96a0" 
              size="18"
              @click="ttsNext"
              :class="{ disabled: !canTTSNext }"
            />
            <fui-icon 
              name="settings" 
              color="#8d96a0" 
              size="18"
              @click="showTTSSettings"
              style="margin-left: 16rpx;"
            />
          </view>
        </view>

        <!-- 进度条 -->
        <view class="reading-progress" v-if="isTTSPlaying">
          <ProgressBar 
            :current="ttsCurrentTime"
            :total="ttsDuration"
            @seek="seekTTS"
            :show-thumb="true"
          />
        </view>
      </view>

      <!-- 文章正文 -->
      <view class="article-body" :class="{ 'tts-highlight': isTTSPlaying }">
        <rich-text 
          :nodes="processedContent" 
          class="article-text"
          :style="{ fontSize: fontSize + 'rpx', lineHeight: lineHeight }"
        ></rich-text>
      </view>

      <!-- 相关推荐 -->
      <view class="related-section" v-if="relatedArticles.length">
        <ContentSection title="相关推荐" :show-more="false">
          <view class="related-list">
            <ContentCard 
              v-for="item in relatedArticles"
              :key="item.id"
              :content="item"
              cardType="list"
              @click="goToArticle(item.id)"
            />
          </view>
        </ContentSection>
      </view>

      <!-- 评论区域 -->
      <view class="comments-section" v-if="showComments">
        <ContentSection title="评论" :show-more="false">
          <view class="comments-list">
            <!-- TODO: 实现评论组件 -->
            <text class="coming-soon">评论功能即将上线</text>
          </view>
        </ContentSection>
      </view>
    </view>

    <!-- 底部操作栏 -->
    <view class="bottom-actions" v-if="article">
      <view class="action-item" @click="toggleLike">
        <fui-icon 
          :name="article.is_liked ? 'heart-fill' : 'heart'" 
          :color="article.is_liked ? '#ff3b30' : '#8d96a0'" 
          size="24"
        />
        <text :class="{ liked: article.is_liked }">
          {{ formatNumber(article.like_count) }}
        </text>
      </view>
      
      <view class="action-item" @click="toggleBookmark">
        <fui-icon 
          :name="article.is_bookmarked ? 'bookmark-fill' : 'bookmark'" 
          :color="article.is_bookmarked ? '#4CD964' : '#8d96a0'" 
          size="24"
        />
        <text :class="{ bookmarked: article.is_bookmarked }">收藏</text>
      </view>
      
      <view class="action-item" @click="shareArticle">
        <fui-icon name="share" color="#8d96a0" size="24" />
        <text>分享</text>
      </view>
      
      <view class="action-item" @click="showCommentInput">
        <fui-icon name="message" color="#8d96a0" size="24" />
        <text>{{ formatNumber(article.comment_count) }}</text>
      </view>
    </view>

    <!-- TTS 设置弹窗 -->
    <fui-bottom-popup 
      v-model:visible="showTTSModal"
      title="朗读设置"
      :mask-close="true"
    >
      <view class="tts-settings">
        <view class="setting-item">
          <text class="setting-label">语音</text>
          <picker 
            :value="ttsVoiceIndex" 
            :range="ttsVoices" 
            range-key="name"
            @change="changeTTSVoice"
          >
            <view class="setting-value">
              {{ ttsVoices[ttsVoiceIndex]?.name || '默认' }}
            </view>
          </picker>
        </view>
        
        <view class="setting-item">
          <text class="setting-label">语速</text>
          <slider 
            :value="ttsSpeed" 
            :min="0.5" 
            :max="2" 
            :step="0.1"
            @change="changeTTSSpeed"
            active-color="#4CD964"
          />
          <text class="setting-value">{{ ttsSpeed }}x</text>
        </view>
        
        <view class="setting-item">
          <text class="setting-label">音量</text>
          <slider 
            :value="ttsVolume" 
            :min="0" 
            :max="1" 
            :step="0.1"
            @change="changeTTSVolume"
            active-color="#4CD964"
          />
          <text class="setting-value">{{ Math.round(ttsVolume * 100) }}%</text>
        </view>
      </view>
    </fui-bottom-popup>
  </view>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { useContentStore } from '@/store/content'
import { usePlayerStore } from '@/store/player'
import { useUserStore } from '@/store/user'
import NavBar from '@/components/common/NavBar.vue'
import ContentSection from '@/components/content/ContentSection.vue'
import ContentCard from '@/components/content/ContentCard.vue'
import FollowButton from '@/components/user/FollowButton.vue'
import ProgressBar from '@/components/player/ProgressBar.vue'
import { getArticleDetail, getRelatedArticles, likeContent, bookmarkContent, followUser } from '@/api/content'
import { formatTime, formatNumber, formatDuration } from '@/utils/format'
import { createTTSPlayer } from '@/utils/tts'

// Store 实例
const contentStore = useContentStore()
const playerStore = usePlayerStore()
const userStore = useUserStore()

// 响应式数据
const articleId = ref('')
const article = ref(null)
const relatedArticles = ref([])
const isLoading = ref(false)
const error = ref('')

// TTS 相关状态
const supportTTS = ref(true)
const isTTSPlaying = ref(false)
const ttsCurrentTime = ref(0)
const ttsDuration = ref(0)
const ttsPlayer = ref(null)
const showTTSModal = ref(false)
const ttsVoiceIndex = ref(0)
const ttsSpeed = ref(1.0)
const ttsVolume = ref(0.8)

// 阅读设置
const fontSize = ref(32) // rpx
const lineHeight = ref(1.6)

// UI 状态
const showComments = ref(false)

// TTS 语音选项
const ttsVoices = ref([
  { id: 'xiaoyun', name: '小云（女声）', gender: 'female' },
  { id: 'xiaogang', name: '小刚（男声）', gender: 'male' },
  { id: 'xiaomei', name: '小美（女声）', gender: 'female' },
  { id: 'xiaoli', name: '小李（男声）', gender: 'male' }
])

// 计算属性
const processedContent = computed(() => {
  if (!article.value?.content) return ''
  
  // 处理富文本内容，添加段落标记用于 TTS 分段
  let content = article.value.content
  
  // 基本的 HTML 清理和格式化
  content = content
    .replace(/<script[^>]*>.*?<\/script>/gi, '') // 移除脚本
    .replace(/<style[^>]*>.*?<\/style>/gi, '') // 移除样式
    .replace(/<iframe[^>]*>.*?<\/iframe>/gi, '') // 移除 iframe
    .replace(/\n\s*\n/g, '\n') // 合并多个换行
  
  return content
})

const canTTSPrevious = computed(() => {
  return ttsPlayer.value?.canPrevious() || false
})

const canTTSNext = computed(() => {
  return ttsPlayer.value?.canNext() || false
})

// 页面加载
onLoad((options) => {
  if (options.id) {
    articleId.value = options.id
    loadArticleDetail()
  } else {
    error.value = '缺少文章ID参数'
  }
})

onShow(() => {
  // 页面显示时更新阅读记录
  if (article.value) {
    recordReadHistory()
  }
})

// 监听器
watch(() => article.value?.content, (newContent) => {
  if (newContent && supportTTS.value) {
    initTTSPlayer()
  }
})

// 主要方法
/**
 * 加载文章详情
 */
const loadArticleDetail = async () => {
  try {
    isLoading.value = true
    error.value = ''
    
    const response = await getArticleDetail(articleId.value)
    
    if (!response || !response.data) {
      throw new Error('文章数据为空')
    }
    
    article.value = response.data
    
    // 验证文章内容类型
    if (article.value.content_type !== 'article') {
      console.warn('Content type mismatch:', article.value.content_type)
    }
    
    // 加载相关文章
    loadRelatedArticles()
    
    // 记录浏览历史
    recordViewHistory()
    
  } catch (err) {
    console.error('Failed to load article:', err)
    error.value = err.message || '加载文章失败'
  } finally {
    isLoading.value = false
  }
}

/**
 * 加载相关文章
 */
const loadRelatedArticles = async () => {
  try {
    const response = await getRelatedArticles(articleId.value, {
      limit: 5,
      exclude_current: true
    })
    
    if (response?.data) {
      relatedArticles.value = response.data.filter(item => 
        item && item.id && item.content_type === 'article'
      )
    }
  } catch (err) {
    console.error('Failed to load related articles:', err)
    // 相关文章加载失败不影响主要功能
  }
}

/**
 * 重试加载
 */
const retryLoad = () => {
  if (articleId.value) {
    loadArticleDetail()
  }
}

/**
 * 初始化 TTS 播放器
 */
const initTTSPlayer = async () => {
  try {
    if (!article.value?.content) return
    
    // 提取纯文本内容用于 TTS
    const textContent = extractTextContent(article.value.content)
    
    if (!textContent.trim()) {
      supportTTS.value = false
      return
    }
    
    // 创建 TTS 播放器实例
    ttsPlayer.value = await createTTSPlayer({
      text: textContent,
      voice: ttsVoices.value[ttsVoiceIndex.value]?.id || 'xiaoyun',
      speed: ttsSpeed.value,
      volume: ttsVolume.value,
      onTimeUpdate: (currentTime, duration) => {
        ttsCurrentTime.value = currentTime
        ttsDuration.value = duration
      },
      onPlay: () => {
        isTTSPlaying.value = true
      },
      onPause: () => {
        isTTSPlaying.value = false
      },
      onEnd: () => {
        isTTSPlaying.value = false
        ttsCurrentTime.value = 0
      },
      onError: (error) => {
        console.error('TTS Error:', error)
        uni.showToast({
          title: 'TTS播放失败',
          icon: 'error'
        })
        isTTSPlaying.value = false
      }
    })
    
  } catch (err) {
    console.error('Failed to init TTS:', err)
    supportTTS.value = false
  }
}

/**
 * 提取文本内容
 */
const extractTextContent = (htmlContent) => {
  if (!htmlContent) return ''
  
  // 移除 HTML 标签，保留文本内容
  return htmlContent
    .replace(/<[^>]*>/g, '') // 移除所有 HTML 标签
    .replace(/&nbsp;/g, ' ') // 替换 HTML 实体
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/\s+/g, ' ') // 合并多个空格
    .trim()
}

// TTS 控制方法
const toggleTTS = () => {
  if (!ttsPlayer.value) {
    initTTSPlayer().then(() => {
      if (ttsPlayer.value) {
        ttsPlayer.value.play()
      }
    })
    return
  }
  
  if (isTTSPlaying.value) {
    ttsPlayer.value.pause()
  } else {
    ttsPlayer.value.play()
  }
}

const ttsPrevious = () => {
  if (ttsPlayer.value?.canPrevious()) {
    ttsPlayer.value.previous()
  }
}

const ttsNext = () => {
  if (ttsPlayer.value?.canNext()) {
    ttsPlayer.value.next()
  }
}

const seekTTS = (time) => {
  if (ttsPlayer.value) {
    ttsPlayer.value.seek(time)
  }
}

const showTTSSettings = () => {
  showTTSModal.value = true
}

const changeTTSVoice = (e) => {
  ttsVoiceIndex.value = e.detail.value
  if (ttsPlayer.value) {
    ttsPlayer.value.setVoice(ttsVoices.value[ttsVoiceIndex.value]?.id)
  }
}

const changeTTSSpeed = (e) => {
  ttsSpeed.value = e.detail.value
  if (ttsPlayer.value) {
    ttsPlayer.value.setSpeed(ttsSpeed.value)
  }
}

const changeTTSVolume = (e) => {
  ttsVolume.value = e.detail.value
  if (ttsPlayer.value) {
    ttsPlayer.value.setVolume(ttsVolume.value)
  }
}

// 互动操作
const toggleLike = async () => {
  try {
    if (!article.value) return
    
    const newLikedState = !article.value.is_liked
    const response = await likeContent(article.value.id, newLikedState)
    
    if (response?.success) {
      article.value.is_liked = newLikedState
      article.value.like_count += newLikedState ? 1 : -1
      
      uni.showToast({
        title: newLikedState ? '已点赞' : '已取消点赞',
        icon: 'success'
      })
    }
  } catch (err) {
    console.error('Failed to toggle like:', err)
    uni.showToast({
      title: '操作失败',
      icon: 'error'
    })
  }
}

const toggleBookmark = async () => {
  try {
    if (!article.value) return
    
    const newBookmarkedState = !article.value.is_bookmarked
    const response = await bookmarkContent(article.value.id, newBookmarkedState)
    
    if (response?.success) {
      article.value.is_bookmarked = newBookmarkedState
      
      uni.showToast({
        title: newBookmarkedState ? '已收藏' : '已取消收藏',
        icon: 'success'
      })
    }
  } catch (err) {
    console.error('Failed to toggle bookmark:', err)
    uni.showToast({
      title: '操作失败',
      icon: 'error'
    })
  }
}

const handleFollow = async () => {
  try {
    if (!article.value?.author) return
    
    const response = await followUser(article.value.author.id, true)
    
    if (response?.success) {
      article.value.author.is_following = true
      
      uni.showToast({
        title: '已关注',
        icon: 'success'
      })
    }
  } catch (err) {
    console.error('Failed to follow user:', err)
    uni.showToast({
      title: '关注失败',
      icon: 'error'
    })
  }
}

const handleUnfollow = async () => {
  try {
    if (!article.value?.author) return
    
    const response = await followUser(article.value.author.id, false)
    
    if (response?.success) {
      article.value.author.is_following = false
      
      uni.showToast({
        title: '已取消关注',
        icon: 'success'
      })
    }
  } catch (err) {
    console.error('Failed to unfollow user:', err)
    uni.showToast({
      title: '取消关注失败',
      icon: 'error'
    })
  }
}

// 导航方法
const goToArticle = (id) => {
  if (!id || id === articleId.value) return
  
  uni.navigateTo({
    url: `/pages/article/detail?id=${id}`
  })
}

const shareArticle = () => {
  if (!article.value) return
  
  uni.share({
    provider: 'weixin',
    scene: 'WXSceneSession',
    type: 0,
    href: `${getBaseUrl()}/article/${article.value.id}`,
    title: article.value.title,
    summary: article.value.summary || '来自羊咩快报的精彩文章',
    imageUrl: article.value.cover_url || '/static/images/common/img_logo.png',
    success: () => {
      uni.showToast({
        title: '分享成功',
        icon: 'success'
      })
    },
    fail: (err) => {
      console.error('Share failed:', err)
      // 降级到复制链接
      uni.setClipboardData({
        data: `${article.value.title} ${getBaseUrl()}/article/${article.value.id}`,
        success: () => {
          uni.showToast({
            title: '链接已复制',
            icon: 'success'
          })
        }
      })
    }
  })
}

const showMoreActions = () => {
  const actions = ['举报', '不感兴趣', '字体设置']
  
  uni.showActionSheet({
    itemList: actions,
    success: (res) => {
      const action = actions[res.tapIndex]
      switch (action) {
        case '举报':
          handleReport()
          break
        case '不感兴趣':
          handleNotInterested()
          break
        case '字体设置':
          showFontSettings()
          break
      }
    }
  })
}

const showCommentInput = () => {
  // TODO: 实现评论输入功能
  uni.showToast({
    title: '评论功能即将上线',
    icon: 'none'
  })
}

// 辅助方法
const recordViewHistory = () => {
  if (article.value) {
    contentStore.addViewHistory({
      id: article.value.id,
      type: 'article',
      title: article.value.title,
      cover_url: article.value.cover_url,
      view_time: Date.now()
    })
  }
}

const recordReadHistory = () => {
  if (article.value) {
    contentStore.addReadHistory({
      id: article.value.id,
      type: 'article',
      read_time: Date.now(),
      read_duration: Date.now() - (contentStore.getPageStartTime() || Date.now())
    })
  }
}

const getBaseUrl = () => {
  // 获取基础 URL，用于分享链接
  return 'https://yangmie.com'
}

const handleReport = () => {
  // TODO: 实现举报功能
  uni.showToast({
    title: '举报功能即将上线',
    icon: 'none'
  })
}

const handleNotInterested = () => {
  // TODO: 实现不感兴趣功能
  uni.showToast({
    title: '已标记不感兴趣',
    icon: 'success'
  })
}

const showFontSettings = () => {
  // TODO: 实现字体设置功能
  uni.showToast({
    title: '字体设置功能即将上线',
    icon: 'none'
  })
}

// 生命周期清理
onUnmounted(() => {
  if (ttsPlayer.value) {
    ttsPlayer.value.destroy()
    ttsPlayer.value = null
  }
})

// 导出供模板使用的方法和数据
defineExpose({
  loadArticleDetail,
  toggleTTS,
  toggleLike,
  toggleBookmark,
  shareArticle
})
</script>

<style lang="scss" scoped>
.article-detail-page {
  min-height: 100vh;
  background-color: #fff;
  padding-bottom: 120rpx; // 为底部操作栏留空间
}

.nav-actions {
  display: flex;
  align-items: center;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120rpx 32rpx;
  text-align: center;
}

.loading-text {
  margin-top: 24rpx;
  font-size: 28rpx;
  color: #8d96a0;
}

.error-title {
  margin: 24rpx 0 16rpx;
  font-size: 32rpx;
  font-weight: 600;
  color: #2c3038;
}

.error-message {
  margin-bottom: 32rpx;
  font-size: 26rpx;
  color: #8d96a0;
  line-height: 1.4;
}

.article-content {
  padding: 32rpx;
}

.article-header {
  margin-bottom: 40rpx;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 24rpx;
  flex-wrap: wrap;
}

.content-type-badge {
  display: flex;
  align-items: center;
  gap: 6rpx;
  padding: 6rpx 12rpx;
  border-radius: 16rpx;
  font-size: 20rpx;
  
  &.article {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: #fff;
  }
}

.publish-time,
.read-count {
  font-size: 24rpx;
  color: #8d96a0;
}

.article-title {
  display: block;
  font-size: 40rpx;
  font-weight: 700;
  color: #2c3038;
  line-height: 1.4;
  margin-bottom: 24rpx;
}

.article-summary {
  padding: 24rpx;
  background-color: #f8f9fa;
  border-radius: 12rpx;
  margin-bottom: 32rpx;
  
  text {
    font-size: 28rpx;
    color: #666;
    line-height: 1.6;
  }
}

.author-info {
  display: flex;
  align-items: center;
  padding: 24rpx;
  background-color: #f8f9fa;
  border-radius: 12rpx;
  margin-bottom: 32rpx;
}

.author-avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 40rpx;
  margin-right: 24rpx;
}

.author-details {
  flex: 1;
  min-width: 0;
}

.author-name {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: #2c3038;
  margin-bottom: 8rpx;
}

.author-desc {
  display: block;
  font-size: 24rpx;
  color: #8d96a0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tts-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16rpx;
  margin-bottom: 24rpx;
}

.tts-info {
  display: flex;
  align-items: center;
  gap: 12rpx;
  flex: 1;
}

.tts-label {
  font-size: 26rpx;
  color: #fff;
  font-weight: 500;
}

.tts-duration {
  font-size: 22rpx;
  color: rgba(255, 255, 255, 0.8);
}

.tts-actions {
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.tts-play-button {
  width: 60rpx;
  height: 60rpx;
  border-radius: 30rpx;
  background-color: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10rpx);
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:active {
    transform: scale(0.95);
  }
}

.reading-progress {
  margin-top: 16rpx;
}

.article-body {
  margin-bottom: 60rpx;
  
  &.tts-highlight {
    // TTS 播放时的高亮样式
    animation: gentle-glow 2s infinite ease-in-out;
  }
}

.article-text {
  font-size: 32rpx;
  line-height: 1.8;
  color: #2c3038;
  
  // 处理富文本样式
  :deep(p) {
    margin-bottom: 24rpx;
  }
  
  :deep(img) {
    max-width: 100%;
    height: auto;
    border-radius: 8rpx;
    margin: 24rpx 0;
  }
  
  :deep(blockquote) {
    padding: 24rpx;
    background-color: #f8f9fa;
    border-left: 6rpx solid #4CD964;
    border-radius: 0 8rpx 8rpx 0;
    margin: 24rpx 0;
    font-style: italic;
    color: #666;
  }
  
  :deep(code) {
    padding: 4rpx 8rpx;
    background-color: #f1f3f4;
    border-radius: 4rpx;
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: 0.9em;
  }
  
  :deep(pre) {
    padding: 24rpx;
    background-color: #f8f9fa;
    border-radius: 8rpx;
    overflow-x: auto;
    margin: 24rpx 0;
    
    code {
      padding: 0;
      background: none;
    }
  }
}

.related-section,
.comments-section {
  margin-top: 60rpx;
  padding-top: 40rpx;
  border-top: 1px solid #eaedf0;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.coming-soon {
  display: block;
  text-align: center;
  padding: 60rpx 32rpx;
  font-size: 28rpx;
  color: #8d96a0;
}

.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  background-color: #fff;
  border-top: 1px solid #eaedf0;
  padding: 24rpx 32rpx;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  z-index: 1000;
}

.action-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  cursor: pointer;
  
  &:active {
    opacity: 0.7;
  }
  
  text {
    font-size: 22rpx;
    color: #8d96a0;
    transition: color 0.2s ease;
    
    &.liked {
      color: #ff3b30;
    }
    
    &.bookmarked {
      color: #4CD964;
    }
  }
}

.tts-settings {
  padding: 32rpx;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24rpx 0;
  border-bottom: 1px solid #eaedf0;
  
  &:last-child {
    border-bottom: none;
  }
}

.setting-label {
  font-size: 28rpx;
  color: #2c3038;
  font-weight: 500;
}

.setting-value {
  font-size: 26rpx;
  color: #8d96a0;
  background-color: #f8f9fa;
  padding: 12rpx 16rpx;
  border-radius: 8rpx;
  min-width: 120rpx;
  text-align: center;
}

.disabled {
  opacity: 0.5;
  pointer-events: none;
}

@keyframes gentle-glow {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(76, 217, 100, 0);
  }
  50% {
    box-shadow: 0 0 20rpx 0 rgba(76, 217, 100, 0.1);
  }
}
</style>