<template>
  <view class="library-page">
    <!-- 用户信息卡片 -->
    <view class="user-card" v-if="userInfo">
      <UserAvatar :src="userInfo.avatarUrl" :size="96" />
      <view class="user-info">
        <text class="user-name">{{ userInfo.nickname }}</text>
        <text class="user-stats">已听 {{ userStats.totalPlays }} 首歌</text>
      </view>
      <fui-icon name="edit" color="#8d96a0" size="20" @click="editProfile" />
    </view>

    <!-- 功能菜单 -->
    <view class="menu-section">
      <view class="menu-item" @click="goToFavorites">
        <fui-icon name="heart" color="#ff3b30" size="24" />
        <text class="menu-text">我喜欢的音乐</text>
        <text class="menu-count">{{ userStats.favoriteCount }}</text>
        <fui-icon name="arrow-right" color="#8d96a0" size="16" />
      </view>
      <view class="menu-item" @click="goToHistory">
        <fui-icon name="clock" color="#5856d6" size="24" />
        <text class="menu-text">最近播放</text>
        <text class="menu-count">{{ userStats.historyCount }}</text>
        <fui-icon name="arrow-right" color="#8d96a0" size="16" />
      </view>
      <view class="menu-item" @click="goToDownloads">
        <fui-icon name="download" color="#4cd964" size="24" />
        <text class="menu-text">下载的音乐</text>
        <text class="menu-count">{{ userStats.downloadCount }}</text>
        <fui-icon name="arrow-right" color="#8d96a0" size="16" />
      </view>
    </view>

    <!-- 我的播放列表 -->
    <ContentSection title="我的播放列表" :show-more="true">
      <view class="playlist-list">
        <view v-for="playlist in myPlaylists" :key="playlist.id" class="playlist-item" @click="goToPlaylist(playlist.id)">
          <BaseImage :src="playlist.coverUrl" class="playlist-cover" />
          <view class="playlist-info">
            <text class="playlist-name">{{ playlist.name }}</text>
            <text class="playlist-count">{{ playlist.trackCount }} 首歌</text>
          </view>
        </view>
      </view>
    </ContentSection>
  </view>
</template>

<script>
import { computed } from 'vue'
import { useUserStore } from '@/store/user'
import ContentSection from '@/components/content/ContentSection.vue'
import UserAvatar from '@/components/user/UserAvatar.vue'
import BaseImage from '@/components/common/BaseImage.vue'

const userStore = useUserStore()

export default {
  name: 'Library',
  components: { ContentSection, UserAvatar, BaseImage },
  setup() {
    // 用户信息
    const userInfo = computed(() => userStore.userInfo || { nickname: '未登录', avatarUrl: '/static/images/common/img_logo.png' })
    // 用户统计 mock
    const userStats = computed(() => ({
      totalPlays: 1234,
      favoriteCount: 56,
      historyCount: 78,
      downloadCount: 12
    }))
    // 我的播放列表 mock
    const myPlaylists = computed(() => ([
      { id: 1, name: 'AI推荐歌单', coverUrl: '/static/images/common/img_logo.png', trackCount: 20 },
      { id: 2, name: '流行精选', coverUrl: '/static/images/common/img_logo.png', trackCount: 15 }
    ]))

    // 跳转
    const editProfile = () => {
      uni.navigateTo({ url: '/pages/profile/edit-profile' })
    }
    const goToFavorites = () => {
      uni.navigateTo({ url: '/pages/library/favorites' })
    }
    const goToHistory = () => {
      uni.navigateTo({ url: '/pages/library/history' })
    }
    const goToDownloads = () => {
      uni.navigateTo({ url: '/pages/library/downloads' })
    }
    const goToPlaylist = (id) => {
      uni.navigateTo({ url: `/pages/library/playlist?id=${id}` })
    }

    return {
      userInfo,
      userStats,
      myPlaylists,
      editProfile,
      goToFavorites,
      goToHistory,
      goToDownloads,
      goToPlaylist
    }
  }
}
</script>

<style lang="scss" scoped>
.library-page {
  min-height: 100vh;
  background: #f8f9fa;
}
.user-card {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
  padding: 32rpx;
  margin: 32rpx;
}
.user-info {
  flex: 1;
  margin-left: 24rpx;
}
.user-name {
  font-size: 32rpx;
  font-weight: 500;
  color: #2c3038;
  margin-bottom: 8rpx;
}
.user-stats {
  font-size: 24rpx;
  color: #8d96a0;
}
.menu-section {
  margin: 32rpx;
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
}
.menu-item {
  display: flex;
  align-items: center;
  padding: 24rpx 32rpx;
  border-bottom: 1px solid #f1f4fa;
  font-size: 28rpx;
  color: #2c3038;
  cursor: pointer;
}
.menu-item:last-child {
  border-bottom: none;
}
.menu-text {
  flex: 1;
  margin-left: 24rpx;
}
.menu-count {
  color: #8d96a0;
  margin-right: 16rpx;
}
.playlist-list {
  display: flex;
  gap: 32rpx;
  padding: 32rpx;
}
.playlist-item {
  width: 180rpx;
  background: #fff;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}
.playlist-cover {
  width: 100%;
  height: 120rpx;
  object-fit: cover;
}
.playlist-info {
  padding: 16rpx;
}
.playlist-name {
  font-size: 26rpx;
  font-weight: 500;
  color: #2c3038;
  margin-bottom: 8rpx;
}
.playlist-count {
  font-size: 22rpx;
  color: #8d96a0;
}
</style> 