# 羊咩快报 - UniApp前端页面设计

## 前端架构概述

基于UniApp框架开发，支持多端发布(小程序、H5、APP)。采用Vue.js 3.0语法，集成FirstUI组件库，实现现代化的音频媒体应用界面。

## 技术栈

- **框架**: UniApp + Vue.js 3.0
- **UI库**: FirstUI (已集成)
- **状态管理**: Pinia (Vue 3 推荐)
- **路由**: UniApp 内置路由
- **音频播放**: uni-app 音频API + 第三方插件
- **网络请求**: Axios + uni.request 封装
- **图标**: FirstUI图标库 + Iconfont

## 项目目录结构

```
yangmie-uniapp/
├── pages/                      # 页面目录
│   ├── index/                  # 首页
│   │   └── index.vue
│   ├── discover/               # 发现页
│   │   ├── discover.vue
│   │   ├── category.vue
│   │   └── search.vue
│   ├── player/                 # 播放相关
│   │   ├── player.vue
│   │   ├── playlist.vue
│   │   └── lyrics.vue
│   ├── library/                # 音乐库
│   │   ├── library.vue
│   │   ├── favorites.vue
│   │   ├── history.vue
│   │   └── downloads.vue
│   ├── profile/                # 个人中心
│   │   ├── profile.vue
│   │   ├── settings.vue
│   │   ├── edit-profile.vue
│   │   └── about.vue
│   ├── artist/                 # 艺术家
│   │   ├── detail.vue
│   │   └── list.vue
│   ├── album/                  # 专辑
│   │   ├── detail.vue
│   │   └── list.vue
│   └── auth/                   # 认证相关
│       ├── login.vue
│       ├── register.vue
│       └── forgot-password.vue
├── components/                 # 组件目录
│   ├── common/                 # 通用组件
│   │   ├── TabBar.vue
│   │   ├── NavBar.vue
│   │   ├── Loading.vue
│   │   ├── Empty.vue
│   │   └── BackToTop.vue
│   ├── player/                 # 播放器组件
│   │   ├── MiniPlayer.vue
│   │   ├── PlayerControls.vue
│   │   ├── ProgressBar.vue
│   │   ├── VolumeControl.vue
│   │   └── PlaylistModal.vue
│   ├── content/                # 内容组件
│   │   ├── ContentCard.vue
│   │   ├── ContentList.vue
│   │   ├── ArtistCard.vue
│   │   ├── AlbumCard.vue
│   │   └── CategoryGrid.vue
│   ├── user/                   # 用户组件
│   │   ├── UserAvatar.vue
│   │   ├── UserStats.vue
│   │   └── FollowButton.vue
│   └── form/                   # 表单组件
│       ├── SearchBox.vue
│       ├── RatingStars.vue
│       └── TagSelector.vue
├── static/                     # 静态资源
│   ├── images/
│   ├── icons/
│   └── audio/
├── store/                      # 状态管理
│   ├── index.js
│   ├── modules/
│   │   ├── user.js
│   │   ├── player.js
│   │   ├── content.js
│   │   └── app.js
├── utils/                      # 工具函数
│   ├── request.js
│   ├── auth.js
│   ├── storage.js
│   ├── player.js
│   ├── format.js
│   └── constants.js
├── styles/                     # 样式文件
│   ├── common.scss
│   ├── variables.scss
│   ├── mixins.scss
│   └── themes/
│       ├── light.scss
│       └── dark.scss
├── api/                        # API接口
│   ├── index.js
│   ├── auth.js
│   ├── user.js
│   ├── content.js
│   ├── player.js
│   └── ai.js
├── App.vue                     # 根组件
├── main.js                     # 入口文件
├── manifest.json               # 应用配置
├── pages.json                  # 路由配置
└── uni.scss                    # 全局样式
```

---

## 页面设计详细说明

### 1. 底部导航 (TabBar)

基于UI设计稿，应用采用底部Tab导航模式：

#### pages.json 配置
```json
{
  "pages": [
    {
      "path": "pages/index/index",
      "style": {
        "navigationBarTitleText": "首页"
      }
    },
    {
      "path": "pages/discover/discover",
      "style": {
        "navigationBarTitleText": "发现"
      }
    },
    {
      "path": "pages/library/library",
      "style": {
        "navigationBarTitleText": "音乐库"
      }
    },
    {
      "path": "pages/profile/profile",
      "style": {
        "navigationBarTitleText": "我的"
      }
    }
  ],
  "tabBar": {
    "color": "#8d96a0",
    "selectedColor": "#4CD964",
    "backgroundColor": "#ffffff",
    "borderStyle": "black",
    "list": [
      {
        "pagePath": "pages/index/index",
        "iconPath": "static/icons/home-default.png",
        "selectedIconPath": "static/icons/home-selected.png",
        "text": "首页"
      },
      {
        "pagePath": "pages/discover/discover",
        "iconPath": "static/icons/discover-default.png",
        "selectedIconPath": "static/icons/discover-selected.png",
        "text": "发现"
      },
      {
        "pagePath": "pages/library/library",
        "iconPath": "static/icons/library-default.png",
        "selectedIconPath": "static/icons/library-selected.png",
        "text": "音乐库"
      },
      {
        "pagePath": "pages/profile/profile",
        "iconPath": "static/icons/profile-default.png",
        "selectedIconPath": "static/icons/profile-selected.png",
        "text": "我的"
      }
    ]
  }
}
```

### 2. 首页 (index/index.vue)

首页展示个性化推荐内容，包含问候语、分类导航、推荐内容等模块。

#### 页面结构
```vue
<template>
  <view class="index-page">
    <!-- 顶部导航 -->
    <NavBar :show-back="false">
      <template #left>
        <fui-icon name="menu" color="#333" size="24"></fui-icon>
      </template>
      <template #center>
        <text class="nav-title">羊咩快报</text>
      </template>
      <template #right>
        <fui-icon name="search" color="#333" size="24" @click="goToSearch"></fui-icon>
      </template>
    </NavBar>

    <!-- 问候语部分 -->
    <view class="greeting-section">
      <text class="greeting-text">{{ greetingText }}</text>
      <fui-icon name="star" color="#FFD700" size="16"></fui-icon>
    </view>

    <!-- 分类导航 -->
    <scroll-view scroll-x class="category-scroll">
      <view class="category-nav">
        <view 
          v-for="(category, index) in categories" 
          :key="category.id"
          class="category-item"
          :class="{ active: activeCategory === index }"
          @click="selectCategory(index)"
        >
          <text class="category-text">{{ category.name }}</text>
        </view>
      </view>
    </scroll-view>

    <!-- 推荐内容 -->
    <view class="content-sections">
      <!-- 最近播放 -->
      <ContentSection 
        title="最近播放"
        :show-more="true"
        @more="goToHistory"
      >
        <scroll-view scroll-x class="horizontal-scroll">
          <view class="content-list horizontal">
            <ContentCard 
              v-for="item in recentPlayed"
              :key="item.id"
              :content="item"
              card-type="small"
              @click="playContent(item)"
            />
          </view>
        </scroll-view>
      </ContentSection>

      <!-- 推荐艺术家 -->
      <ContentSection 
        title="推荐艺术家"
        :show-more="true"
        @more="goToArtists"
      >
        <scroll-view scroll-x class="horizontal-scroll">
          <view class="artist-list horizontal">
            <ArtistCard 
              v-for="artist in recommendedArtists"
              :key="artist.id"
              :artist="artist"
              @click="goToArtist(artist.id)"
            />
          </view>
        </scroll-view>
      </ContentSection>

      <!-- 为你推荐 -->
      <ContentSection 
        title="为你推荐"
        :show-more="true"
        @more="goToRecommend"
      >
        <view class="content-list vertical">
          <ContentCard 
            v-for="item in recommendedContent"
            :key="item.id"
            :content="item"
            card-type="list"
            @click="playContent(item)"
          />
        </view>
      </ContentSection>
    </view>

    <!-- 迷你播放器 -->
    <MiniPlayer v-if="currentTrack" />
  </view>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from '@/store'
import NavBar from '@/components/common/NavBar.vue'
import ContentSection from '@/components/content/ContentSection.vue'
import ContentCard from '@/components/content/ContentCard.vue'
import ArtistCard from '@/components/content/ArtistCard.vue'
import MiniPlayer from '@/components/player/MiniPlayer.vue'

const store = useStore()

// 数据定义
const categories = ref([
  { id: 0, name: '推荐' },
  { id: 1, name: '音乐' },
  { id: 2, name: '播客' },
  { id: 3, name: '新闻' },
  { id: 4, name: '有声书' }
])

const activeCategory = ref(0)
const recentPlayed = ref([])
const recommendedArtists = ref([])
const recommendedContent = ref([])

// 计算属性
const greetingText = computed(() => {
  const hour = new Date().getHours()
  const username = store.user.userInfo?.nickname || 'Phillip'
  
  if (hour < 12) return `Good Morning, ${username}`
  if (hour < 18) return `Good Afternoon, ${username}`
  return `Good Evening, ${username}`
})

const currentTrack = computed(() => store.player.currentTrack)

// 方法定义
const selectCategory = (index) => {
  activeCategory.value = index
  loadContentByCategory(categories.value[index].id)
}

const loadContentByCategory = async (categoryId) => {
  // 根据分类加载内容
}

const playContent = (content) => {
  store.player.playTrack(content)
}

const goToSearch = () => {
  uni.navigateTo({ url: '/pages/discover/search' })
}

const goToHistory = () => {
  uni.navigateTo({ url: '/pages/library/history' })
}

const goToArtists = () => {
  uni.navigateTo({ url: '/pages/artist/list' })
}

const goToArtist = (artistId) => {
  uni.navigateTo({ url: `/pages/artist/detail?id=${artistId}` })
}

const goToRecommend = () => {
  uni.navigateTo({ url: '/pages/discover/recommend' })
}

// 生命周期
onMounted(() => {
  loadRecentPlayed()
  loadRecommendedArtists()
  loadRecommendedContent()
})

const loadRecentPlayed = async () => {
  // 加载最近播放
}

const loadRecommendedArtists = async () => {
  // 加载推荐艺术家
}

const loadRecommendedContent = async () => {
  // 加载推荐内容
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
      color: #ffffff;
    }
  }
  
  .category-text {
    font-size: 28rpx;
    color: #2c3038;
    font-weight: 500;
  }
}

.content-sections {
  padding-bottom: 160rpx; // 为底部播放器留空间
}

.horizontal-scroll {
  white-space: nowrap;
}

.content-list {
  display: flex;
  gap: 24rpx;
  
  &.horizontal {
    padding: 0 32rpx;
  }
  
  &.vertical {
    flex-direction: column;
    padding: 0 32rpx;
  }
}

.artist-list {
  display: flex;
  gap: 32rpx;
  padding: 0 32rpx;
}
</style>
```

### 3. 发现页 (discover/discover.vue)

发现页提供搜索功能和内容分类浏览。

#### 页面结构
```vue
<template>
  <view class="discover-page">
    <!-- 搜索框 -->
    <view class="search-section">
      <SearchBox 
        placeholder="搜索音乐、艺术家、专辑"
        @search="handleSearch"
        @focus="goToSearch"
      />
    </view>

    <!-- 分类网格 -->
    <view class="category-grid">
      <view 
        v-for="category in categories"
        :key="category.id"
        class="category-card"
        :style="{ backgroundColor: category.color_code }"
        @click="goToCategory(category.id)"
      >
        <image :src="category.icon_url" class="category-icon" />
        <text class="category-name">{{ category.name }}</text>
      </view>
    </view>

    <!-- 榜单推荐 -->
    <ContentSection title="热门榜单">
      <view class="chart-list">
        <view 
          v-for="chart in charts"
          :key="chart.id"
          class="chart-item"
          @click="goToChart(chart.id)"
        >
          <image :src="chart.cover_url" class="chart-cover" />
          <view class="chart-info">
            <text class="chart-title">{{ chart.title }}</text>
            <text class="chart-desc">{{ chart.description }}</text>
          </view>
          <fui-icon name="arrow-right" color="#8d96a0" size="20" />
        </view>
      </view>
    </ContentSection>

    <!-- 新音乐 -->
    <ContentSection title="最新音乐" :show-more="true">
      <view class="content-list">
        <ContentCard 
          v-for="item in newMusic"
          :key="item.id"
          :content="item"
          card-type="list"
          @click="playContent(item)"
        />
      </view>
    </ContentSection>
  </view>
</template>
```

### 4. 播放页面 (player/player.vue)

全屏播放界面，包含专辑封面、播放控制、歌词等功能。

#### 页面结构
```vue
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
          <text class="source-name">{{ currentPlaylist?.name || '推荐音乐' }}</text>
        </view>
      </template>
      <template #right>
        <fui-icon name="more" color="#fff" size="24" @click="showMoreActions" />
      </template>
    </NavBar>

    <!-- 专辑封面 -->
    <view class="cover-section">
      <view class="cover-container" :class="{ playing: isPlaying }">
        <image 
          :src="currentTrack?.cover_url" 
          class="cover-image"
          mode="aspectFill"
        />
        <!-- 音频可视化效果 -->
        <view class="audio-visualizer" v-if="isPlaying">
          <view class="wave-bar" v-for="i in 20" :key="i"></view>
        </view>
      </view>
    </view>

    <!-- 歌曲信息 -->
    <view class="track-info">
      <text class="track-title">{{ currentTrack?.title }}</text>
      <text class="track-artist">{{ currentTrack?.artist?.name }}</text>
    </view>

    <!-- 进度条 -->
    <view class="progress-section">
      <text class="time-text">{{ formatTime(currentTime) }}</text>
      <ProgressBar 
        :current="currentTime"
        :total="duration"
        @seek="handleSeek"
      />
      <text class="time-text">{{ formatTime(duration) }}</text>
    </view>

    <!-- 播放控制 -->
    <view class="controls-section">
      <fui-icon 
        name="skip-back-15" 
        color="#fff" 
        size="32"
        @click="skipBackward"
      />
      <fui-icon 
        name="skip-previous" 
        color="#fff" 
        size="36"
        @click="playPrevious"
      />
      <view class="play-button" @click="togglePlay">
        <fui-icon 
          :name="isPlaying ? 'pause' : 'play'" 
          color="#fff" 
          size="28"
        />
      </view>
      <fui-icon 
        name="skip-next" 
        color="#fff" 
        size="36"
        @click="playNext"
      />
      <fui-icon 
        name="skip-forward-30" 
        color="#fff" 
        size="32"
        @click="skipForward"
      />
    </view>

    <!-- 底部功能区 -->
    <view class="bottom-actions">
      <fui-icon 
        name="shuffle" 
        :color="shuffleMode ? '#4CD964' : '#8d96a0'" 
        size="24"
        @click="toggleShuffle"
      />
      <fui-icon 
        name="volume" 
        color="#8d96a0" 
        size="24"
        @click="showVolumeControl"
      />
      <fui-icon 
        name="share" 
        color="#8d96a0" 
        size="24"
        @click="shareTrack"
      />
      <text class="swipe-hint">向上滑动查看歌词</text>
    </view>

    <!-- 歌词页面 (滑动弹出) -->
    <LyricsModal 
      v-if="showLyrics"
      :lyrics="currentTrack?.lyrics"
      :current-time="currentTime"
      @close="showLyrics = false"
    />
  </view>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useStore } from '@/store'
import NavBar from '@/components/common/NavBar.vue'
import ProgressBar from '@/components/player/ProgressBar.vue'
import LyricsModal from '@/components/player/LyricsModal.vue'

const store = useStore()

// 状态数据
const showLyrics = ref(false)
const currentTime = ref(0)
const timer = ref(null)

// 计算属性
const currentTrack = computed(() => store.player.currentTrack)
const currentPlaylist = computed(() => store.player.currentPlaylist)
const isPlaying = computed(() => store.player.isPlaying)
const duration = computed(() => store.player.duration)
const shuffleMode = computed(() => store.player.shuffleMode)

// 方法
const minimize = () => {
  uni.navigateBack()
}

const togglePlay = () => {
  store.player.togglePlay()
}

const playPrevious = () => {
  store.player.playPrevious()
}

const playNext = () => {
  store.player.playNext()
}

const skipBackward = () => {
  store.player.seek(currentTime.value - 15)
}

const skipForward = () => {
  store.player.seek(currentTime.value + 30)
}

const handleSeek = (time) => {
  store.player.seek(time)
}

const toggleShuffle = () => {
  store.player.toggleShuffle()
}

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 生命周期
onMounted(() => {
  // 启动定时器更新播放进度
  timer.value = setInterval(() => {
    if (isPlaying.value) {
      currentTime.value = store.player.getCurrentTime()
    }
  }, 1000)
})

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
})
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

.audio-visualizer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100rpx;
  background: linear-gradient(to top, rgba(0,0,0,0.6), transparent);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 8rpx;
  padding: 0 40rpx 20rpx;
}

.wave-bar {
  width: 6rpx;
  background: #fff;
  border-radius: 3rpx;
  animation: wave 1s infinite ease-in-out;
  
  &:nth-child(2n) { animation-delay: 0.1s; }
  &:nth-child(3n) { animation-delay: 0.2s; }
  &:nth-child(4n) { animation-delay: 0.3s; }
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

.controls-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 80rpx;
  margin-bottom: 80rpx;
}

.play-button {
  width: 120rpx;
  height: 120rpx;
  border-radius: 60rpx;
  background-color: #4CD964;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 24rpx rgba(76, 217, 100, 0.4);
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

@keyframes wave {
  0%, 100% { height: 20rpx; }
  50% { height: 60rpx; }
}
</style>
```

### 5. 音乐库页面 (library/library.vue)

用户的个人音乐收藏和历史记录。

#### 页面结构
```vue
<template>
  <view class="library-page">
    <!-- 用户信息卡片 -->
    <view class="user-card" v-if="userInfo">
      <image :src="userInfo.avatar_url" class="user-avatar" />
      <view class="user-info">
        <text class="user-name">{{ userInfo.nickname }}</text>
        <text class="user-stats">已听 {{ userStats.total_plays }} 首歌</text>
      </view>
      <fui-icon name="edit" color="#8d96a0" size="20" @click="editProfile" />
    </view>

    <!-- 功能菜单 -->
    <view class="menu-section">
      <view class="menu-item" @click="goToFavorites">
        <fui-icon name="heart" color="#ff3b30" size="24" />
        <text class="menu-text">我喜欢的音乐</text>
        <text class="menu-count">{{ favoriteCount }}</text>
        <fui-icon name="arrow-right" color="#8d96a0" size="16" />
      </view>
      
      <view class="menu-item" @click="goToHistory">
        <fui-icon name="clock" color="#5856d6" size="24" />
        <text class="menu-text">最近播放</text>
        <text class="menu-count">{{ historyCount }}</text>
        <fui-icon name="arrow-right" color="#8d96a0" size="16" />
      </view>
      
      <view class="menu-item" @click="goToDownloads">
        <fui-icon name="download" color="#4cd964" size="24" />
        <text class="menu-text">下载的音乐</text>
        <text class="menu-count">{{ downloadCount }}</text>
        <fui-icon name="arrow-right" color="#8d96a0" size="16" />
      </view>
    </view>

    <!-- 我的播放列表 -->
    <ContentSection title="我的播放列表" :show-more="true">
      <view class="playlist-list">
        <view 
          v-for="playlist in myPlaylists"
          :key="playlist.id"
          class="playlist-item"
          @click="goToPlaylist(playlist.id)"
        >
          <image :src="playlist.cover_url" class="playlist-cover" />
          <view class="playlist-info">
            <text class="playlist-name">{{ playlist.name }}</text>
            <text class="playlist-count">{{ playlist.track_count }} 首歌</text>
          </view>
        </view>
      </view>
    </ContentSection>
  </view>
</template>
```

### 6. 个人中心页面 (profile/profile.vue)

用户账户管理和应用设置。

#### 页面结构
```vue
<template>
  <view class="profile-page">
    <!-- 用户头部 -->
    <view class="profile-header">
      <image :src="userInfo?.avatar_url" class="profile-avatar" />
      <text class="profile-name">{{ userInfo?.nickname }}</text>
      <text class="profile-email">{{ userInfo?.email }}</text>
      <fui-button type="primary" size="small" @click="editProfile">
        编辑资料
      </fui-button>
    </view>

    <!-- 统计信息 -->
    <view class="stats-section">
      <view class="stat-item">
        <text class="stat-number">{{ userStats.total_plays }}</text>
        <text class="stat-label">播放次数</text>
      </view>
      <view class="stat-item">
        <text class="stat-number">{{ userStats.favorite_count }}</text>
        <text class="stat-label">收藏歌曲</text>
      </view>
      <view class="stat-item">
        <text class="stat-number">{{ userStats.playlist_count }}</text>
        <text class="stat-label">创建歌单</text>
      </view>
    </view>

    <!-- 功能列表 -->
    <view class="menu-list">
      <view class="menu-group">
        <text class="group-title">音乐设置</text>
        <view class="menu-item" @click="goToSettings">
          <fui-icon name="settings" color="#8d96a0" size="20" />
          <text class="menu-text">播放设置</text>
          <fui-icon name="arrow-right" color="#8d96a0" size="16" />
        </view>
        <view class="menu-item" @click="goToDownloadSettings">
          <fui-icon name="download" color="#8d96a0" size="20" />
          <text class="menu-text">下载设置</text>
          <fui-icon name="arrow-right" color="#8d96a0" size="16" />
        </view>
      </view>

      <view class="menu-group">
        <text class="group-title">账户</text>
        <view class="menu-item" @click="goToSecurity">
          <fui-icon name="shield" color="#8d96a0" size="20" />
          <text class="menu-text">账户与安全</text>
          <fui-icon name="arrow-right" color="#8d96a0" size="16" />
        </view>
        <view class="menu-item" @click="goToPrivacy">
          <fui-icon name="lock" color="#8d96a0" size="20" />
          <text class="menu-text">隐私设置</text>
          <fui-icon name="arrow-right" color="#8d96a0" size="16" />
        </view>
      </view>

      <view class="menu-group">
        <text class="group-title">其他</text>
        <view class="menu-item" @click="goToHelp">
          <fui-icon name="help" color="#8d96a0" size="20" />
          <text class="menu-text">帮助与反馈</text>
          <fui-icon name="arrow-right" color="#8d96a0" size="16" />
        </view>
        <view class="menu-item" @click="goToAbout">
          <fui-icon name="info" color="#8d96a0" size="20" />
          <text class="menu-text">关于羊咩快报</text>
          <fui-icon name="arrow-right" color="#8d96a0" size="16" />
        </view>
      </view>
    </view>

    <!-- 退出登录 -->
    <view class="logout-section">
      <fui-button type="danger" @click="logout">退出登录</fui-button>
    </view>
  </view>
</template>
```

---

## 核心组件设计

### 1. 迷你播放器 (MiniPlayer.vue)

底部固定的迷你播放器，在所有页面显示。

```vue
<template>
  <view class="mini-player" v-if="currentTrack" @click="goToPlayer">
    <view class="track-info">
      <image :src="currentTrack.cover_url" class="track-cover" />
      <view class="track-details">
        <text class="track-title">{{ currentTrack.title }}</text>
        <text class="track-artist">{{ currentTrack.artist?.name }}</text>
      </view>
    </view>

    <view class="player-controls">
      <fui-icon 
        :name="isPlaying ? 'pause' : 'play'" 
        color="#4CD964" 
        size="24"
        @click.stop="togglePlay"
      />
      <fui-icon 
        name="skip-next" 
        color="#8d96a0" 
        size="20"
        @click.stop="playNext"
      />
    </view>

    <!-- 进度条 -->
    <view class="progress-bar">
      <view 
        class="progress-filled" 
        :style="{ width: progressPercent + '%' }"
      ></view>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from '@/store'

const store = useStore()

const currentTrack = computed(() => store.player.currentTrack)
const isPlaying = computed(() => store.player.isPlaying)
const progressPercent = computed(() => store.player.progressPercent)

const togglePlay = () => {
  store.player.togglePlay()
}

const playNext = () => {
  store.player.playNext()
}

const goToPlayer = () => {
  uni.navigateTo({ url: '/pages/player/player' })
}
</script>

<style lang="scss" scoped>
.mini-player {
  position: fixed;
  bottom: 100rpx; // 底部导航栏高度
  left: 0;
  right: 0;
  height: 120rpx;
  background-color: #fff;
  border-top: 1px solid #eaedf0;
  display: flex;
  align-items: center;
  padding: 0 32rpx;
  z-index: 1000;
}

.track-info {
  flex: 1;
  display: flex;
  align-items: center;
  min-width: 0;
}

.track-cover {
  width: 80rpx;
  height: 80rpx;
  border-radius: 8rpx;
  margin-right: 24rpx;
}

.track-details {
  flex: 1;
  min-width: 0;
}

.track-title {
  display: block;
  font-size: 28rpx;
  font-weight: 500;
  color: #2c3038;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-artist {
  display: block;
  font-size: 24rpx;
  color: #8d96a0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.player-controls {
  display: flex;
  align-items: center;
  gap: 32rpx;
}

.progress-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4rpx;
  background-color: #eaedf0;
}

.progress-filled {
  height: 100%;
  background-color: #4CD964;
  transition: width 0.3s ease;
}
</style>
```

### 2. 内容卡片 (ContentCard.vue)

通用的内容展示卡片组件。

```vue
<template>
  <view 
    class="content-card" 
    :class="[`card-${cardType}`, { 'is-playing': isCurrentTrack }]"
    @click="handleClick"
  >
    <view class="card-cover-container">
      <image 
        :src="content.cover_url" 
        class="card-cover"
        mode="aspectFill"
      />
      
      <!-- 播放指示器 -->
      <view class="play-indicator" v-if="isCurrentTrack && isPlaying">
        <view class="wave-icon">
          <view class="wave-bar" v-for="i in 3" :key="i"></view>
        </view>
      </view>
      
      <!-- 播放按钮 -->
      <view class="play-overlay" v-else>
        <fui-icon name="play" color="#fff" size="20" />
      </view>
      
      <!-- 时长标签 -->
      <text class="duration-label">{{ formatDuration(content.duration) }}</text>
    </view>

    <view class="card-info">
      <text class="card-title">{{ content.title }}</text>
      <text class="card-artist">{{ content.artist?.name }}</text>
      
      <!-- 额外信息 -->
      <view class="card-meta" v-if="cardType === 'list'">
        <text class="play-count">{{ formatPlayCount(content.play_count) }} 次播放</text>
        <fui-icon 
          :name="content.is_liked ? 'heart-fill' : 'heart'" 
          :color="content.is_liked ? '#ff3b30' : '#8d96a0'" 
          size="16"
          @click.stop="toggleLike"
        />
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from '@/store'

const props = defineProps({
  content: {
    type: Object,
    required: true
  },
  cardType: {
    type: String,
    default: 'small', // small | medium | large | list
    validator: (value) => ['small', 'medium', 'large', 'list'].includes(value)
  }
})

const emit = defineEmits(['click', 'like'])

const store = useStore()

const isCurrentTrack = computed(() => 
  store.player.currentTrack?.id === props.content.id
)

const isPlaying = computed(() => store.player.isPlaying)

const handleClick = () => {
  emit('click', props.content)
}

const toggleLike = () => {
  emit('like', props.content)
}

const formatDuration = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const formatPlayCount = (count) => {
  if (count >= 1000000) {
    return `${(count / 1000000).toFixed(1)}M`
  }
  if (count >= 1000) {
    return `${(count / 1000).toFixed(1)}K`
  }
  return count.toString()
}
</script>

<style lang="scss" scoped>
.content-card {
  background-color: #fff;
  border-radius: 12rpx;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
  
  &:active {
    transform: scale(0.98);
  }
  
  &.is-playing {
    .card-cover-container {
      border: 2px solid #4CD964;
    }
  }
}

// 小尺寸卡片 (横向滚动列表)
.card-small {
  width: 280rpx;
  
  .card-cover-container {
    width: 280rpx;
    height: 280rpx;
  }
  
  .card-info {
    padding: 16rpx;
  }
  
  .card-title {
    font-size: 28rpx;
  }
  
  .card-artist {
    font-size: 24rpx;
  }
}

// 列表样式卡片
.card-list {
  display: flex;
  align-items: center;
  padding: 24rpx;
  margin-bottom: 16rpx;
  
  .card-cover-container {
    width: 100rpx;
    height: 100rpx;
    margin-right: 24rpx;
    border-radius: 8rpx;
  }
  
  .card-info {
    flex: 1;
    min-width: 0;
  }
  
  .card-title {
    font-size: 32rpx;
    font-weight: 500;
    margin-bottom: 8rpx;
  }
  
  .card-artist {
    font-size: 26rpx;
    color: #8d96a0;
    margin-bottom: 8rpx;
  }
  
  .card-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .play-count {
    font-size: 22rpx;
    color: #8d96a0;
  }
}

.card-cover-container {
  position: relative;
  border-radius: 12rpx;
  overflow: hidden;
}

.card-cover {
  width: 100%;
  height: 100%;
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60rpx;
  height: 60rpx;
  border-radius: 30rpx;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.content-card:hover .play-overlay {
  opacity: 1;
}

.play-indicator {
  position: absolute;
  bottom: 16rpx;
  left: 16rpx;
  
  .wave-icon {
    display: flex;
    align-items: flex-end;
    gap: 4rpx;
  }
  
  .wave-bar {
    width: 6rpx;
    background-color: #4CD964;
    border-radius: 3rpx;
    animation: wave 1s infinite ease-in-out;
    
    &:nth-child(1) { height: 12rpx; animation-delay: 0s; }
    &:nth-child(2) { height: 20rpx; animation-delay: 0.1s; }
    &:nth-child(3) { height: 16rpx; animation-delay: 0.2s; }
  }
}

.duration-label {
  position: absolute;
  bottom: 16rpx;
  right: 16rpx;
  font-size: 20rpx;
  color: #fff;
  background-color: rgba(0, 0, 0, 0.6);
  padding: 4rpx 8rpx;
  border-radius: 4rpx;
}

.card-title {
  display: block;
  color: #2c3038;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 8rpx;
}

.card-artist {
  display: block;
  color: #8d96a0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@keyframes wave {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}
</style>
```

---

## 状态管理 (Pinia Store)

### 播放器状态管理 (store/modules/player.js)

```javascript
import { defineStore } from 'pinia'

export const usePlayerStore = defineStore('player', {
  state: () => ({
    currentTrack: null,
    currentPlaylist: null,
    isPlaying: false,
    currentTime: 0,
    duration: 0,
    volume: 1,
    shuffleMode: false,
    repeatMode: 'none', // none | one | all
    audioContext: null,
    playlist: [],
    currentIndex: 0
  }),

  getters: {
    progressPercent: (state) => {
      if (state.duration === 0) return 0
      return (state.currentTime / state.duration) * 100
    },

    canPlayPrevious: (state) => {
      return state.currentIndex > 0 || state.repeatMode === 'all'
    },

    canPlayNext: (state) => {
      return state.currentIndex < state.playlist.length - 1 || state.repeatMode === 'all'
    }
  },

  actions: {
    async playTrack(track, playlist = null) {
      this.currentTrack = track
      
      if (playlist) {
        this.currentPlaylist = playlist
        this.playlist = playlist.tracks
        this.currentIndex = playlist.tracks.findIndex(t => t.id === track.id)
      }

      try {
        await this.setupAudio(track.audio_url)
        this.isPlaying = true
        
        // 记录播放历史
        this.recordPlayHistory(track)
      } catch (error) {
        console.error('播放失败:', error)
        uni.showToast({
          title: '播放失败',
          icon: 'error'
        })
      }
    },

    async setupAudio(audioUrl) {
      return new Promise((resolve, reject) => {
        this.audioContext = uni.createInnerAudioContext()
        
        this.audioContext.src = audioUrl
        this.audioContext.volume = this.volume
        
        this.audioContext.onPlay(() => {
          this.isPlaying = true
          resolve()
        })
        
        this.audioContext.onPause(() => {
          this.isPlaying = false
        })
        
        this.audioContext.onEnded(() => {
          this.handleTrackEnded()
        })
        
        this.audioContext.onError((error) => {
          reject(error)
        })
        
        this.audioContext.onTimeUpdate(() => {
          this.currentTime = this.audioContext.currentTime
          this.duration = this.audioContext.duration
        })
        
        this.audioContext.play()
      })
    },

    togglePlay() {
      if (this.audioContext) {
        if (this.isPlaying) {
          this.audioContext.pause()
        } else {
          this.audioContext.play()
        }
      }
    },

    playNext() {
      if (this.shuffleMode) {
        this.playRandomTrack()
      } else {
        const nextIndex = this.getNextIndex()
        if (nextIndex !== -1) {
          this.playTrackAtIndex(nextIndex)
        }
      }
    },

    playPrevious() {
      const prevIndex = this.getPreviousIndex()
      if (prevIndex !== -1) {
        this.playTrackAtIndex(prevIndex)
      }
    },

    seek(time) {
      if (this.audioContext) {
        this.audioContext.seek(time)
        this.currentTime = time
      }
    },

    setVolume(volume) {
      this.volume = volume
      if (this.audioContext) {
        this.audioContext.volume = volume
      }
    },

    toggleShuffle() {
      this.shuffleMode = !this.shuffleMode
    },

    toggleRepeat() {
      const modes = ['none', 'one', 'all']
      const currentIndex = modes.indexOf(this.repeatMode)
      this.repeatMode = modes[(currentIndex + 1) % modes.length]
    },

    handleTrackEnded() {
      if (this.repeatMode === 'one') {
        this.seek(0)
        this.togglePlay()
      } else {
        this.playNext()
      }
    },

    getNextIndex() {
      if (this.currentIndex < this.playlist.length - 1) {
        return this.currentIndex + 1
      } else if (this.repeatMode === 'all') {
        return 0
      }
      return -1
    },

    getPreviousIndex() {
      if (this.currentIndex > 0) {
        return this.currentIndex - 1
      } else if (this.repeatMode === 'all') {
        return this.playlist.length - 1
      }
      return -1
    },

    playTrackAtIndex(index) {
      if (index >= 0 && index < this.playlist.length) {
        this.currentIndex = index
        this.playTrack(this.playlist[index])
      }
    },

    playRandomTrack() {
      const randomIndex = Math.floor(Math.random() * this.playlist.length)
      this.playTrackAtIndex(randomIndex)
    },

    getCurrentTime() {
      return this.audioContext ? this.audioContext.currentTime : 0
    },

    async recordPlayHistory(track) {
      // 调用API记录播放历史
      try {
        await api.player.recordPlay({
          content_id: track.id,
          device_type: 'mobile'
        })
      } catch (error) {
        console.error('记录播放历史失败:', error)
      }
    },

    destroy() {
      if (this.audioContext) {
        this.audioContext.destroy()
        this.audioContext = null
      }
      this.currentTrack = null
      this.isPlaying = false
      this.currentTime = 0
      this.duration = 0
    }
  }
})
```

---

## 工具函数

### API请求封装 (utils/request.js)

```javascript
import { useUserStore } from '@/store/modules/user'

const BASE_URL = 'https://api.yangmie.com/v1'

// 请求拦截器
const requestInterceptor = (config) => {
  const userStore = useUserStore()
  
  // 添加认证token
  if (userStore.token) {
    config.header.Authorization = `Bearer ${userStore.token}`
  }
  
  // 添加通用header
  config.header['Content-Type'] = 'application/json'
  config.header['Accept'] = 'application/json'
  
  return config
}

// 响应拦截器
const responseInterceptor = (response) => {
  const { statusCode, data } = response
  
  if (statusCode >= 200 && statusCode < 300) {
    return data
  }
  
  // 处理特定错误
  if (statusCode === 401) {
    const userStore = useUserStore()
    userStore.logout()
    uni.reLaunch({
      url: '/pages/auth/login'
    })
    return Promise.reject(new Error('登录已过期'))
  }
  
  if (statusCode === 429) {
    uni.showToast({
      title: '请求过于频繁',
      icon: 'error'
    })
    return Promise.reject(new Error('请求限流'))
  }
  
  return Promise.reject(new Error(data.message || '请求失败'))
}

// 基础请求方法
const request = (options) => {
  return new Promise((resolve, reject) => {
    const config = {
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data,
      header: {},
      timeout: options.timeout || 10000,
      ...options
    }
    
    // 应用请求拦截器
    const interceptedConfig = requestInterceptor(config)
    
    uni.request({
      ...interceptedConfig,
      success: (response) => {
        try {
          const result = responseInterceptor(response)
          resolve(result)
        } catch (error) {
          reject(error)
        }
      },
      fail: (error) => {
        uni.showToast({
          title: '网络错误',
          icon: 'error'
        })
        reject(error)
      }
    })
  })
}

// HTTP方法封装
export const http = {
  get: (url, params) => request({
    url,
    method: 'GET',
    data: params
  }),
  
  post: (url, data) => request({
    url,
    method: 'POST',
    data
  }),
  
  put: (url, data) => request({
    url,
    method: 'PUT',
    data
  }),
  
  delete: (url, params) => request({
    url,
    method: 'DELETE',
    data: params
  }),
  
  upload: (url, filePath, formData = {}) => {
    const userStore = useUserStore()
    
    return new Promise((resolve, reject) => {
      uni.uploadFile({
        url: BASE_URL + url,
        filePath,
        name: 'file',
        formData,
        header: {
          Authorization: userStore.token ? `Bearer ${userStore.token}` : ''
        },
        success: (response) => {
          try {
            const data = JSON.parse(response.data)
            resolve(data)
          } catch (error) {
            reject(error)
          }
        },
        fail: reject
      })
    })
  }
}

export default http
```

---

## 性能优化策略

### 1. 图片懒加载
- 使用`uni-lazyload`组件
- 实现渐进式图片加载
- 缓存用户头像和封面图

### 2. 音频预加载
- 智能预加载下一首歌曲
- 根据网络状况调整加载策略
- 实现断点续传功能

### 3. 数据缓存
- 用户偏好设置本地缓存
- 热门内容离线缓存
- 播放历史本地存储

### 4. 代码分包
- 按功能模块进行分包
- 首页优先加载
- 播放器核心功能独立包

---

*此文档随开发进展持续更新*