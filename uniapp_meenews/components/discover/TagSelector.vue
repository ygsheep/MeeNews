<template>
  <fui-bottom-popup :visible="visible" @close="handleClose">
    <view class="tag-selector">
      <view class="selector-header">
        <text class="selector-title">选择标签</text>
        <view class="header-actions">
          <text class="clear-btn" @click="clearSelection">清空</text>
          <text class="confirm-btn" @click="confirmSelection">确定</text>
        </view>
      </view>

      <!-- 搜索框 -->
      <view class="search-section">
        <view class="search-container">
          <fui-icon name="search" color="#8d96a0" size="18" />
          <input 
            class="search-input"
            placeholder="搜索标签名称"
            v-model="searchQuery"
            @input="onSearchInput"
          />
          <fui-icon 
            name="x" 
            color="#8d96a0" 
            size="16"
            @click="clearSearch"
            v-if="searchQuery"
          />
        </view>
      </view>

      <!-- 已选标签 -->
      <view class="selected-section" v-if="selectedTags.length">
        <view class="section-header">
          <text class="section-title">已选择 ({{ selectedTags.length }})</text>
          <text class="select-limit">最多选择 {{ maxSelection }} 个</text>
        </view>
        
        <scroll-view scroll-x class="selected-scroll">
          <view class="selected-tags">
            <view 
              v-for="tagId in selectedTags"
              :key="`selected-${tagId}`"
              class="selected-tag"
              @click="removeTag(tagId)"
            >
              <text class="tag-name">#{{ getTagName(tagId) }}</text>
              <fui-icon name="x" size="12" color="#fff" />
            </view>
          </view>
        </scroll-view>
      </view>

      <!-- 标签列表 -->
      <scroll-view scroll-y class="tag-list-scroll">
        <!-- 搜索结果 -->
        <view class="search-results" v-if="searchQuery && searchResults.length">
          <text class="list-title">搜索结果</text>
          <view class="tag-grid">
            <view 
              v-for="tag in searchResults"
              :key="`search-${tag.id}`"
              class="tag-item"
              :class="{ 
                selected: selectedTags.includes(tag.id),
                disabled: isTagDisabled(tag.id)
              }"
              @click="toggleTag(tag.id)"
            >
              <text class="tag-text">#{{ tag.name }}</text>
              <text class="tag-count">{{ formatCount(tag.content_count) }}</text>
              <fui-icon 
                name="check" 
                size="14" 
                color="#4CD964"
                v-if="selectedTags.includes(tag.id)"
              />
            </view>
          </view>
        </view>

        <!-- 热门标签 -->
        <view class="popular-section" v-if="!searchQuery">
          <text class="list-title">热门标签</text>
          <view class="tag-grid">
            <view 
              v-for="tag in popularTags"
              :key="`popular-${tag.id}`"
              class="tag-item popular"
              :class="{ 
                selected: selectedTags.includes(tag.id),
                disabled: isTagDisabled(tag.id)
              }"
              @click="toggleTag(tag.id)"
            >
              <view class="tag-info">
                <text class="tag-text">#{{ tag.name }}</text>
                <text class="tag-count">{{ formatCount(tag.content_count) }}</text>
              </view>
              <view class="tag-meta">
                <view class="hot-badge">
                  <fui-icon name="trending-up" size="10" color="#ff9500" />
                  <text class="hot-text">热门</text>
                </view>
                <fui-icon 
                  name="check" 
                  size="14" 
                  color="#4CD964"
                  v-if="selectedTags.includes(tag.id)"
                />
              </view>
            </view>
          </view>
        </view>

        <!-- 分类标签 -->
        <view class="category-sections" v-if="!searchQuery">
          <view 
            v-for="category in tagCategories"
            :key="category.id"
            class="category-section"
          >
            <view class="category-header" @click="toggleCategory(category.id)">
              <view class="category-info">
                <fui-icon :name="category.icon" size="18" color="#5c6873" />
                <text class="category-name">{{ category.name }}</text>
                <text class="category-count">({{ category.tags?.length || 0 }})</text>
              </view>
              <fui-icon 
                :name="expandedCategories.includes(category.id) ? 'chevron-down' : 'chevron-right'" 
                size="16" 
                color="#8d96a0"
              />
            </view>

            <view class="category-tags" v-if="expandedCategories.includes(category.id)">
              <view class="tag-grid">
                <view 
                  v-for="tag in category.tags"
                  :key="`category-${tag.id}`"
                  class="tag-item"
                  :class="{ 
                    selected: selectedTags.includes(tag.id),
                    disabled: isTagDisabled(tag.id)
                  }"
                  @click="toggleTag(tag.id)"
                >
                  <text class="tag-text">#{{ tag.name }}</text>
                  <text class="tag-count">{{ formatCount(tag.content_count) }}</text>
                  <fui-icon 
                    name="check" 
                    size="14" 
                    color="#4CD964"
                    v-if="selectedTags.includes(tag.id)"
                  />
                </view>
              </view>
            </view>
          </view>
        </view>

        <!-- 所有标签 -->
        <view class="all-tags-section" v-if="!searchQuery && showAllTags">
          <view class="section-header">
            <text class="list-title">所有标签</text>
            <picker 
              :range="sortOptions" 
              range-key="name"
              @change="onSortChange"
            >
              <view class="sort-selector">
                <text class="sort-text">{{ currentSort.name }}</text>
                <fui-icon name="chevron-down" size="14" color="#8d96a0" />
              </view>
            </picker>
          </view>
          
          <view class="tag-grid">
            <view 
              v-for="tag in sortedAllTags"
              :key="`all-${tag.id}`"
              class="tag-item"
              :class="{ 
                selected: selectedTags.includes(tag.id),
                disabled: isTagDisabled(tag.id)
              }"
              @click="toggleTag(tag.id)"
            >
              <text class="tag-text">#{{ tag.name }}</text>
              <text class="tag-count">{{ formatCount(tag.content_count) }}</text>
              <fui-icon 
                name="check" 
                size="14" 
                color="#4CD964"
                v-if="selectedTags.includes(tag.id)"
              />
            </view>
          </view>

          <view class="load-more" v-if="hasMoreTags">
            <fui-button 
              type="plain" 
              size="small"
              :loading="loadingMore"
              @click="loadMoreTags"
            >
              加载更多
            </fui-button>
          </view>
        </view>

        <!-- 显示所有标签按钮 -->
        <view class="show-all-btn" v-if="!searchQuery && !showAllTags">
          <fui-button type="plain" @click="toggleShowAllTags">
            显示所有标签
          </fui-button>
        </view>

        <!-- 空状态 -->
        <view class="empty-state" v-if="showEmptyState">
          <fui-icon name="tag" color="#c7c7cc" size="48" />
          <text class="empty-title">{{ getEmptyTitle() }}</text>
          <text class="empty-desc">{{ getEmptyDescription() }}</text>
        </view>
      </scroll-view>

      <!-- 底部操作栏 -->
      <view class="selector-footer">
        <view class="selection-info">
          <text class="selection-count">已选择 {{ selectedTags.length }}/{{ maxSelection }}</text>
          <view class="selection-progress">
            <view 
              class="progress-fill"
              :style="{ width: `${(selectedTags.length / maxSelection) * 100}%` }"
            ></view>
          </view>
        </view>
        
        <view class="footer-actions">
          <fui-button type="plain" @click="handleClose">取消</fui-button>
          <fui-button 
            type="primary" 
            @click="confirmSelection"
            :disabled="selectedTags.length === 0"
          >
            确定选择
          </fui-button>
        </view>
      </view>
    </view>
  </fui-bottom-popup>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  tags: {
    type: Array,
    default: () => []
  },
  selected: {
    type: Array,
    default: () => []
  },
  maxSelection: {
    type: Number,
    default: 10
  },
  contentType: {
    type: String,
    default: 'all'
  }
})

const emit = defineEmits(['update:visible', 'confirm'])

// 数据定义
const selectedTags = ref([])
const searchQuery = ref('')
const searchResults = ref([])
const popularTags = ref([])
const allTags = ref([])
const tagCategories = ref([])
const expandedCategories = ref([])
const showAllTags = ref(false)
const loadingMore = ref(false)
const hasMoreTags = ref(false)
const currentPage = ref(1)

const currentSort = ref({ name: '热度', value: 'popular' })

const sortOptions = [
  { name: '热度', value: 'popular' },
  { name: '名称', value: 'name' },
  { name: '内容数', value: 'content_count' },
  { name: '最新', value: 'latest' }
]

// 计算属性
const isTagDisabled = computed(() => (tagId) => {
  return !selectedTags.value.includes(tagId) && 
         selectedTags.value.length >= props.maxSelection
})

const sortedAllTags = computed(() => {
  const tags = [...allTags.value]
  const sortValue = currentSort.value.value
  
  return tags.sort((a, b) => {
    switch (sortValue) {
      case 'name':
        return a.name.localeCompare(b.name)
      case 'content_count':
        return b.content_count - a.content_count
      case 'latest':
        return new Date(b.created_at) - new Date(a.created_at)
      case 'popular':
      default:
        return b.popularity_score - a.popularity_score
    }
  })
})

const showEmptyState = computed(() => {
  if (searchQuery.value) {
    return searchResults.value.length === 0
  }
  return allTags.value.length === 0
})

// 方法定义
const handleClose = () => {
  emit('update:visible', false)
}

const clearSelection = () => {
  selectedTags.value = []
}

const clearSearch = () => {
  searchQuery.value = ''
  searchResults.value = []
}

const confirmSelection = () => {
  emit('confirm', selectedTags.value)
  handleClose()
}

const toggleTag = (tagId) => {
  if (isTagDisabled.value(tagId)) return
  
  const index = selectedTags.value.indexOf(tagId)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    if (selectedTags.value.length < props.maxSelection) {
      selectedTags.value.push(tagId)
    }
  }
}

const removeTag = (tagId) => {
  const index = selectedTags.value.indexOf(tagId)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  }
}

const toggleCategory = (categoryId) => {
  const index = expandedCategories.value.indexOf(categoryId)
  if (index > -1) {
    expandedCategories.value.splice(index, 1)
  } else {
    expandedCategories.value.push(categoryId)
  }
}

const toggleShowAllTags = () => {
  showAllTags.value = !showAllTags.value
  if (showAllTags.value && allTags.value.length === 0) {
    loadAllTags()
  }
}

const onSearchInput = (e) => {
  const query = e.detail.value
  searchQuery.value = query
  debounceSearch(query)
}

const debounceSearch = debounce(async (query) => {
  if (query.length === 0) {
    searchResults.value = []
    return
  }
  
  try {
    const response = await api.tags.search({
      q: query,
      content_type: props.contentType,
      limit: 50
    })
    
    if (response.success) {
      searchResults.value = response.data.tags
    }
  } catch (error) {
    console.error('搜索标签失败:', error)
  }
}, 300)

const onSortChange = (e) => {
  currentSort.value = sortOptions[e.detail.value]
}

const loadPopularTags = async () => {
  try {
    const response = await api.tags.getPopular({
      content_type: props.contentType,
      limit: 20
    })
    
    if (response.success) {
      popularTags.value = response.data.tags
    }
  } catch (error) {
    console.error('加载热门标签失败:', error)
  }
}

const loadTagCategories = async () => {
  try {
    const response = await api.tags.getCategories({
      content_type: props.contentType
    })
    
    if (response.success) {
      tagCategories.value = response.data.categories
      // 默认展开前两个分类
      expandedCategories.value = response.data.categories.slice(0, 2).map(c => c.id)
    }
  } catch (error) {
    console.error('加载标签分类失败:', error)
  }
}

const loadAllTags = async (page = 1) => {
  try {
    loadingMore.value = page > 1
    
    const response = await api.tags.getAll({
      content_type: props.contentType,
      sort: currentSort.value.value,
      page,
      page_size: 50
    })
    
    if (response.success) {
      if (page === 1) {
        allTags.value = response.data.tags
      } else {
        allTags.value.push(...response.data.tags)
      }
      
      hasMoreTags.value = response.data.has_more
      currentPage.value = page
    }
  } catch (error) {
    console.error('加载所有标签失败:', error)
  } finally {
    loadingMore.value = false
  }
}

const loadMoreTags = () => {
  if (!loadingMore.value && hasMoreTags.value) {
    loadAllTags(currentPage.value + 1)
  }
}

const getTagName = (tagId) => {
  const allTagsList = [
    ...popularTags.value,
    ...allTags.value,
    ...searchResults.value,
    ...tagCategories.value.flatMap(c => c.tags || [])
  ]
  
  const tag = allTagsList.find(t => t.id === tagId)
  return tag?.name || ''
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

const getEmptyTitle = () => {
  return searchQuery.value ? '没有找到相关标签' : '暂无标签'
}

const getEmptyDescription = () => {
  return searchQuery.value ? '尝试使用其他关键词搜索' : '暂时没有可用的标签'
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

// 监听器
watch(() => props.visible, (visible) => {
  if (visible) {
    selectedTags.value = [...props.selected]
    loadPopularTags()
    loadTagCategories()
  }
})

watch(currentSort, () => {
  if (showAllTags.value) {
    loadAllTags(1)
  }
})

// 生命周期
onMounted(() => {
  if (props.visible) {
    selectedTags.value = [...props.selected]
    loadPopularTags()
    loadTagCategories()
  }
})
</script>

<style lang="scss" scoped>
.tag-selector {
  background: #ffffff;
  border-radius: 24rpx 24rpx 0 0;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.selector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx;
  border-bottom: 1px solid #eaedf0;
}

.selector-title {
  font-size: 36rpx;
  font-weight: 600;
  color: #2c3038;
}

.header-actions {
  display: flex;
  gap: 24rpx;
}

.clear-btn {
  font-size: 28rpx;
  color: #8d96a0;
}

.confirm-btn {
  font-size: 28rpx;
  color: #4CD964;
  font-weight: 500;
}

.search-section {
  padding: 24rpx 32rpx;
  border-bottom: 1px solid #f0f0f0;
}

.search-container {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 16rpx 20rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
}

.search-input {
  flex: 1;
  font-size: 26rpx;
  color: #2c3038;
  
  &::placeholder {
    color: #8d96a0;
  }
}

.selected-section {
  padding: 24rpx 32rpx;
  border-bottom: 1px solid #f0f0f0;
  background: #f8f9fa;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.section-title {
  font-size: 28rpx;
  font-weight: 500;
  color: #2c3038;
}

.select-limit {
  font-size: 24rpx;
  color: #8d96a0;
}

.selected-scroll {
  white-space: nowrap;
}

.selected-tags {
  display: flex;
  gap: 12rpx;
}

.selected-tag {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 16rpx;
  background: #4CD964;
  color: #fff;
  border-radius: 16rpx;
  white-space: nowrap;
}

.tag-name {
  font-size: 24rpx;
}

.tag-list-scroll {
  flex: 1;
  padding: 24rpx 32rpx;
}

.list-title {
  display: block;
  font-size: 28rpx;
  font-weight: 500;
  color: #2c3038;
  margin-bottom: 20rpx;
}

.tag-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16rpx;
  margin-bottom: 32rpx;
}

.tag-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16rpx 20rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  
  &.selected {
    background: rgba(76, 217, 100, 0.1);
    border-color: #4CD964;
  }
  
  &.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  &.popular {
    flex-direction: column;
    align-items: stretch;
    gap: 12rpx;
  }
}

.tag-text {
  font-size: 26rpx;
  color: #2c3038;
  font-weight: 500;
}

.tag-count {
  font-size: 22rpx;
  color: #8d96a0;
}

.tag-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tag-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hot-badge {
  display: flex;
  align-items: center;
  gap: 4rpx;
  padding: 4rpx 8rpx;
  background: rgba(255, 149, 0, 0.1);
  border-radius: 8rpx;
}

.hot-text {
  font-size: 20rpx;
  color: #ff9500;
}

.category-section {
  margin-bottom: 32rpx;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16rpx 20rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
  margin-bottom: 16rpx;
}

.category-info {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.category-name {
  font-size: 28rpx;
  font-weight: 500;
  color: #2c3038;
}

.category-count {
  font-size: 24rpx;
  color: #8d96a0;
}

.category-tags {
  margin-left: 16rpx;
}

.all-tags-section {
  margin-top: 32rpx;
}

.sort-selector {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 16rpx;
  background: #f8f9fa;
  border-radius: 8rpx;
}

.sort-text {
  font-size: 24rpx;
  color: #5c6873;
}

.load-more {
  text-align: center;
  margin-top: 24rpx;
}

.show-all-btn {
  text-align: center;
  margin-top: 24rpx;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80rpx 40rpx;
  text-align: center;
}

.empty-title {
  font-size: 32rpx;
  color: #5c6873;
  margin: 24rpx 0 16rpx;
}

.empty-desc {
  font-size: 26rpx;
  color: #8d96a0;
  line-height: 1.5;
}

.selector-footer {
  padding: 24rpx 32rpx;
  border-top: 1px solid #eaedf0;
  background: #f8f9fa;
}

.selection-info {
  margin-bottom: 20rpx;
}

.selection-count {
  display: block;
  font-size: 24rpx;
  color: #5c6873;
  margin-bottom: 12rpx;
}

.selection-progress {
  height: 6rpx;
  background: #eaedf0;
  border-radius: 3rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #4CD964;
  border-radius: 3rpx;
  transition: width 0.3s ease;
}

.footer-actions {
  display: flex;
  gap: 16rpx;
}
</style>