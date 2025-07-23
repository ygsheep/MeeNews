<template>
  <view class="user-stats">
    <view v-for="item in stats" :key="item.label" class="stat-item">
      <text class="stat-number">{{ item.value }}</text>
      <text class="stat-label">{{ item.label }}</text>
    </view>
  </view>
</template>

<script>
export default {
  name: 'UserStats',
  props: {
    stats: { type: Array, default: () => [] } // [{ label: '播放次数', value: 0 }, ...]
  }
}
</script>

<style scoped>
.user-stats {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 24rpx 0;
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
}
.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stat-number {
  font-size: 32rpx;
  color: #4CD964;
  font-weight: bold;
}
.stat-label {
  font-size: 22rpx;
  color: #8d96a0;
}
</style> 