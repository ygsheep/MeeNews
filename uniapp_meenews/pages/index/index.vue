<template>
  <view class="index-page">
    <!-- 顶部导航 -->
    <NavBar :title="'羊咩快报'" :fixed="true">
      <template #right>
        <fui-icon name="search" color="#333" size="24" @click="goToSearch" />
      </template>
    </NavBar>

    <!-- 问候语部分 -->
    <view class="greeting-section">
      <text class="greeting-text">{{ greetingText }}</text>
      <fui-icon name="star" color="#FFD700" size="16" />
    </view>

    <!-- 分类导航（资讯导向） -->
    <scroll-view scroll-x class="category-scroll">
      <view class="category-nav">
        <view v-for="category in categories" :key="category.id" class="category-item"
          :class="{ active: activeCategoryId === category.id }" @click="selectCategory(category.id)">
          <text class="category-text">{{ category.name }}</text>
        </view>
      </view>
    </scroll-view>

    <!-- 内容区块：根据分类动态渲染 -->
    <ContentSection title="分类内容" :show-more="false">
      <view class="content-list vertical">
        <ContentCard v-for="item in contentList" :key="item.id" :content="item" cardType="list"
          @click="handleContentClick(item)" @like="handleLike" />
      </view>
    </ContentSection>

    <!-- 推荐作者区块（如有） -->
    <ContentSection v-if="authorList && authorList.length" title="推荐作者" :show-more="true">
      <scroll-view scroll-x class="horizontal-scroll">
        <view class="author-list horizontal">
          <ArtistCard v-for="author in authorList" :key="author.id" :artist="author" @click="goToAuthor(author.id)" />
        </view>
      </scroll-view>
    </ContentSection>


    <CustomTabBar :current="currentTab" @switch="onTabSwitch" @play="onPlayBtnClick" />
    <!-- 全屏播放器弹窗，仅在 showPlayer 时显示 -->
    <view v-if="showPlayer" class="player-modal" :class="{ 'player-modal--show': showPlayer }" @touchmove.stop.prevent>
      <MediaPlayer @close="closePlayerModal" />
    </view>
    <view v-if="showPlayer" class="player-mask" @click="closePlayerModal"></view>
  </view>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { useContentStore } from '@/store/content'
import { usePlayerStore } from '@/store/player'
import NavBar from '@/components/common/NavBar.vue'
import ContentSection from '@/components/content/ContentSection.vue'
import ContentCard from '@/components/content/ContentCard.vue'
import ArtistCard from '@/components/content/ArtistCard.vue'
import CustomTabBar from '@/components/tabbar/index.vue'
import MediaPlayer from '@/components/player/MediaPlayer.vue'
import { getRecommendList, getDailyNews, getFollowContent, getNewsContent, getRecommendedAuthors, getCategoryList } from '@/api/content'
import { ContentValidator, CONTENT_TYPES } from '@/utils/contentValidator'
import request from '@/utils/request'

const userStore = useUserStore()
const contentStore = useContentStore()
const playerStore = usePlayerStore()

export default {
  name: 'Index',
  components: { NavBar, ContentSection, ContentCard, ArtistCard, CustomTabBar, MediaPlayer },
  setup() {
    // 分类数据
    const categories = ref([])
    const activeCategoryId = ref(null)
    // 内容数据
    const contentList = ref([])
    // 其他区块数据
    const authorList = ref([])
    // 播放器
    const showPlayer = ref(false)
    const currentContent = computed(() => playerStore.currentContent)
    const isPlaying = computed(() => playerStore.isPlaying)
    // 问候语
    const greetingText = computed(() => {
      const hour = new Date().getHours()
      const username = userStore.userInfo?.nickname || '用户'
      if (hour < 12) return `早安, ${username}`
      if (hour < 18) return `下午好, ${username}`
      return `晚上好, ${username}`
    })
    // 加载分类列表
    const loadCategories = async () => {
      try {
        categories.value = await getCategoryList()
        if (categories.value.length > 0) {
          activeCategoryId.value = categories.value[0].id
          await loadContentByCategoryId(categories.value[0].id)
        }
      } catch (error) {
        console.error('分类获取失败:', error)
        categories.value = []
        uni.showToast({ title: '分类加载失败', icon: 'none' })
      }
    }
    // 分类切换
    const selectCategory = async (id) => {
      if (activeCategoryId.value === id) return // 避免重复加载
      activeCategoryId.value = id
      await loadContentByCategoryId(id)
    }
    // 分类内容联动加载
    const loadContentByCategoryId = async (categoryId) => {
      try {
        // 可根据业务需求扩展参数，如 type、sort 等
        contentList.value = await getRecommendList({ category_id: categoryId, page: 1, page_size: 20 })
        // 推荐作者区块（如有需求）
        authorList.value = await getRecommendedAuthors({ category_id: categoryId, page: 1, page_size: 10 })
      } catch (error) {
        contentList.value = []
        authorList.value = []
        uni.showToast({ title: '内容加载失败', icon: 'none' })
      }
    }
    // 首次加载
    onMounted(() => {
      loadCategories()
    })
    // 播放器状态
    const showPlayerModal = () => {
      showPlayer.value = true
    }

    // 关闭播放器模态框
    const closePlayerModal = () => {
      showPlayer.value = false
    }
    // 喜欢/取消喜欢
    const handleLike = (item) => {
      // 业务逻辑：调用API或store方法
      contentStore.toggleLike(item)
    }


    // 跳转
    const goToSearch = () => {
      uni.navigateTo({ url: '/pages/discover/search' })
    }
    const goToRecommend = () => {
      // 可跳转到推荐内容页
    }
    const goToAuthors = () => {
      uni.navigateTo({ url: '/pages/author/list' })
    }
    const goToAuthor = (id) => {
      uni.navigateTo({ url: `/pages/author/detail?id=${id}` })
    }

    const goToPlayer = (item) => {
      playerStore.setCurrentContent(item)
      uni.navigateTo({ url: '/pages/player/mediaPlayer' })
    }

    // 新增：内容卡片点击处理 - 根据内容类型智能跳转
    const handleContentClick = (item) => {
      console.log('Content clicked:', item)

      // 检查代码逻辑并修正
      // 1. 变量content未声明，且赋值语法错误（content = = res.data）
      // 2. 异步请求后立即访问content.type，content还未赋值，逻辑有误
      // 3. 建议将后续逻辑放在then回调中，保证数据可用
      // 4. request方法未引入，假设已全局可用

      request({
        url: `/content/${item.id}`,
        method: 'GET'
      }).then(res => {
        // 请求成功，res.data为内容详情对象
        const content = res.data
        const contentType = content.type

        // 根据内容类型进行不同的处理
        switch (contentType) {
          case CONTENT_TYPES.ARTICLE:
          case CONTENT_TYPES.NEWS:
            // 文章类型：跳转到文章详情页
            uni.navigateTo({
              url: `/pages/article/detail?id=${content.id}`
            })
            break

          case CONTENT_TYPES.AUDIO:
            break
          case CONTENT_TYPES.PODCAST:
          case CONTENT_TYPES.LIVE:
          case CONTENT_TYPES.VIDEO:
            // 音视频类型：设置播放内容并显示全屏播放器
            const normalized = {
              ...content,
              video_url: content.video_content?.video_url,
              duration: content.video_content?.duration,
              thumbnail_url: content.video_content?.thumbnail_url || content.video_content?.poster_url
            }
            console.log(normalized);
            
            playerStore.setCurrentContent(normalized)
            // console.log(content.video_content.video_url)
            showPlayerModal()
            break



          default:
            // 未知类型：根据内容特征判断
            if (content.content || content.html_content || content.markdown_content) {
              // 有文本内容，当作文章处理
              uni.navigateTo({
                url: `/pages/article/detail?id=${content.id}`
              })
            } else if (content.audio_url || content.video_url || content.stream_url || content.media_url) {
              // 有媒体URL，当作音视频处理
              playerStore.setCurrentContent(content)
              showPlayerModal()
            } else {
              // 默认跳转到文章详情页
              console.warn('无法确定内容类型，默认跳转到详情页:', contentType)
              uni.navigateTo({
                url: `/pages/article/detail?id=${content.id}`
              })
            }
            break
        }
      }).catch(err => {
        // 请求失败或网络异常
        console.error('内容详情请求异常:', err)
        uni.showToast({
          title: '获取内容失败',
          icon: 'error'
        })
        return
      })
    }

    // 防止模板引用报错，补充空实现
    const togglePlay = () => {}
    const playNext = () => {}

    return {
      greetingText,
      categories,
      activeCategoryId,
      selectCategory,
      contentList,
      authorList,
      showPlayer,
      currentContent,
      isPlaying,
      showPlayerModal,
      closePlayerModal,
      handleLike,
      togglePlay,
      playNext,
      goToSearch,
      goToRecommend,
      goToAuthors,
      goToAuthor,
      goToPlayer,
      handleContentClick,
    }
  },
  data() {
    return {
      currentTab: 0, // 首页高亮
    }
  },
  watch: {
    // 监听路由变化自动高亮
    '$route.path'(val) {
      this.updateTabIndex(val)
    }
  },
  mounted() {
    this.updateTabIndex(this.$route.path)
  },
  methods: {
    updateTabIndex(path) {
      // 路径与tab顺序对应
      const tabPaths = ['/pages/index/index', '/pages/discover/discover', '/pages/library/library', '/pages/profile/profile']
      const idx = tabPaths.findIndex(p => path.startsWith(p))
      this.currentTab = idx === -1 ? 0 : idx
    },
    onTabSwitch(idx, tabItem) {
      if (this.currentTab !== idx) {
        uni.redirectTo({ url: tabItem.pagePath })
      }
    },
    onPlayBtnClick() {
      this.showPlayerModal()
    }
  }
}
</script>

<style lang="scss" scoped>
.index-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.greeting-section {
  padding: 20rpx 32rpx;
  display: flex;
  align-items: center;

  .greeting-text {
    font-size: 48rpx;
    font-weight: 600;
    color: #2c3038;
    margin-right: 16rpx;
  }
}

.category-scroll {
  white-space: nowrap;
  padding: 0 32rpx 32rpx;
}

.category-nav {
  display: flex;
  gap: 32rpx;
}

.category-item {
  padding: 16rpx 24rpx;
  border-radius: 40rpx;
  background-color: #eaedf0;
  transition: all 0.3s ease;

  &.active {
    background-color: #4CD964;

    .category-text {
      color: #fff;
    }
  }

  .category-text {
    font-size: 28rpx;
    color: #2c3038;
    font-weight: 500;
  }
}

.content-sections {
  padding-bottom: 160rpx;
}

.horizontal-scroll {
  white-space: nowrap;
}

.author-list {
  display: flex;
  gap: 32rpx;
  padding: 0 32rpx;
}

.content-list.vertical {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
  padding: 0 32rpx;
}

.player-modal {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  z-index: 2000;
  background: #000;
  transform: translateY(100%);
  transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  will-change: transform;
}

.player-modal--show {
  transform: translateY(0);
}

.player-mask {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 1999;
  opacity: 0;
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}
</style>