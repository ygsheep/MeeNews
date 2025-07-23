<template>
  <view class="error-tip">
    <fui-icon name="info" color="#ff3b30" size="28" />
    <text class="error-text">{{ message }}</text>
  </view>
</template>

<script>
export default {
  name: 'ErrorTip',
  props: {
    message: { type: String, default: '出错了，请稍后重试' }
  }
}
</script>

<style scoped>
.error-tip {
  display: flex;
  align-items: center;
  background: #fff0f0;
  border-radius: 12rpx;
  padding: 24rpx;
  margin: 24rpx 0;
}
.error-text {
  font-size: 28rpx;
  color: #ff3b30;
  margin-left: 16rpx;
}
</style> 