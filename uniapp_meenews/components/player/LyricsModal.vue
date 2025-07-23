<template>
  <view class="lyrics-modal" v-if="show">
    <view class="modal-bg" @click="$emit('close')"></view>
    <view class="modal-content">
      <scroll-view scroll-y class="lyrics-scroll">
        <view v-for="(line, idx) in lyrics" :key="idx" :class="['lyric-line', { active: idx === currentLine }]">
          {{ line.text }}
        </view>
      </scroll-view>
      <fui-icon name="close" color="#8d96a0" size="32" class="close-btn" @click="$emit('close')" />
    </view>
  </view>
</template>

<script>
export default {
  name: 'LyricsModal',
  props: {
    show: { type: Boolean, default: false },
    lyrics: { type: Array, default: () => [] },
    currentLine: { type: Number, default: 0 }
  },
  emits: ['close']
}
</script>

<style scoped>
.lyrics-modal {
  position: fixed;
  left: 0; right: 0; top: 0; bottom: 0;
  z-index: 2000;
}
.modal-bg {
  position: absolute;
  left: 0; right: 0; top: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
}
.modal-content {
  position: absolute;
  left: 0; right: 0; bottom: 0;
  background: #fff;
  border-top-left-radius: 32rpx;
  border-top-right-radius: 32rpx;
  padding: 48rpx 32rpx 32rpx 32rpx;
  min-height: 60vh;
  max-height: 80vh;
  box-shadow: 0 -8rpx 32rpx rgba(0,0,0,0.08);
}
.lyrics-scroll {
  max-height: 60vh;
  overflow-y: auto;
}
.lyric-line {
  font-size: 32rpx;
  color: #8d96a0;
  text-align: center;
  margin: 16rpx 0;
  transition: color 0.2s;
}
.lyric-line.active {
  color: #4CD964;
  font-weight: bold;
  font-size: 36rpx;
}
.close-btn {
  position: absolute;
  top: 24rpx;
  right: 24rpx;
}
</style> 