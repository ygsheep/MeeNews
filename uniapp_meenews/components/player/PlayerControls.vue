<template>
  <view class="player-controls">
    <fui-icon name="skip-previous" color="#8d96a0" size="36" @click="$emit('playPrevious')" />
    <view class="play-btn" @click="$emit('togglePlay')">
      <fui-icon :name="isPlaying ? 'pause' : 'play'" color="#fff" size="40" />
    </view>
    <fui-icon name="skip-next" color="#8d96a0" size="36" @click="$emit('playNext')" />
    <fui-icon :name="repeatModeIcon" color="#4CD964" size="28" @click="$emit('toggleRepeat')" />
    <fui-icon :name="shuffleMode ? 'shuffle' : 'shuffle-outline'" color="#4CD964" size="28" @click="$emit('toggleShuffle')" />
  </view>
</template>

<script>
export default {
  name: 'PlayerControls',
  props: {
    isPlaying: { type: Boolean, default: false },
    repeatMode: { type: String, default: 'none' }, // none | one | all
    shuffleMode: { type: Boolean, default: false }
  },
  computed: {
    repeatModeIcon() {
      if (this.repeatMode === 'one') return 'repeat-one'
      if (this.repeatMode === 'all') return 'repeat'
      return 'repeat-outline'
    }
  }
}
</script>

<style scoped>
.player-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 48rpx;
  margin: 32rpx 0;
}
.play-btn {
  width: 100rpx; height: 100rpx;
  border-radius: 50rpx;
  background: #4CD964;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 8rpx 24rpx rgba(76,217,100,0.2);
}
</style> 