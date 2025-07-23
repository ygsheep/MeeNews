<template>
  <view class="search-page">
    <!-- 顶部搜索框 -->
    <view class="search-bar">
      <SearchBox v-model="keyword" placeholder="搜索音乐、艺术家、专辑" @search="onSearch" @clear="onClear" />
    </view>

    <!-- 搜索历史 -->
    <view class="history-section" v-if="historyList.length">
      <view class="section-title">
        <fui-icon name="clock" color="#8d96a0" size="20" />
        <text>搜索历史</text>
        <fui-icon name="delete" color="#8d96a0" size="20" class="clear-btn" @click="clearHistory" />
      </view>
      <view class="history-list">
        <view v-for="item in historyList" :key="item" class="history-item" @click="onHistoryClick(item)">{{ item }}</view>
      </view>
    </view>

    <!-- 热门搜索 -->
    <view class="hot-section">
      <view class="section-title">
        <fui-icon name="fire" color="#ff3b30" size="20" />
        <text>热门搜索</text>
      </view>
      <view class="hot-list">
        <view v-for="item in hotList" :key="item" class="hot-item" @click="onHotClick(item)">{{ item }}</view>
      </view>
    </view>

    <!-- 搜索结果 -->
    <view v-if="searching" class="result-section">
      <Skeleton v-if="loading" :rows="5" />
      <ErrorTip v-if="error" :message="error" />
      <ContentList v-if="!loading && !error" :list="resultList" cardType="list" direction="vertical" @itemClick="playContent" />
      <view v-if="!loading && !error && !resultList.length" class="empty-tip">暂无搜索结果</view>
    </view>
  </view>
</template>

<script>
import { ref, onMounted } from 'vue'
import SearchBox from '@/components/user/SearchBox.vue'
import ContentList from '@/components/content/ContentList.vue'
import Skeleton from '@/components/common/Skeleton.vue'
import ErrorTip from '@/components/common/ErrorTip.vue'

export default {
  name: 'Search',
  components: { SearchBox, ContentList, Skeleton, ErrorTip },
  setup() {
    const keyword = ref('')
    const historyList = ref([])
    const hotList = ref(['AI音乐', '流行', '电子', '古典', '摇滚', '爵士'])
    const resultList = ref([])
    const loading = ref(false)
    const error = ref('')
    const searching = ref(false)

    // 加载历史
    onMounted(() => {
      const h = uni.getStorageSync('search_history') || []
      historyList.value = h
    })

    // 搜索
    const onSearch = async (kw) => {
      if (!kw) return
      keyword.value = kw
      searching.value = true
      loading.value = true
      error.value = ''
      // 模拟请求
      setTimeout(() => {
        loading.value = false
        // mock 结果
        resultList.value = [
          { id: 1, title: kw + ' 热门歌曲', artist: 'AI歌手', coverUrl: '/static/images/common/img_logo.png', duration: 210 },
          { id: 2, title: kw + ' 推荐', artist: '流行歌手', coverUrl: '/static/images/common/img_logo.png', duration: 180 }
        ]
        // 存历史
        if (!historyList.value.includes(kw)) {
          historyList.value.unshift(kw)
          if (historyList.value.length > 10) historyList.value.pop()
          uni.setStorageSync('search_history', historyList.value)
        }
      }, 800)
    }
    // 清空输入
    const onClear = () => {
      keyword.value = ''
      searching.value = false
      resultList.value = []
    }
    // 点击历史
    const onHistoryClick = (kw) => {
      onSearch(kw)
    }
    // 点击热门
    const onHotClick = (kw) => {
      onSearch(kw)
    }
    // 清空历史
    const clearHistory = () => {
      historyList.value = []
      uni.removeStorageSync('search_history')
    }
    // 播放内容
    const playContent = (item) => {
      // 可对接播放器
      uni.showToast({ title: '播放 ' + item.title, icon: 'none' })
    }

    return {
      keyword,
      historyList,
      hotList,
      resultList,
      loading,
      error,
      searching,
      onSearch,
      onClear,
      onHistoryClick,
      onHotClick,
      clearHistory,
      playContent
    }
  }
}
</script>

<style lang="scss" scoped>
.search-page {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 0 32rpx;
}
.search-bar {
  padding: 32rpx 0 16rpx 0;
}
.section-title {
  display: flex;
  align-items: center;
  font-size: 26rpx;
  color: #8d96a0;
  margin: 24rpx 0 8rpx 0;
  gap: 12rpx;
}
.clear-btn {
  margin-left: auto;
  cursor: pointer;
}
.history-list, .hot-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  margin-bottom: 16rpx;
}
.history-item, .hot-item {
  background: #fff;
  border-radius: 32rpx;
  padding: 12rpx 32rpx;
  font-size: 26rpx;
  color: #2c3038;
  cursor: pointer;
  transition: background 0.2s;
}
.history-item:hover, .hot-item:hover {
  background: #4CD964;
  color: #fff;
}
.result-section {
  margin-top: 32rpx;
}
.empty-tip {
  text-align: center;
  color: #8d96a0;
  font-size: 28rpx;
  margin: 48rpx 0;
}
</style> 