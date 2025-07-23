<template>
  <fui-bottom-popup :visible="visible" @close="handleClose">
    <view class="filter-modal">
      <view class="modal-header">
        <text class="modal-title">筛选条件</text>
        <view class="header-actions">
          <text class="reset-btn" @click="resetFilters">重置</text>
          <text class="confirm-btn" @click="applyFilters">确定</text>
        </view>
      </view>

      <scroll-view scroll-y class="filter-content">
        <!-- 内容类型 -->
        <view class="filter-section">
          <text class="section-title">内容类型</text>
          <view class="type-options">
            <view 
              v-for="type in contentTypes"
              :key="type.value"
              class="type-option"
              :class="{ active: selectedContentType === type.value }"
              @click="selectContentType(type.value)"
            >
              <fui-icon :name="type.icon" size="20" color="inherit" />
              <text class="type-name">{{ type.name }}</text>
              <fui-icon 
                name="check" 
                size="16" 
                color="#4CD964"
                v-if="selectedContentType === type.value"
              />
            </view>
          </view>
        </view>

        <!-- 分类筛选 -->
        <view class="filter-section">
          <text class="section-title">分类</text>
          <view class="category-grid">
            <view 
              v-for="category in categories"
              :key="category.id"
              class="category-option"
              :class="{ active: selectedCategories.includes(category.id) }"
              @click="toggleCategory(category.id)"
            >
              <fui-icon :name="category.icon" size="18" color="inherit" />
              <text class="category-name">{{ category.name }}</text>
            </view>
          </view>
        </view>

        <!-- 标签筛选 -->
        <view class="filter-section">
          <view class="section-header">
            <text class="section-title">标签</text>
            <text class="tag-count">已选 {{ selectedTags.length }} 个</text>
          </view>
          
          <!-- 搜索标签 -->
          <view class="tag-search">
            <fui-icon name="search" color="#8d96a0" size="16" />
            <input 
              class="search-input"
              placeholder="搜索标签"
              v-model="tagSearchQuery"
              @input="onTagSearch"
            />
          </view>

          <!-- 热门标签 -->
          <view class="popular-tags" v-if="!tagSearchQuery">
            <text class="subsection-title">热门标签</text>
            <view class="tag-list">
              <view 
                v-for="tag in popularTags"
                :key="tag.id"
                class="tag-chip"
                :class="{ active: selectedTags.includes(tag.id) }"
                @click="toggleTag(tag.id)"
              >
                <text class="tag-text">#{{ tag.name }}</text>
                <text class="tag-count">{{ tag.content_count }}</text>
              </view>
            </view>
          </view>

          <!-- 搜索结果标签 -->
          <view class="search-tags" v-if="tagSearchQuery && searchedTags.length">
            <text class="subsection-title">搜索结果</text>
            <view class="tag-list">
              <view 
                v-for="tag in searchedTags"
                :key="tag.id"
                class="tag-chip"
                :class="{ active: selectedTags.includes(tag.id) }"
                @click="toggleTag(tag.id)"
              >
                <text class="tag-text">#{{ tag.name }}</text>
                <text class="tag-count">{{ tag.content_count }}</text>
              </view>
            </view>
          </view>

          <!-- 已选标签 -->
          <view class="selected-tags" v-if="selectedTags.length">
            <text class="subsection-title">已选标签</text>
            <view class="tag-list">
              <view 
                v-for="tagId in selectedTags"
                :key="tagId"
                class="tag-chip active"
                @click="removeTag(tagId)"
              >
                <text class="tag-text">#{{ getTagName(tagId) }}</text>
                <fui-icon name="x" size="12" color="#fff" />
              </view>
            </view>
          </view>
        </view>

        <!-- 时间筛选 -->
        <view class="filter-section">
          <text class="section-title">发布时间</text>
          <view class="time-options">
            <view 
              v-for="timeOption in timeOptions"
              :key="timeOption.value"
              class="time-option"
              :class="{ active: selectedTimeRange === timeOption.value }"
              @click="selectTimeRange(timeOption.value)"
            >
              <text class="time-text">{{ timeOption.name }}</text>
            </view>
          </view>

          <!-- 自定义时间范围 -->
          <view class="custom-time" v-if="selectedTimeRange === 'custom'">
            <view class="date-picker-group">
              <text class="date-label">开始时间</text>
              <picker 
                mode="date" 
                :value="customDateRange.start"
                @change="onStartDateChange"
              >
                <view class="date-picker">
                  <text class="date-text">{{ customDateRange.start || '选择日期' }}</text>
                  <fui-icon name="calendar" color="#8d96a0" size="16" />
                </view>
              </picker>
            </view>
            
            <view class="date-picker-group">
              <text class="date-label">结束时间</text>
              <picker 
                mode="date" 
                :value="customDateRange.end"
                @change="onEndDateChange"
              >
                <view class="date-picker">
                  <text class="date-text">{{ customDateRange.end || '选择日期' }}</text>
                  <fui-icon name="calendar" color="#8d96a0" size="16" />
                </view>
              </picker>
            </view>
          </view>
        </view>

        <!-- 时长筛选 (音频/视频) -->
        <view class="filter-section" v-if="showDurationFilter">
          <text class="section-title">时长</text>
          <view class="duration-options">
            <view 
              v-for="duration in durationOptions"
              :key="duration.value"
              class="duration-option"
              :class="{ active: selectedDuration === duration.value }"
              @click="selectDuration(duration.value)"
            >
              <text class="duration-text">{{ duration.name }}</text>
            </view>
          </view>

          <!-- 自定义时长范围 -->
          <view class="custom-duration" v-if="selectedDuration === 'custom'">
            <text class="range-label">时长范围（分钟）</text>
            <view class="range-inputs">
              <input 
                type="number"
                class="range-input"
                placeholder="最小"
                v-model="customDurationRange.min"
              />
              <text class="range-separator">至</text>
              <input 
                type="number"
                class="range-input"
                placeholder="最大"
                v-model="customDurationRange.max"
              />
            </view>
          </view>
        </view>

        <!-- 排序选项 -->
        <view class="filter-section">
          <text class="section-title">排序方式</text>
          <view class="sort-options">
            <view 
              v-for="sort in sortOptions"
              :key="sort.value"
              class="sort-option"
              :class="{ active: selectedSort === sort.value }"
              @click="selectSort(sort.value)"
            >
              <fui-icon :name="sort.icon" size="18" color="inherit" />
              <text class="sort-text">{{ sort.name }}</text>
              <text class="sort-desc">{{ sort.description }}</text>
            </view>
          </view>
        </view>

        <!-- 其他筛选 -->
        <view class="filter-section">
          <text class="section-title">其他</text>
          <view class="other-options">
            <view class="option-item">
              <view class="option-info">
                <text class="option-name">仅显示有音频解说</text>
                <text class="option-desc">筛选包含AI语音解说的内容</text>
              </view>
              <switch 
                :checked="filters.hasAudio"
                @change="onHasAudioChange"
                color="#4CD964"
              />
            </view>

            <view class="option-item">
              <view class="option-info">
                <text class="option-name">仅显示已完结</text>
                <text class="option-desc">筛选系列内容中已完结的</text>
              </view>
              <switch 
                :checked="filters.isCompleted"
                @change="onIsCompletedChange"
                color="#4CD964"
              />
            </view>

            <view class="option-item">
              <view class="option-info">
                <text class="option-name">高质量内容</text>
                <text class="option-desc">仅显示编辑推荐的优质内容</text>
              </view>
              <switch 
                :checked="filters.isHighQuality"
                @change="onIsHighQualityChange"
                color="#4CD964"
              />
            </view>
          </view>
        </view>
      </scroll-view>

      <!-- 底部操作栏 -->
      <view class="modal-footer">
        <view class="filter-summary">
          <text class="summary-text">已选择 {{ getFilterCount() }} 个筛选条件</text>
        </view>
        <view class="footer-actions">
          <fui-button type="plain" @click="resetFilters">重置</fui-button>
          <fui-button type="primary" @click="applyFilters">应用筛选</fui-button>
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
  contentType: {
    type: String,
    default: 'all'
  },
  categories: {
    type: Array,
    default: () => []
  },
  tags: {
    type: Array,
    default: () => []
  },
  selectedCategories: {
    type: Array,
    default: () => []
  },
  selectedTags: {
    type: Array,
    default: () => []
  },
  dateRange: {
    type: Object,
    default: () => ({})
  },
  durationRange: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:visible', 'apply', 'reset'])

// 数据定义
const selectedContentType = ref('all')
const selectedCategories = ref([])
const selectedTags = ref([])
const selectedTimeRange = ref('all')
const selectedDuration = ref('all')
const selectedSort = ref('latest')

const tagSearchQuery = ref('')
const searchedTags = ref([])
const popularTags = ref([])

const customDateRange = ref({
  start: '',
  end: ''
})

const customDurationRange = ref({
  min: '',
  max: ''
})

const filters = ref({
  hasAudio: false,
  isCompleted: false,
  isHighQuality: false
})

// 配置数据
const contentTypes = [
  { name: '全部', value: 'all', icon: 'grid' },
  { name: '文章', value: 'article', icon: 'file-text' },
  { name: '视频', value: 'video', icon: 'video' },
  { name: '音频', value: 'audio', icon: 'headphones' }
]

const timeOptions = [
  { name: '全部时间', value: 'all' },
  { name: '今天', value: 'today' },
  { name: '本周', value: 'week' },
  { name: '本月', value: 'month' },
  { name: '最近三个月', value: '3months' },
  { name: '自定义', value: 'custom' }
]

const durationOptions = [
  { name: '全部时长', value: 'all' },
  { name: '5分钟以内', value: 'short' },
  { name: '5-20分钟', value: 'medium' },
  { name: '20-60分钟', value: 'long' },
  { name: '60分钟以上', value: 'verylong' },
  { name: '自定义', value: 'custom' }
]

const sortOptions = [
  { 
    name: '最新发布', 
    value: 'latest', 
    icon: 'clock',
    description: '按发布时间排序'
  },
  { 
    name: '最多播放', 
    value: 'popular', 
    icon: 'trending-up',
    description: '按播放量排序'
  },
  { 
    name: '最多点赞', 
    value: 'liked', 
    icon: 'heart',
    description: '按点赞数排序'
  },
  { 
    name: '最多收藏', 
    value: 'bookmarked', 
    icon: 'bookmark',
    description: '按收藏数排序'
  },
  { 
    name: '评分最高', 
    value: 'rating', 
    icon: 'star',
    description: '按用户评分排序'
  }
]

// 计算属性
const showDurationFilter = computed(() => {
  return selectedContentType.value === 'audio' || 
         selectedContentType.value === 'video' ||
         selectedContentType.value === 'all'
})

// 方法定义
const handleClose = () => {
  emit('update:visible', false)
}

const selectContentType = (type) => {
  selectedContentType.value = type
}

const toggleCategory = (categoryId) => {
  const index = selectedCategories.value.indexOf(categoryId)
  if (index > -1) {
    selectedCategories.value.splice(index, 1)
  } else {
    selectedCategories.value.push(categoryId)
  }
}

const toggleTag = (tagId) => {
  const index = selectedTags.value.indexOf(tagId)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(tagId)
  }
}

const removeTag = (tagId) => {
  const index = selectedTags.value.indexOf(tagId)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  }
}

const onTagSearch = async (e) => {
  const query = e.detail.value
  tagSearchQuery.value = query
  
  if (query.length > 0) {
    try {
      const response = await api.tags.search({
        q: query,
        content_type: selectedContentType.value,
        limit: 20
      })
      
      if (response.success) {
        searchedTags.value = response.data.tags
      }
    } catch (error) {
      console.error('搜索标签失败:', error)
    }
  } else {
    searchedTags.value = []
  }
}

const selectTimeRange = (range) => {
  selectedTimeRange.value = range
  if (range !== 'custom') {
    customDateRange.value = { start: '', end: '' }
  }
}

const selectDuration = (duration) => {
  selectedDuration.value = duration
  if (duration !== 'custom') {
    customDurationRange.value = { min: '', max: '' }
  }
}

const selectSort = (sort) => {
  selectedSort.value = sort
}

const onStartDateChange = (e) => {
  customDateRange.value.start = e.detail.value
}

const onEndDateChange = (e) => {
  customDateRange.value.end = e.detail.value
}

const onHasAudioChange = (e) => {
  filters.value.hasAudio = e.detail.value
}

const onIsCompletedChange = (e) => {
  filters.value.isCompleted = e.detail.value
}

const onIsHighQualityChange = (e) => {
  filters.value.isHighQuality = e.detail.value
}

const getTagName = (tagId) => {
  const tag = props.tags.find(t => t.id === tagId)
  return tag?.name || ''
}

const getFilterCount = () => {
  let count = 0
  
  if (selectedContentType.value !== 'all') count++
  count += selectedCategories.value.length
  count += selectedTags.value.length
  if (selectedTimeRange.value !== 'all') count++
  if (selectedDuration.value !== 'all') count++
  if (selectedSort.value !== 'latest') count++
  if (filters.value.hasAudio) count++
  if (filters.value.isCompleted) count++
  if (filters.value.isHighQuality) count++
  
  return count
}

const resetFilters = () => {
  selectedContentType.value = 'all'
  selectedCategories.value = []
  selectedTags.value = []
  selectedTimeRange.value = 'all'
  selectedDuration.value = 'all'
  selectedSort.value = 'latest'
  customDateRange.value = { start: '', end: '' }
  customDurationRange.value = { min: '', max: '' }
  filters.value = {
    hasAudio: false,
    isCompleted: false,
    isHighQuality: false
  }
  
  emit('reset')
}

const applyFilters = () => {
  const filterData = {
    contentType: selectedContentType.value,
    categories: selectedCategories.value,
    tags: selectedTags.value,
    timeRange: selectedTimeRange.value,
    duration: selectedDuration.value,
    sort: selectedSort.value,
    dateRange: selectedTimeRange.value === 'custom' ? customDateRange.value : {},
    durationRange: selectedDuration.value === 'custom' ? customDurationRange.value : {},
    ...filters.value
  }
  
  emit('apply', filterData)
}

const loadPopularTags = async () => {
  try {
    const response = await api.tags.getPopular({
      content_type: selectedContentType.value,
      limit: 15
    })
    
    if (response.success) {
      popularTags.value = response.data.tags
    }
  } catch (error) {
    console.error('加载热门标签失败:', error)
  }
}

// 监听器
watch(() => props.visible, (visible) => {
  if (visible) {
    // 初始化数据
    selectedContentType.value = props.contentType
    selectedCategories.value = [...props.selectedCategories]
    selectedTags.value = [...props.selectedTags]
    
    loadPopularTags()
  }
})

watch(selectedContentType, () => {
  loadPopularTags()
})

// 生命周期
onMounted(() => {
  loadPopularTags()
})
</script>

<style lang="scss" scoped>
.filter-modal {
  background: #ffffff;
  border-radius: 24rpx 24rpx 0 0;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx;
  border-bottom: 1px solid #eaedf0;
}

.modal-title {
  font-size: 36rpx;
  font-weight: 600;
  color: #2c3038;
}

.header-actions {
  display: flex;
  gap: 24rpx;
}

.reset-btn {
  font-size: 28rpx;
  color: #8d96a0;
}

.confirm-btn {
  font-size: 28rpx;
  color: #4CD964;
  font-weight: 500;
}

.filter-content {
  flex: 1;
  padding: 32rpx;
}

.filter-section {
  margin-bottom: 48rpx;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.section-title {
  display: block;
  font-size: 32rpx;
  font-weight: 600;
  color: #2c3038;
  margin-bottom: 24rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.tag-count {
  font-size: 24rpx;
  color: #8d96a0;
}

.type-options {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.type-option {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 20rpx 24rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
  border: 2px solid transparent;
  color: #2c3038;
  
  &.active {
    background: rgba(76, 217, 100, 0.1);
    border-color: #4CD964;
    color: #4CD964;
  }
}

.type-name {
  flex: 1;
  font-size: 28rpx;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16rpx;
}

.category-option {
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 20rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
  border: 2px solid transparent;
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
}

.tag-search {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 16rpx 20rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
  margin-bottom: 24rpx;
}

.search-input {
  flex: 1;
  font-size: 26rpx;
  color: #2c3038;
  
  &::placeholder {
    color: #8d96a0;
  }
}

.subsection-title {
  display: block;
  font-size: 26rpx;
  font-weight: 500;
  color: #5c6873;
  margin-bottom: 16rpx;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.tag-chip {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 12rpx 16rpx;
  background: #f8f9fa;
  border-radius: 16rpx;
  border: 1px solid transparent;
  transition: all 0.3s ease;
  
  &.active {
    background: #4CD964;
    color: #fff;
  }
}

.tag-text {
  font-size: 24rpx;
}

.tag-count {
  font-size: 20rpx;
  opacity: 0.8;
}

.time-options,
.duration-options {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.time-option,
.duration-option {
  padding: 16rpx 24rpx;
  background: #f8f9fa;
  border-radius: 20rpx;
  border: 1px solid transparent;
  font-size: 26rpx;
  color: #2c3038;
  transition: all 0.3s ease;
  
  &.active {
    background: rgba(76, 217, 100, 0.1);
    border-color: #4CD964;
    color: #4CD964;
  }
}

.custom-time,
.custom-duration {
  margin-top: 24rpx;
  padding: 24rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
}

.date-picker-group {
  margin-bottom: 16rpx;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.date-label {
  display: block;
  font-size: 26rpx;
  color: #5c6873;
  margin-bottom: 12rpx;
}

.date-picker {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16rpx 20rpx;
  background: #fff;
  border-radius: 8rpx;
  border: 1px solid #eaedf0;
}

.date-text {
  font-size: 26rpx;
  color: #2c3038;
}

.range-label {
  display: block;
  font-size: 26rpx;
  color: #5c6873;
  margin-bottom: 16rpx;
}

.range-inputs {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.range-input {
  flex: 1;
  padding: 16rpx 20rpx;
  background: #fff;
  border-radius: 8rpx;
  border: 1px solid #eaedf0;
  font-size: 26rpx;
  color: #2c3038;
  text-align: center;
}

.range-separator {
  font-size: 26rpx;
  color: #8d96a0;
}

.sort-options {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.sort-option {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 20rpx 24rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
  border: 2px solid transparent;
  color: #2c3038;
  
  &.active {
    background: rgba(76, 217, 100, 0.1);
    border-color: #4CD964;
    color: #4CD964;
  }
}

.sort-text {
  font-size: 28rpx;
  font-weight: 500;
}

.sort-desc {
  flex: 1;
  font-size: 24rpx;
  color: #8d96a0;
  margin-left: auto;
}

.other-options {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.option-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24rpx;
}

.option-info {
  flex: 1;
}

.option-name {
  display: block;
  font-size: 28rpx;
  color: #2c3038;
  margin-bottom: 4rpx;
}

.option-desc {
  font-size: 24rpx;
  color: #8d96a0;
}

.modal-footer {
  padding: 32rpx;
  border-top: 1px solid #eaedf0;
  background: #f8f9fa;
}

.filter-summary {
  margin-bottom: 24rpx;
  text-align: center;
}

.summary-text {
  font-size: 26rpx;
  color: #5c6873;
}

.footer-actions {
  display: flex;
  gap: 16rpx;
}
</style>