<template>
  <view class="artist-card" @click="$emit('click', artist)">
    <BaseImage :src="artist.avatarUrl" class="avatar" />
    <view class="info">
      <text class="name">{{ artist.name }}</text>
      <text class="desc">{{ artist.desc }}</text>
    </view>
  </view>
</template>

<script>
import BaseImage from '@/components/common/BaseImage.vue'
export default {
  name: 'ArtistCard',
  components: { BaseImage },
  props: {
    artist: { type: Object, required: true }
  },
  emits: ['click']
}
</script>

<style scoped>
.artist-card {
  width: 180rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
  padding: 24rpx 0;
  cursor: pointer;
  transition: transform 0.2s;
}
.avatar {
  width: 96rpx; height: 96rpx; border-radius: 50%; margin-bottom: 16rpx;
}
.name {
  font-size: 28rpx; font-weight: 500; color: #2c3038; margin-bottom: 8rpx;
}
.desc {
  font-size: 22rpx; color: #8d96a0; text-align: center;
}
</style> 