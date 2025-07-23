<template>
  <view class="album-card" @click="$emit('click', album)">
    <BaseImage :src="album.coverUrl" class="cover" />
    <view class="info">
      <text class="name">{{ album.name }}</text>
      <text class="artist">{{ album.artist }}</text>
      <text class="track-count">{{ album.trackCount }} 首曲目</text>
    </view>
  </view>
</template>

<script>
import BaseImage from '@/components/common/BaseImage.vue'
export default {
  name: 'AlbumCard',
  components: { BaseImage },
  props: {
    album: { type: Object, required: true }
  },
  emits: ['click']
}
</script>

<style scoped>
.album-card {
  width: 220rpx;
  background: #fff;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}
.cover {
  width: 100%; height: 160rpx; object-fit: cover;
}
.info {
  padding: 16rpx;
}
.name {
  font-size: 26rpx; font-weight: 500; color: #2c3038; margin-bottom: 8rpx;
}
.artist {
  font-size: 22rpx; color: #8d96a0; margin-bottom: 4rpx;
}
.track-count {
  font-size: 20rpx; color: #b0b0b0;
}
</style> 