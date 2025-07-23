<template>
  <view :class="['content-card', `card-${cardType}`]" @click="handleClick">
    <!-- 封面及类型icon -->
    <view class="cover-container">
      <BaseImage :src="content.coverUrl" class="cover" mode="aspectFill" />
      <!-- 类型icon（音频/视频/文章） -->
      <view class="type-icon" v-if="content.type">
        <fui-icon :name="typeIconName" :color="typeIconColor" size="22" />
      </view>
      <!-- 时长/字数 -->
      <text class="duration" v-if="showDuration">{{ durationOrWordCount }}</text>
    </view>
    <!-- 内容信息区 -->
    <view class="info">
      <text class="title">{{ content.title }}</text>
      <text class="author" v-if="content.author">{{ content.author }}</text>
      <!-- 文章摘要 -->
      <text class="summary" v-if="content.type === 'article' && content.summary">{{ content.summary }}</text>
      <!-- 标签 -->
      <view class="tags" v-if="Array.isArray(content.tags) && content.tags.length">
        <text class="tag" v-for="tag in content.tags" :key="tag">{{ tag }}</text>
      </view>
      <!-- 播放量/阅读量/喜欢 -->
      <view v-if="cardType === 'list'" class="meta">
        <text class="play-count" v-if="showPlayCount">{{ formatPlayCount(content.playCount) }}{{ playCountLabel }}</text>
        <fui-icon v-if="showLike" :name="content.isLiked ? 'heart-fill' : 'heart'" :color="content.isLiked ? '#ff3b30' : '#8d96a0'" size="20" @click.stop="toggleLike" />
      </view>
    </view>
  </view>
</template>

<script>
import BaseImage from '@/components/common/BaseImage.vue'
/**
 * 通用多媒体内容卡片组件
 * 支持音频、视频、文章资讯内容
 * 业务健壮、可扩展、可维护
 */
export default {
  name: 'ContentCard',
  components: { BaseImage },
  props: {
    // 内容对象，需包含 type、coverUrl、title、author、duration、playCount、summary、tags、isLiked 等字段
    content: { type: Object, required: true },
    // 卡片类型：small | list | medium | large
    cardType: { type: String, default: 'small' }
  },
  emits: ['click', 'like'],
  computed: {
    // 类型icon名称
    typeIconName() {
      switch (this.content.type) {
        case 'audio': return 'music';
        case 'video': return 'video';
        case 'article': return 'file-text';
        default: return 'file';
      }
    },
    // 类型icon颜色
    typeIconColor() {
      switch (this.content.type) {
        case 'audio': return '#4CD964';
        case 'video': return '#5856d6';
        case 'article': return '#ff9500';
        default: return '#8d96a0';
      }
    },
    // 是否显示时长/字数
    showDuration() {
      if (this.content.type === 'audio' || this.content.type === 'video') {
        return typeof this.content.duration === 'number' && this.content.duration > 0
      }
      if (this.content.type === 'article') {
        return typeof this.content.wordCount === 'number' && this.content.wordCount > 0
      }
      return false
    },
    // 时长（音频/视频）或字数（文章）
    durationOrWordCount() {
      if (this.content.type === 'audio' || this.content.type === 'video') {
        return this.formatDuration(this.content.duration)
      }
      if (this.content.type === 'article') {
        return this.formatWordCount(this.content.wordCount)
      }
      return ''
    },
    // 是否显示播放量/阅读量
    showPlayCount() {
      return typeof this.content.playCount === 'number' && this.content.playCount >= 0
    },
    // 播放量/阅读量label
    playCountLabel() {
      switch (this.content.type) {
        case 'audio': return '次播放';
        case 'video': return '次播放';
        case 'article': return '次阅读';
        default: return '';
      }
    },
    // 是否显示喜欢按钮
    showLike() {
      return this.content.type === 'audio' || this.content.type === 'video'
    }
  },
  methods: {
    /**
     * 点击卡片
     */
    handleClick() {
      this.$emit('click', this.content)
    },
    /**
     * 喜欢/取消喜欢
     */
    toggleLike() {
      this.$emit('like', this.content)
    },
    /**
     * 格式化时长（秒转分:秒）
     */
    formatDuration(sec) {
      if (!sec || typeof sec !== 'number' || sec < 0) return ''
      const m = Math.floor(sec / 60)
      const s = Math.floor(sec % 60)
      return `${m}:${s.toString().padStart(2, '0')}`
    },
    /**
     * 格式化字数（如 1.2K字）
     */
    formatWordCount(count) {
      if (!count || typeof count !== 'number' || count < 0) return ''
      if (count >= 10000) return (count / 10000).toFixed(1) + '万字'
      if (count >= 1000) return (count / 1000).toFixed(1) + 'K字'
      return count + '字'
    },
    /**
     * 格式化播放量/阅读量
     */
    formatPlayCount(count) {
      if (!count || typeof count !== 'number' || count < 0) return 0
      if (count >= 1000000) return (count / 1000000).toFixed(1) + 'M'
      if (count >= 1000) return (count / 1000).toFixed(1) + 'K'
      return count
    }
  }
}
</script>

<style scoped>
.content-card {
  background: #fff;
  border-radius: 12rpx;
  overflow: hidden;
  margin-bottom: 24rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.34);
  cursor: pointer;
  transition: transform 0.2s;
}
.card-small {
  width: 280rpx;
}
.card-list {
  display: flex;
  align-items: center;
  padding: 24rpx;
}
.cover-container {
  position: relative;
  border-radius: 12rpx;
  overflow: hidden;
}
.cover {
  width: 100%; height: 100%;
}
.type-icon {
  position: absolute;
  top: 12rpx; left: 12rpx;
  background: rgba(255,255,255,0.9);
  border-radius: 8rpx;
  padding: 4rpx 8rpx;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
}
.duration {
  position: absolute;
  bottom: 16rpx; right: 16rpx;
  font-size: 20rpx;
  color: #fff;
  background: rgba(0,0,0,0.6);
  padding: 4rpx 8rpx;
  border-radius: 4rpx;
}
.info {
  padding: 16rpx;
}
.title {
  font-size: 28rpx; font-weight: 500; color: #2c3038; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.author {
  font-size: 24rpx; color: #8d96a0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.summary {
  font-size: 24rpx; color: #666; margin-top: 8rpx; display: block; white-space: normal; overflow: hidden; text-overflow: ellipsis; max-height: 3em;
}
.tags {
  margin-top: 8rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
}
.tag {
  font-size: 20rpx;
  color: #4CD964;
  background: #eafaf0;
  border-radius: 6rpx;
  padding: 2rpx 10rpx;
}
.meta {
  display: flex; align-items: center; justify-content: space-between;
  margin-top: 8rpx;
}
.play-count {
  font-size: 22rpx; color: #8d96a0;
}
</style> 