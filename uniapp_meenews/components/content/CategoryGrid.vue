<template>
  <view class="category-grid">
    <view v-for="item in categories" :key="item.id" class="category-item" @click="$emit('click', item)">
      <BaseImage :src="item.iconUrl" class="icon" />
      <text class="name">{{ item.name }}</text>
    </view>
  </view>
</template>

<script>
import BaseImage from '@/components/common/BaseImage.vue'
export default {
  name: 'CategoryGrid',
  components: { BaseImage },
  props: {
    categories: { type: Array, default: () => [] }
  },
  emits: ['click']
}
</script>

<style scoped>
.category-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 32rpx;
  padding: 16rpx 0;
}
.category-item {
  width: 120rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.34);
  padding: 24rpx 0;
  cursor: pointer;
  transition: transform 0.2s;
}
.icon {
  width: 56rpx; height: 56rpx; margin-bottom: 12rpx;
}
.name {
  font-size: 24rpx; color: #2c3038; text-align: center;
}
</style> 