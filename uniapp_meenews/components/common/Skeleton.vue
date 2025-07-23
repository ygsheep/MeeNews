<template>
  <view class="skeleton">
    <view v-for="n in rows" :key="n" class="skeleton-row" :style="{ borderRadius: radius + 'rpx' }"></view>
  </view>
</template>

<script>
export default {
  name: 'Skeleton',
  props: {
    rows: { type: Number, default: 3 },
    radius: { type: Number, default: 8 }
  }
}
</script>

<style scoped>
.skeleton {
  padding: 16rpx 0;
}
.skeleton-row {
  height: 32rpx;
  background: linear-gradient(90deg, #f1f4fa 25%, #e6eaf2 50%, #f1f4fa 75%);
  margin-bottom: 16rpx;
  animation: skeleton-loading 1.2s infinite linear;
}
@keyframes skeleton-loading {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
</style> 