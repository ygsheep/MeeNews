<template>
  <view class="ai-summary">
    <fui-icon name="bulb" color="#4CD964" size="24" />
    <text class="summary-text">{{ summary }}</text>
  </view>
</template>

<script>
export default {
  name: 'AiSummary',
  props: {
    summary: { type: String, default: '' }
  }
}
</script>

<style scoped>
.ai-summary {
  display: flex;
  align-items: flex-start;
  background: #f1f4fa;
  border-radius: 12rpx;
  padding: 24rpx;
  margin: 24rpx 0;
}
.summary-text {
  font-size: 28rpx;
  color: #2c3038;
  margin-left: 16rpx;
}
</style> 