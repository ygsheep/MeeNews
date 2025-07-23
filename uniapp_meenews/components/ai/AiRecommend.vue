<template>
  <view class="ai-recommend">
    <view v-for="item in recommendList" :key="item.id" class="recommend-item">
      <fui-icon name="star" color="#FFD700" size="20" />
      <text class="recommend-text">{{ item.text }}</text>
    </view>
  </view>
</template>

<script>
export default {
  name: 'AiRecommend',
  props: {
    recommendList: { type: Array, default: () => [] }
  }
}
</script>

<style scoped>
.ai-recommend {
  background: #f1f4fa;
  border-radius: 12rpx;
  padding: 24rpx;
  margin: 24rpx 0;
}
.recommend-item {
  display: flex;
  align-items: center;
  margin-bottom: 12rpx;
}
.recommend-text {
  font-size: 28rpx;
  color: #2c3038;
  margin-left: 12rpx;
}
</style> 