<template>
  <view class="ai-tts-player">
    <fui-icon :name="isPlaying ? 'pause' : 'play'" color="#4CD964" size="36" @click="togglePlay" />
    <text class="audio-label">AI解说</text>
  </view>
</template>

<script>
export default {
  name: 'AiTTSPlayer',
  props: {
    audioUrl: { type: String, default: '' }
  },
  data() {
    return { isPlaying: false, audio: null }
  },
  methods: {
    togglePlay() {
      if (!this.audio) {
        this.audio = uni.createInnerAudioContext()
        this.audio.src = this.audioUrl
        this.audio.onEnded(() => { this.isPlaying = false })
      }
      if (this.isPlaying) {
        this.audio.pause()
        this.isPlaying = false
      } else {
        this.audio.play()
        this.isPlaying = true
      }
    }
  },
  beforeUnmount() {
    if (this.audio) this.audio.destroy()
  }
}
</script>

<style scoped>
.ai-tts-player {
  display: flex;
  align-items: center;
  background: #f1f4fa;
  border-radius: 12rpx;
  padding: 16rpx 24rpx;
  margin: 16rpx 0;
}
.audio-label {
  font-size: 28rpx;
  color: #2c3038;
  margin-left: 16rpx;
}
</style> 