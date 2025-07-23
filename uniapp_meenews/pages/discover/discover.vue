<template>
  <view class="discover-page">
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-container">
        <fui-icon name="search" color="#8d96a0" size="20" />
        <input 
          class="search-input"
          placeholder="搜索文章、视频、音频内容"
          v-model="searchQuery"
          @input="onSearchInput"
          @confirm="performSearch"
        />
        <fui-icon 
          name="filter" 
          color="#8d96a0" 
          size="20"
          @click="showFilterModal"
        />
      </view>
      <!-- 搜索建议 -->
      <view class="search-suggestions" v-if="searchSuggestions.length && searchQuery">
        <view 
          v-for="suggestion in searchSuggestions"
          :key="suggestion.id"
          class="suggestion-item"
          @click="selectSuggestion(suggestion)"
        >
          <fui-icon name="search" color="#8d96a0" size="16" />
          <text class="suggestion-text">{{ suggestion.text }}</text>
          <text class="suggestion-type">{{ suggestion.type }}</text>
        </view>
      </view>
    </view>

    <!-- 内容类型切换（多媒体tab） -->
    <view class="content-type-tabs">
      <scroll-view scroll-x class="tabs-scroll">
        <view class="tabs-container">
          <view 
            v-for="tab in contentTabs"
            :key="tab.type"
            class="tab-item"
            :class="{ active: activeContentType === tab.type }"
            @click="switchContentType(tab.type)"
          >
            <fui-icon :name="tab.icon" :color="getTabColor(tab.type)" size="20" />
            <text class="tab-text" :style="{ color: getTabColor(tab.type) }">
              {{ tab.name }}
            </text>
            <view class="tab-count" v-if="tab.count > 0">{{ formatCount(tab.count) }}</view>
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- 标签分类 -->
    <view class="tags-section" v-if="!isSearchMode">
      <view class="section-header">
        <text class="section-title">热门标签</text>
        <text class="more-link" @click="showAllTags">更多</text>
      </view>
      <view class="tags-container">
        <scroll-view scroll-x class="tags-scroll">
          <view class="tags-list">
            <view 
              v-for="tag in popularTags"
              :key="tag.id"
              class="tag-item"
              :class="{ active: selectedTags.includes(tag.id) }"
              @click="toggleTag(tag)"
            >
              <text class="tag-name">#{{ tag.name }}</text>
              <text class="tag-count">{{ tag.content_count }}</text>
            </view>
          </view>
        </scroll-view>
      </view>
    </view>

    <!-- 分类筛选 -->
    <view class="category-filter" v-if="!isSearchMode">
      <view class="filter-header">
        <text class="filter-title">分类筛选</text>
        <view class="filter-actions">
          <text class="clear-filters" @click="clearFilters" v-if="hasActiveFilters">
            清除筛选
          </text>
          <fui-icon 
            name="sliders" 
            color="#8d96a0" 
            size="18"
            @click="showAdvancedFilter"
          />
        </view>
      </view>
      <scroll-view scroll-x class="category-scroll">
        <view class="category-list">
          <view 
            v-for="category in categories"
            :key="category.id"
            class="category-chip"
            :class="{ active: selectedCategories.includes(category.id) }"
            @click="toggleCategory(category)"
          >
            <fui-icon :name="category.icon" size="16" color="inherit" />
            <text class="category-name">{{ category.name }}</text>
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- 排序选项 -->
    <view class="sort-section">
      <view class="sort-container">
        <text class="sort-label">排序：</text>
        <picker 
          :range="sortOptions" 
          range-key="name"
          @change="onSortChange"
          class="sort-picker"
        >
          <view class="sort-selected">
            <text class="sort-text">{{ currentSort.name }}</text>
            <fui-icon name="chevron-down" color="#8d96a0" size="16" />
          </view>
        </picker>
        <view class="view-mode-toggle">
          <fui-icon 
            :name="viewMode === 'list' ? 'list' : 'grid'" 
            :color="viewMode === 'list' ? '#4CD964' : '#8d96a0'"
            size="20"
            @click="toggleViewMode"
          />
        </view>
      </view>
    </view>

    <!-- 内容列表区块（全部用新版ContentCard） -->
    <view class="content-section">
      <!-- 搜索结果 -->
      <view class="search-results" v-if="isSearchMode">
        <view class="results-header">
          <text class="results-count">找到 {{ totalResults }} 个结果</text>
          <text class="search-time">用时 {{ searchTime }}ms</text>
        </view>
        <view :class="['search-content-list', viewMode]">
          <ContentCard 
            v-for="item in searchResults"
            :key="item.id"
            :content="item"
            :card-type="viewMode === 'list' ? 'list' : 'small'"
            @click="handleContentClick(item)"
            @like="toggleLike(item)"
          />
        </view>
        <view v-if="hasMoreSearchResults && !searchLoading" class="load-more" @click="loadMoreSearchResults">加载更多</view>
        <view v-if="searchLoading" class="loading-text">加载中...</view>
      </view>

      <!-- 发现内容 -->
      <view class="discover-content" v-else>
        <!-- 今日推荐 -->
        <ContentSection 
          title="今日推荐"
          subtitle="基于您的兴趣精选"
          :show-more="true"
          @more="viewRecommendations"
          v-if="recommendedContents.length"
        >
          <scroll-view scroll-x class="horizontal-scroll">
            <view class="horizontal-list">
              <ContentCard 
                v-for="content in recommendedContents.slice(0, 5)"
                :key="content.id"
                :content="content"
                card-type="featured"
                @click="handleContentClick(content)"
                @like="toggleLike(content)"
              />
            </view>
          </scroll-view>
        </ContentSection>

        <!-- 热门内容 -->
        <ContentSection 
          title="热门内容"
          subtitle="最受欢迎的内容"
          :show-more="true"
          @more="viewTrending"
        >
          <view :class="['trending-content-list', viewMode]">
            <ContentCard 
              v-for="item in trendingContents"
              :key="item.id"
              :content="item"
              :card-type="viewMode === 'list' ? 'list' : 'small'"
              @click="handleContentClick(item)"
              @like="toggleLike(item)"
            />
          </view>
          <view v-if="hasMoreTrending && !trendingLoading" class="load-more" @click="loadMoreTrending">加载更多</view>
          <view v-if="trendingLoading" class="loading-text">加载中...</view>
        </ContentSection>

        <!-- 分类内容 -->
        <view class="category-contents" v-if="selectedCategories.length">
          <ContentSection 
            v-for="categoryId in selectedCategories"
            :key="categoryId"
            :title="getCategoryName(categoryId)"
            :subtitle="getCategoryDescription(categoryId)"
            :show-more="true"
            @more="viewCategoryContent(categoryId)"
          >
            <view :class="['category-content-list', viewMode]">
              <ContentCard 
                v-for="item in getCategoryContents(categoryId)"
                :key="item.id"
                :content="item"
                :card-type="viewMode === 'list' ? 'list' : 'small'"
                @click="handleContentClick(item)"
                @like="toggleLike(item)"
              />
            </view>
            <view v-if="hasCategoryMore(categoryId) && !getCategoryLoading(categoryId)" class="load-more" @click="loadMoreCategoryContent(categoryId)">加载更多</view>
            <view v-if="getCategoryLoading(categoryId)" class="loading-text">加载中...</view>
          </ContentSection>
        </view>

        <!-- 标签内容 -->
        <view class="tag-contents" v-if="selectedTags.length">
          <ContentSection 
            v-for="tagId in selectedTags"
            :key="tagId"
            :title="`#${getTagName(tagId)}`"
            :subtitle="getTagDescription(tagId)"
            :show-more="true"
            @more="viewTagContent(tagId)"
          >
            <view :class="['tag-content-list', viewMode]">
              <ContentCard 
                v-for="item in getTagContents(tagId)"
                :key="item.id"
                :content="item"
                :card-type="viewMode === 'list' ? 'list' : 'small'"
                @click="handleContentClick(item)"
                @like="toggleLike(item)"
              />
            </view>
            <view v-if="hasTagMore(tagId) && !getTagLoading(tagId)" class="load-more" @click="loadMoreTagContent(tagId)">加载更多</view>
            <view v-if="getTagLoading(tagId)" class="loading-text">加载中...</view>
          </ContentSection>
        </view>
      </view>
    </view>

    <!-- 筛选弹窗 -->
    <FilterModal 
      v-model:visible="showFilter"
      :content-type="activeContentType"
      :categories="categories"
      :tags="allTags"
      :selected-categories="selectedCategories"
      :selected-tags="selectedTags"
      :date-range="dateRange"
      :duration-range="durationRange"
      @apply="applyFilters"
      @reset="resetFilters"
    />

    <!-- 标签选择器 -->
    <TagSelector 
      v-model:visible="showTagSelector"
      :tags="allTags"
      :selected="selectedTags"
      @confirm="onTagsSelected"
    />

    <!-- 空状态 -->
    <Empty 
      v-if="showEmptyState"
      :icon="getEmptyStateIcon()"
      :title="getEmptyStateTitle()"
      :description="getEmptyStateDescription()"
      @action="handleEmptyAction"
    />

    <!-- 迷你播放器 -->
    <MiniPlayer />
    <CustomTabBar :current="currentTab" @switch="onTabSwitch" @play="onPlayBtnClick" />
    <!-- 全屏播放器弹窗 -->
    <view v-if="showPlayer" class="player-modal" :class="{ 'player-modal--show': showPlayer }" @touchmove.stop.prevent>
      <MediaPlayer @close="closePlayer" />
    </view>
    <view v-if="showPlayer" class="player-mask" @click="closePlayer"></view>
  </view>
</template>

<script>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { usePlayerStore } from '@/store/modules/player'
import ContentSection from '@/components/content/ContentSection.vue'
import ContentList from '@/components/content/ContentList.vue'
import ContentCard from '@/components/content/ContentCard.vue'
import FilterModal from '@/components/discover/FilterModal.vue'
import TagSelector from '@/components/discover/TagSelector.vue'
import Empty from '@/components/common/Empty.vue'
import MiniPlayer from '@/components/player/MiniPlayer.vue'
import CustomTabBar from '@/components/tabbar/index.vue'
import MediaPlayer from '@/components/player/MediaPlayer.vue'
import { http } from '@/utils/request'

const playerStore = usePlayerStore()

// 数据定义
const searchQuery = ref('')
const searchSuggestions = ref([])
const activeContentType = ref('article')
const selectedCategories = ref([])
const selectedTags = ref([])
const viewMode = ref('list') // 'list' | 'grid'
const currentSort = ref({ name: '最新', value: 'latest' })
const showFilter = ref(false)
const showTagSelector = ref(false)

// 搜索相关
const isSearchMode = ref(false)
const searchResults = ref([])
const totalResults = ref(0)
const searchTime = ref(0)
const searchLoading = ref(false)
const hasMoreSearchResults = ref(false)

// 内容数据
const recommendedContents = ref([])
const trendingContents = ref([])
const latestContents = ref([])
const categoryContents = ref({})
const tagContents = ref({})

// 加载状态
const trendingLoading = ref(false)
const latestLoading = ref(false)
const hasMoreTrending = ref(false)
const hasMoreLatest = ref(false)

// 配置数据
const contentTabs = ref([
  { type: 'article', name: '文章', icon: 'file-text', count: 0 },
  { type: 'video', name: '视频', icon: 'video', count: 0 },
  { type: 'audio', name: '音频', icon: 'music', count: 0 }
])

const sortOptions = [
  { name: '最新', value: 'latest' },
  { name: '最热', value: 'trending' },
  { name: '最多播放', value: 'popular' },
  { name: '最多收藏', value: 'liked' },
  { name: '时长', value: 'duration' }
]

const popularTags = ref([])
const allTags = ref([])
const categories = ref([])

// 筛选条件
const dateRange = ref({})
const durationRange = ref({})

// 计算属性
const hasActiveFilters = computed(() => {
  return selectedCategories.value.length > 0 || 
         selectedTags.value.length > 0 ||
         Object.keys(dateRange.value).length > 0 ||
         Object.keys(durationRange.value).length > 0
})

const showEmptyState = computed(() => {
  if (isSearchMode.value) {
    return !searchLoading.value && searchResults.value.length === 0 && searchQuery.value
  }
  return !trendingLoading.value && trendingContents.value.length === 0
})

// 方法定义
const onSearchInput = (e) => {
  const query = e.detail.value
  searchQuery.value = query
  
  if (query.length > 0) {
    isSearchMode.value = true
    debounceSearch(query)
  } else {
    isSearchMode.value = false
    searchSuggestions.value = []
  }
}

const debounceSearch = debounce(async (query) => {
  try {
    const response = await http.get('/search/suggestions', {
      q: query,
      content_type: activeContentType.value,
      limit: 8
    })
    
    if (response.success) {
      searchSuggestions.value = response.data.suggestions
    }
  } catch (error) {
    console.error('获取搜索建议失败:', error)
  }
}, 300)


const selectSuggestion = (suggestion) => {
  searchQuery.value = suggestion.text
  searchSuggestions.value = []
  performSearch()
}

// 切换内容类型
const switchContentType = (type) => {
  activeContentType.value = type
  refreshContent()
}

const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag.id)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(tag.id)
  }
  refreshContent()
}

const toggleCategory = (category) => {
  const index = selectedCategories.value.indexOf(category.id)
  if (index > -1) {
    selectedCategories.value.splice(index, 1)
  } else {
    selectedCategories.value.push(category.id)
  }
  refreshContent()
}

const onSortChange = (e) => {
  currentSort.value = sortOptions[e.detail.value]
  refreshContent()
}

const toggleViewMode = () => {
  viewMode.value = viewMode.value === 'list' ? 'grid' : 'list'
}

const playContent = (content) => {
  playerStore.playContent(content)
}

const toggleLike = async (content) => {
  try {
    await http.post('/content/toggle-like', { content_id: content.id })
    content.is_liked = !content.is_liked
  } catch (error) {
    uni.showToast({
      title: '操作失败',
      icon: 'error'
    })
  }
}

const clearFilters = () => {
  selectedCategories.value = []
  selectedTags.value = []
  dateRange.value = {}
  durationRange.value = {}
  refreshContent()
}

const showFilterModal = () => {
  showFilter.value = true
}

const showAdvancedFilter = () => {
  showFilter.value = true
}

const showAllTags = () => {
  showTagSelector.value = true
}

const applyFilters = (filters) => {
  selectedCategories.value = filters.categories
  selectedTags.value = filters.tags
  dateRange.value = filters.dateRange
  durationRange.value = filters.durationRange
  showFilter.value = false
  refreshContent()
}

const resetFilters = () => {
  clearFilters()
  showFilter.value = false
}

const onTagsSelected = (tags) => {
  selectedTags.value = tags
  showTagSelector.value = false
  refreshContent()
}

const refreshContent = async () => {
  await Promise.all([
    loadRecommendedContent(),
    loadTrendingContent(),
    loadLatestContent()
  ])
}

// 分类加载
const loadCategories = async () => {
  try {
    const response = await http.get('/categories')
    if (response.success) {
      categories.value = response.data
    }
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}
// 推荐内容加载
const loadRecommendedContent = async () => {
  try {
    const response = await http.get('/content/recommend', { type: activeContentType.value, page_size: 10 })
    if (response.success) {
      recommendedContents.value = response.data.results
    }
  } catch (error) {
    console.error('加载推荐内容失败:', error)
  }
}
// 热门内容加载
const loadTrendingContent = async () => {
  try {
    trendingLoading.value = true
    const response = await http.get('/content/trending', {
      type: activeContentType.value,
      categories: selectedCategories.value.join(','),
      tags: selectedTags.value.join(','),
      sort: currentSort.value.value,
      page: 1,
      page_size: 20
    })
    if (response.success) {
      trendingContents.value = response.data.results
      hasMoreTrending.value = response.data.has_more
    }
  } catch (error) {
    console.error('加载热门内容失败:', error)
  } finally {
    trendingLoading.value = false
  }
}
// 搜索内容
const performSearch = async () => {
  try {
    searchLoading.value = true
    const response = await http.get('/content/search', {
      q: searchQuery.value,
      type: activeContentType.value,
      categories: selectedCategories.value.join(','),
      tags: selectedTags.value.join(','),
      sort: currentSort.value.value,
      page: 1,
      page_size: 20
    })
    if (response.success) {
      searchResults.value = response.data.results
      totalResults.value = response.data.total
      hasMoreSearchResults.value = response.data.has_more
    }
  } catch (error) {
    uni.showToast({ title: '搜索失败', icon: 'error' })
  } finally {
    searchLoading.value = false
  }
}
// 标签加载
const loadPopularTags = async () => {
  try {
    const response = await http.get('/tags/popular', { type: activeContentType.value, limit: 10 })
    if (response.success) {
      popularTags.value = response.data
    }
  } catch (error) {
    console.error('加载热门标签失败:', error)
  }
}

const loadLatestContent = async () => {
  try {
    latestLoading.value = true
    
    const response = await http.get('/content/latest', {
      type: activeContentType.value,
      categories: selectedCategories.value.join(','),
      tags: selectedTags.value.join(','),
      page: 1,
      page_size: 15
    })
    
    if (response.success) {
      latestContents.value = response.data.results
      hasMoreLatest.value = response.data.has_more
    }
  } catch (error) {
    console.error('加载最新内容失败:', error)
  } finally {
    latestLoading.value = false
  }
}

const getTabColor = (type) => {
  return activeContentType.value === type ? '#4CD964' : '#8d96a0'
}

const formatCount = (count) => {
  if (count >= 1000000) {
    return `${(count / 1000000).toFixed(1)}M`
  }
  if (count >= 1000) {
    return `${(count / 1000).toFixed(1)}K`
  }
  return count.toString()
}

const getCategoryName = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category?.name || ''
}

const getCategoryDescription = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category?.description || ''
}

const getTagName = (tagId) => {
  const tag = allTags.value.find(t => t.id === tagId)
  return tag?.name || ''
}

const getTagDescription = (tagId) => {
  const tag = allTags.value.find(t => t.id === tagId)
  return `${tag?.content_count || 0} 个内容`
}

const getCategoryContents = (categoryId) => {
  return categoryContents.value[categoryId] || []
}

const getTagContents = (tagId) => {
  return tagContents.value[tagId] || []
}

const getEmptyStateIcon = () => {
  if (isSearchMode.value) return 'search'
  return 'inbox'
}

const getEmptyStateTitle = () => {
  if (isSearchMode.value) return '没有找到相关内容'
  return '暂无内容'
}

const getEmptyStateDescription = () => {
  if (isSearchMode.value) return '尝试更换关键词或调整筛选条件'
  return '暂时没有相关内容，稍后再来看看吧'
}

const handleEmptyAction = () => {
  if (isSearchMode.value) {
    clearFilters()
  }
}

const goToPlayer = (item) => {
  playerStore.setCurrentContent(item)
  uni.navigateTo({ url: '/pages/player/mediaPlayer' })
}

// 新增：内容卡片点击处理
const handleContentClick = (item) => {
  // 可根据实际内容类型跳转不同详情页
  uni.navigateTo({ url: `/pages/article/detail?id=${item.id}` })
}

// 工具函数
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// 生命周期
onMounted(async () => {
  await Promise.all([
    loadCategories(),
    loadPopularTags(),
    refreshContent()
  ])
})

// 监听器
watch(activeContentType, () => {
  loadPopularTags()
  loadCategories()
})

export default {
  components: { CustomTabBar, MediaPlayer },
  data() {
    return {
      currentTab: 1, // 发现页高亮
      showPlayer: false,
    }
  },
  watch: {
    '$route.path'(val) {
      this.updateTabIndex(val)
    }
  },
  mounted() {
    this.updateTabIndex(this.$route.path)
  },
  methods: {
    updateTabIndex(path) {
      const tabPaths = ['/pages/index/index', '/pages/discover/discover', '/pages/library/library', '/pages/profile/profile']
      const idx = tabPaths.findIndex(p => path.startsWith(p))
      this.currentTab = idx === -1 ? 1 : idx
    },
    onTabSwitch(idx, tabItem) {
      if (this.currentTab !== idx) {
        uni.redirectTo({ url: tabItem.pagePath })
      }
    },
    onPlayBtnClick() {
      this.showPlayer = true
    },
    closePlayer() {
      this.showPlayer = false
    },
  },
  setup() {
    return {
      searchQuery,
      searchSuggestions,
      activeContentType,
      selectedCategories,
      selectedTags,
      viewMode,
      currentSort,
      sortOptions,
      onSortChange,
      isSearchMode,
      searchResults,
      totalResults,
      searchTime,
      searchLoading,
      hasMoreSearchResults,
      recommendedContents,
      trendingContents,
      latestContents,
      categoryContents,
      tagContents,
      trendingLoading,
      latestLoading,
      hasMoreTrending,
      hasMoreLatest,
      contentTabs,
      popularTags,
      allTags,
      categories,
      dateRange,
      durationRange,
      hasActiveFilters,
      showEmptyState,
      onSearchInput,
      debounceSearch,
      performSearch,
      selectSuggestion,
      switchContentType,
      toggleTag,
      toggleCategory,
      toggleViewMode,
      playContent,
      getTabColor,
      formatCount,
      getCategoryName,
      getCategoryDescription,
      getTagName,
      getTagDescription,
      getCategoryContents,
      getTagContents,
      getEmptyStateIcon,
      getEmptyStateTitle,
      getEmptyStateDescription,
      handleEmptyAction,
      goToPlayer,
      showFilter,
      showTagSelector,
      clearFilters,
      showAllTags,
      viewRecommendations,
      viewTrending,
      viewCategoryContent,
      viewTagContent,
      hasCategoryMore,
      getCategoryLoading,
      loadMoreCategoryContent,
      hasTagMore,
      getTagLoading,
      loadMoreTagContent,
      loadMoreSearchResults,
      handleContentClick,
      toggleLike,
    }
  }
}
</script>

<style lang="scss" scoped>
.discover-page {
  min-height: 100vh;
  background: #f8f9fa;
  padding-bottom: 200rpx; // 为迷你播放器留空间
}

.search-section {
  padding: 32rpx;
  background: #ffffff;
  border-bottom: 1px solid #eaedf0;
}

.search-container {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 20rpx 24rpx;
  background: #f8f9fa;
  border-radius: 24rpx;
}

.search-input {
  flex: 1;
  font-size: 28rpx;
  color: #2c3038;
  
  &::placeholder {
    color: #8d96a0;
  }
}

.search-suggestions {
  margin-top: 16rpx;
  background: #ffffff;
  border-radius: 12rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 20rpx 24rpx;
  border-bottom: 1px solid #f0f0f0;
  
  &:last-child {
    border-bottom: none;
  }
}

.suggestion-text {
  flex: 1;
  font-size: 28rpx;
  color: #2c3038;
}

.suggestion-type {
  font-size: 24rpx;
  color: #8d96a0;
}

.content-type-tabs {
  background: #ffffff;
  border-bottom: 1px solid #eaedf0;
}

.tabs-scroll {
  white-space: nowrap;
}

.tabs-container {
  display: flex;
  padding: 0 32rpx;
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  padding: 24rpx 32rpx;
  position: relative;
  
  &.active::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 40rpx;
    height: 4rpx;
    background: #4CD964;
    border-radius: 2rpx;
  }
}

.tab-text {
  font-size: 26rpx;
  font-weight: 500;
}

.tab-count {
  font-size: 20rpx;
  color: #fff;
  background: #ff3b30;
  padding: 2rpx 8rpx;
  border-radius: 8rpx;
  min-width: 32rpx;
  text-align: center;
}

.tags-section {
  padding: 32rpx;
  background: #ffffff;
  margin-bottom: 16rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #2c3038;
}

.more-link {
  font-size: 26rpx;
  color: #4CD964;
}

.tags-scroll {
  white-space: nowrap;
}

.tags-list {
  display: flex;
  gap: 16rpx;
}

.tag-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rpx;
  padding: 16rpx 20rpx;
  background: #f8f9fa;
  border-radius: 16rpx;
  border: 1px solid transparent;
  transition: all 0.3s ease;
  
  &.active {
    background: rgba(76, 217, 100, 0.1);
    border-color: #4CD964;
    
    .tag-name {
      color: #4CD964;
      font-weight: 600;
    }
  }
}

.tag-name {
  font-size: 26rpx;
  color: #2c3038;
  white-space: nowrap;
}

.tag-count {
  font-size: 20rpx;
  color: #8d96a0;
}

.category-filter {
  padding: 32rpx;
  background: #ffffff;
  margin-bottom: 16rpx;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.filter-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #2c3038;
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.clear-filters {
  font-size: 26rpx;
  color: #ff3b30;
}

.category-scroll {
  white-space: nowrap;
}

.category-list {
  display: flex;
  gap: 16rpx;
}

.category-chip {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 12rpx 20rpx;
  background: #f8f9fa;
  border-radius: 20rpx;
  border: 1px solid transparent;
  color: #2c3038;
  transition: all 0.3s ease;
  
  &.active {
    background: rgba(76, 217, 100, 0.1);
    border-color: #4CD964;
    color: #4CD964;
  }
}

.category-name {
  font-size: 26rpx;
  white-space: nowrap;
}

.sort-section {
  padding: 16rpx 32rpx;
  background: #ffffff;
  border-bottom: 1px solid #eaedf0;
}

.sort-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sort-label {
  font-size: 28rpx;
  color: #2c3038;
  margin-right: 16rpx;
}

.sort-selected {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.sort-text {
  font-size: 28rpx;
  color: #2c3038;
}

.view-mode-toggle {
  padding: 12rpx;
  border-radius: 8rpx;
  background: #f8f9fa;
}

.content-section {
  flex: 1;
}

.search-results {
  padding: 32rpx;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.results-count {
  font-size: 28rpx;
  color: #2c3038;
  font-weight: 500;
}

.search-time {
  font-size: 24rpx;
  color: #8d96a0;
}

.discover-content {
  padding: 16rpx 0;
}

.horizontal-scroll {
  white-space: nowrap;
}

.horizontal-list {
  display: flex;
  gap: 24rpx;
  padding: 0 32rpx;
}

.category-contents,
.tag-contents {
  margin-top: 32rpx;
}

.search-content-list,
.trending-content-list,
.category-content-list,
.tag-content-list {
  display: flex;
  gap: 24rpx;
  padding: 0 32rpx;
}

.search-content-list.list,
.trending-content-list.list,
.category-content-list.list,
.tag-content-list.list {
  flex-direction: column;
}

.search-content-list.grid,
.trending-content-list.grid,
.category-content-list.grid,
.tag-content-list.grid {
  flex-wrap: wrap;
}

.load-more {
  text-align: center;
  padding: 20rpx 0;
  color: #4CD964;
  font-size: 28rpx;
  font-weight: 500;
}

.loading-text {
  text-align: center;
  padding: 20rpx 0;
  color: #8d96a0;
  font-size: 28rpx;
}

.player-modal {
  position: fixed;
  left: 0; right: 0; bottom: 0; top: 0;
  z-index: 2000;
  background: #fff;
  transform: translateY(100%);
  transition: transform 0.35s cubic-bezier(0.4,0,0.2,1);
}
.player-modal--show {
  transform: translateY(0);
}
.player-mask {
  position: fixed;
  left: 0; right: 0; top: 0; bottom: 0;
  background: rgba(0,0,0,0.35);
  z-index: 1999;
}
</style>