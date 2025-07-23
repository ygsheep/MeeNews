<template>
  <view class="ai-emotion">
    <fui-icon :name="iconName" :color="iconColor" size="24" />
    <text class="emotion-text">{{ emotionLabel }}（{{ score }}）</text>
  </view>
</template>

<script>
export default {
  name: 'AiEmotion',
  props: {
    emotion: { type: String, default: 'neutral' }, // positive | negative | neutral
    score: { type: Number, default: 0 }
  },
  computed: {
    iconName() {
      if (this.emotion === 'positive') return 'smile'
      if (this.emotion === 'negative') return 'frown'
      return 'meh'
    },
    iconColor() {
      if (this.emotion === 'positive') return '#4CD964'
      if (this.emotion === 'negative') return '#ff3b30'
      return '#8d96a0'
    },
    emotionLabel() {
      if (this.emotion === 'positive') return '积极'
      if (this.emotion === 'negative') return '消极'
      return '中性'
    }
  }
}
</script>

<style scoped>
.ai-emotion {
  display: flex;
  align-items: center;
  background: #f1f4fa;
  border-radius: 12rpx;
  padding: 16rpx 24rpx;
  margin: 16rpx 0;
}
.emotion-text {
  font-size: 28rpx;
  color: #2c3038;
  margin-left: 16rpx;
}
</style> 