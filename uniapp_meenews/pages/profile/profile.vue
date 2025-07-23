<template>
  <view class="profile-page">
    <!-- 用户头部 -->
    <view class="profile-header">
      <UserAvatar :src="userInfo.avatarUrl" :size="96" />
      <text class="profile-name">{{ userInfo.nickname }}</text>
      <text class="profile-email">{{ userInfo.email }}</text>
      <fui-button type="primary" size="small" @click="editProfile">编辑资料</fui-button>
    </view>

    <!-- 统计信息 -->
    <UserStats :stats="statsList" />

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

<script>
import { computed } from 'vue'
import { useUserStore } from '@/store/user'
import UserAvatar from '@/components/user/UserAvatar.vue'
import UserStats from '@/components/user/UserStats.vue'

const userStore = useUserStore()

export default {
  name: 'Profile',
  components: { UserAvatar, UserStats },
  setup() {
    // 用户信息
    const userInfo = computed(() => userStore.userInfo || { nickname: '未登录', email: '', avatarUrl: '/static/images/common/img_logo.png' })
    // 统计信息 mock
    const statsList = computed(() => ([
      { label: '播放次数', value: 1234 },
      { label: '收藏歌曲', value: 56 },
      { label: '创建歌单', value: 3 }
    ]))

    // 跳转
    const editProfile = () => {
      uni.navigateTo({ url: '/pages/profile/edit-profile' })
    }
    const goToSettings = () => {
      uni.navigateTo({ url: '/pages/profile/settings' })
    }
    const goToDownloadSettings = () => {
      uni.navigateTo({ url: '/pages/profile/download-settings' })
    }
    const goToSecurity = () => {
      uni.navigateTo({ url: '/pages/profile/security' })
    }
    const goToPrivacy = () => {
      uni.navigateTo({ url: '/pages/profile/privacy' })
    }
    const goToHelp = () => {
      uni.navigateTo({ url: '/pages/profile/help' })
    }
    const goToAbout = () => {
      uni.navigateTo({ url: '/pages/profile/about' })
    }
    const logout = () => {
      userStore.logout()
      uni.reLaunch({ url: '/pages/index/index' })
    }

    return {
      userInfo,
      statsList,
      editProfile,
      goToSettings,
      goToDownloadSettings,
      goToSecurity,
      goToPrivacy,
      goToHelp,
      goToAbout,
      logout
    }
  }
}
</script>

<style lang="scss" scoped>
.profile-page {
  min-height: 100vh;
  background: #f8f9fa;
}
.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
  padding: 32rpx;
  margin: 32rpx;
}
.profile-name {
  font-size: 32rpx;
  font-weight: 500;
  color: #2c3038;
  margin: 16rpx 0 8rpx 0;
}
.profile-email {
  font-size: 24rpx;
  color: #8d96a0;
  margin-bottom: 16rpx;
}
.menu-list {
  margin: 32rpx;
}
.menu-group {
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
  margin-bottom: 32rpx;
  padding-bottom: 8rpx;
}
.group-title {
  font-size: 24rpx;
  color: #8d96a0;
  padding: 24rpx 32rpx 0 32rpx;
  display: block;
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
.logout-section {
  margin: 32rpx;
  text-align: center;
}
</style> 