<template>
  <view class="content-section">
    <!-- 内容区块 -->
    <slot />
  </view>
</template>

<script>
export default {
  name: 'ContentSection',
  props: {
    title: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.content-section {
  padding: 16rpx;
  background: #fff;
  border-radius: 12rpx;
  margin-bottom: 24rpx;
}
</style> 