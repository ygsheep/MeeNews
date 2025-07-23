<template>
  <view class="progress-bar-container" @touchstart="onTouchStart" @touchmove="onTouchMove" @touchend="onTouchEnd">
    <!-- 进度条背景 -->
    <view class="progress-track" :style="trackStyle">
      <!-- 缓冲进度 -->
      <view 
        class="progress-buffered" 
        :style="{ width: `${bufferedPercent}%` }"
        v-if="showBuffered"
      ></view>
      
      <!-- 播放进度 -->
      <view 
        class="progress-played" 
        :style="[{ width: `${currentPercent}%` }, playedStyle]"
      ></view>
      
      <!-- 进度控制点 -->
      <view 
        class="progress-thumb"
        :class="{ dragging: isDragging, visible: showThumb }"
        :style="[{ left: `${currentPercent}%` }, thumbStyle]"
        v-if="interactive"
      >
        <view class="thumb-inner"></view>
      </view>
      
      <!-- 时间提示 -->
      <view 
        class="time-tooltip"
        :style="{ left: `${tooltipPercent}%` }"
        v-if="showTooltip && isDragging"
      >
        <text class="tooltip-text">{{ formatTooltipTime(tooltipTime) }}</text>
      </view>
    </view>
    
    <!-- 章节标记 -->
    <view class="chapter-markers" v-if="chapters && chapters.length">
      <view 
        v-for="chapter in chapters"
        :key="chapter.id"
        class="chapter-marker"
        :style="{ left: `${(chapter.time / total) * 100}%` }"
        @click="seekToChapter(chapter)"
      >
        <view class="marker-dot"></view>
        <view class="marker-tooltip">{{ chapter.title }}</view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  // 当前进度值
  current: {
    type: Number,
    default: 0
  },
  // 总长度
  total: {
    type: Number,
    default: 100
  },
  // 缓冲进度
  buffered: {
    type: Number,
    default: 0
  },
  // 是否可交互
  interactive: {
    type: Boolean,
    default: true
  },
  // 是否显示缓冲进度
  showBuffered: {
    type: Boolean,
    default: true
  },
  // 是否显示拖拽按钮
  showThumb: {
    type: Boolean,
    default: true
  },
  // 是否显示时间提示
  showTooltip: {
    type: Boolean,
    default: true
  },
  // 章节标记
  chapters: {
    type: Array,
    default: () => []
  },
  // 进度条高度
  height: {
    type: String,
    default: '6rpx'
  },
  // 主色调
  primaryColor: {
    type: String,
    default: '#4CD964'
  },
  // 背景色
  backgroundColor: {
    type: String,
    default: '#eaedf0'
  },
  // 缓冲色
  bufferedColor: {
    type: String,
    default: '#c7c7cc'
  },
  // 控制点大小
  thumbSize: {
    type: String,
    default: '28rpx'
  }
})

const emit = defineEmits(['seek', 'start-drag', 'end-drag', 'chapter-click'])

// 数据
const isDragging = ref(false)
const dragStartX = ref(0)
const dragStartPercent = ref(0)
const tooltipPercent = ref(0)
const tooltipTime = ref(0)

// 计算属性
const currentPercent = computed(() => {
  if (props.total === 0) return 0
  return Math.min(100, Math.max(0, (props.current / props.total) * 100))
})

const bufferedPercent = computed(() => {
  if (props.total === 0) return 0
  return Math.min(100, Math.max(0, (props.buffered / props.total) * 100))
})

const trackStyle = computed(() => ({
  height: props.height,
  backgroundColor: props.backgroundColor
}))

const playedStyle = computed(() => ({
  backgroundColor: props.primaryColor
}))

const thumbStyle = computed(() => ({
  width: props.thumbSize,
  height: props.thumbSize,
  backgroundColor: props.primaryColor
}))

// 方法
const onTouchStart = (e) => {
  if (!props.interactive) return
  
  const touch = e.touches[0]
  const rect = e.currentTarget.getBoundingClientRect()
  const percent = ((touch.clientX - rect.left) / rect.width) * 100
  
  isDragging.value = true
  dragStartX.value = touch.clientX
  dragStartPercent.value = percent
  tooltipPercent.value = percent
  tooltipTime.value = (percent / 100) * props.total
  
  emit('start-drag')
}

const onTouchMove = (e) => {
  if (!isDragging.value || !props.interactive) return
  
  e.preventDefault()
  
  const touch = e.touches[0]
  const rect = e.currentTarget.getBoundingClientRect()
  const percent = Math.min(100, Math.max(0, ((touch.clientX - rect.left) / rect.width) * 100))
  
  tooltipPercent.value = percent
  tooltipTime.value = (percent / 100) * props.total
}

const onTouchEnd = (e) => {
  if (!isDragging.value || !props.interactive) return
  
  const touch = e.changedTouches[0]
  const rect = e.currentTarget.getBoundingClientRect()
  const percent = Math.min(100, Math.max(0, ((touch.clientX - rect.left) / rect.width) * 100))
  const seekTime = (percent / 100) * props.total
  
  isDragging.value = false
  
  emit('seek', seekTime)
  emit('end-drag')
}

const seekToChapter = (chapter) => {
  emit('seek', chapter.time)
  emit('chapter-click', chapter)
}

const formatTooltipTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  
  if (hours > 0) {
    return `${hours}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 监听器
watch(() => props.current, (newCurrent) => {
  if (!isDragging.value) {
    // 非拖拽状态下自动更新
  }
})
</script>

<style lang="scss" scoped>
.progress-bar-container {
  position: relative;
  width: 100%;
  padding: 20rpx 0;
  cursor: pointer;
}

.progress-track {
  position: relative;
  width: 100%;
  border-radius: 50rpx;
  overflow: hidden;
  transition: height 0.2s ease;
  
  &:hover {
    height: 8rpx !important;
  }
}

.progress-buffered {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #c7c7cc;
  transition: width 0.3s ease;
}

.progress-played {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: linear-gradient(90deg, #4CD964 0%, #00d2ff 100%);
  transition: width 0.1s ease;
  border-radius: inherit;
}

.progress-thumb {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  box-shadow: 0 4rpx 12rpx rgba(76, 217, 100, 0.4);
  transition: all 0.2s ease;
  opacity: 0;
  z-index: 10;
  
  &.visible {
    opacity: 1;
  }
  
  &.dragging {
    transform: translate(-50%, -50%) scale(1.2);
    box-shadow: 0 6rpx 16rpx rgba(76, 217, 100, 0.6);
  }
  
  .progress-track:hover & {
    opacity: 1;
  }
}

.thumb-inner {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: inherit;
  border: 4rpx solid #ffffff;
  box-sizing: border-box;
}

.time-tooltip {
  position: absolute;
  bottom: 60rpx;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  padding: 8rpx 16rpx;
  border-radius: 8rpx;
  z-index: 20;
  pointer-events: none;
  
  &::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 8rpx solid transparent;
    border-right: 8rpx solid transparent;
    border-top: 8rpx solid rgba(0, 0, 0, 0.8);
  }
}

.tooltip-text {
  font-size: 24rpx;
  color: #ffffff;
  white-space: nowrap;
}

.chapter-markers {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.chapter-marker {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  pointer-events: all;
  z-index: 5;
  
  &:hover .marker-tooltip {
    opacity: 1;
    transform: translateX(-50%) translateY(-8rpx);
  }
}

.marker-dot {
  width: 12rpx;
  height: 12rpx;
  border-radius: 50%;
  background: #ff9500;
  border: 2rpx solid #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    transform: scale(1.3);
    box-shadow: 0 4rpx 12rpx rgba(255, 149, 0, 0.4);
  }
}

.marker-tooltip {
  position: absolute;
  bottom: 40rpx;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 149, 0, 0.9);
  color: #ffffff;
  padding: 8rpx 12rpx;
  border-radius: 6rpx;
  font-size: 20rpx;
  white-space: nowrap;
  opacity: 0;
  transition: all 0.2s ease;
  pointer-events: none;
  
  &::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 6rpx solid transparent;
    border-right: 6rpx solid transparent;
    border-top: 6rpx solid rgba(255, 149, 0, 0.9);
  }
}

// 不同尺寸变体
.progress-bar-container.small {
  .progress-track {
    height: 4rpx;
  }
  
  .progress-thumb {
    width: 20rpx;
    height: 20rpx;
  }
}

.progress-bar-container.large {
  .progress-track {
    height: 10rpx;
  }
  
  .progress-thumb {
    width: 36rpx;
    height: 36rpx;
  }
}

// 主题变体
.progress-bar-container.dark {
  .progress-track {
    background-color: rgba(255, 255, 255, 0.2);
  }
  
  .progress-buffered {
    background-color: rgba(255, 255, 255, 0.4);
  }
}

.progress-bar-container.minimal {
  .progress-thumb {
    display: none;
  }
  
  .time-tooltip {
    display: none;
  }
  
  .chapter-markers {
    display: none;
  }
}
</style>