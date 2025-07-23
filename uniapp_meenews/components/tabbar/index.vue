<template>
  <view class="custom-tabbar">
    <!-- 左侧Tab -->
    <view class="tab-item" :class="{active: selected === 0}" @click="switchTab(0)">
      <image :src="selected === 0 ? tabList[0].selectedIconPath : tabList[0].iconPath" class="tab-icon" mode="aspectFit" />
      <text class="tab-text">{{ tabList[0].text }}</text>
    </view>
    <!-- 发现Tab -->
    <view class="tab-item" :class="{active: selected === 1}" @click="switchTab(1)">
      <image :src="selected === 1 ? tabList[1].selectedIconPath : tabList[1].iconPath" class="tab-icon" mode="aspectFit" />
      <text class="tab-text">{{ tabList[1].text }}</text>
    </view>
    <!-- 中间悬浮播放按钮 -->
    <view class="play-btn-wrapper" @click="goToPlayer">
      <view class="play-btn">
        <image v-if="currentContent && currentContent.isPlaying" src="/static/icons/player-pause-circle.svg" class="play-icon" mode="aspectFit" />
        <image v-else src="/static/icons/player-play-circle.svg" class="play-icon" mode="aspectFit" />
      </view>
    </view>
    <!-- 音乐库Tab -->
    <view class="tab-item" :class="{active: selected === 2}" @click="switchTab(2)">
      <image :src="selected === 2 ? tabList[2].selectedIconPath : tabList[2].iconPath" class="tab-icon" mode="aspectFit" />
      <text class="tab-text">{{ tabList[2].text }}</text>
    </view>
    <!-- 我的Tab -->
    <view class="tab-item" :class="{active: selected === 3}" @click="switchTab(3)">
      <image :src="selected === 3 ? tabList[3].selectedIconPath : tabList[3].iconPath" class="tab-icon" mode="aspectFit" />
      <text class="tab-text">{{ tabList[3].text }}</text>
    </view>
  </view>
</template>

<script>
import { computed } from 'vue'
import { usePlayerStore } from '@/store/player'

export default {
  name: 'CustomTabBar',
  setup() {
    // Tab配置，全部使用svg后缀
    const tabList = [
      {
        pagePath: '/pages/index/index',
        iconPath: '/static/icons/home-default.svg',
        selectedIconPath: '/static/icons/home-selected.svg',
        text: '首页'
      },
      {
        pagePath: '/pages/discover/discover',
        iconPath: '/static/icons/discover-default.svg',
        selectedIconPath: '/static/icons/discover-selected.svg',
        text: '发现'
      },
      {
        pagePath: '/pages/library/library',
        iconPath: '/static/icons/library-default.svg',
        selectedIconPath: '/static/icons/library-selected.svg',
        text: '音乐库'
      },
      {
        pagePath: '/pages/profile/profile',
        iconPath: '/static/icons/profile-default.svg',
        selectedIconPath: '/static/icons/profile-selected.svg',
        text: '我的'
      }
    ]
    // 当前选中Tab
    const selected = uni.getStorageSync('tabbar_selected') || 0
    // 全局播放器store
    const playerStore = usePlayerStore()
    const currentContent = computed(() => {
      // 需保证currentContent有isPlaying字段，true为正在播放，false为暂停/无内容
      return playerStore.currentContent || { isPlaying: false }
    })

    // 切换Tab
    const switchTab = (idx) => {
      if (selected === idx) return
      uni.setStorageSync('tabbar_selected', idx)
      uni.switchTab({ url: tabList[idx].pagePath })
    }
    // 跳转到多媒体播放页
    const goToPlayer = () => {
      if (playerStore.currentContent) {
        uni.navigateTo({ url: '/pages/player/mediaPlayer' })
      } else {
        uni.showToast({ title: '暂无播放内容', icon: 'none' })
      }
    }
    return {
      tabList,
      selected,
      currentContent,
      switchTab,
      goToPlayer
    }
  }
}
</script>

<style scoped>
.custom-tabbar {
  position: fixed;
  left: 0; right: 0; bottom: 0;
  height: 120rpx;
  background: #fff;
  border-top: 1px solid #eaedf0;
  display: flex;
  align-items: center;
  justify-content: space-around;
  z-index: 1000;
}
.tab-item {
  flex: 1;
  text-align: center;
  color: #8d96a0;
  font-size: 24rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}
.tab-item.active .tab-text {
  color: #4CD964;
}
.tab-icon {
  width: 48rpx;
  height: 48rpx;
  margin-bottom: 4rpx;
}
.play-btn-wrapper {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 48rpx; /* 上移按钮，原为24rpx */
  z-index: 1100;
}
.play-btn {
  width: 96rpx;
  height: 96rpx;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 4rpx 24rpx rgba(76,217,100,0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4rpx solid #4CD964;
  overflow: hidden;
}
.play-icon {
  width: 64rpx;
  height: 64rpx;
}
</style> 