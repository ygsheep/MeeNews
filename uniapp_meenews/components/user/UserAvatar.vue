<template>
  <BaseImage :src="src" :style="avatarStyle" class="user-avatar" @click="$emit('click')" />
</template>

<script>
import BaseImage from '@/components/common/BaseImage.vue'
export default {
  name: 'UserAvatar',
  components: { BaseImage },
  props: {
    src: { type: String, default: '/static/images/common/img_logo.png' },
    size: { type: [Number, String], default: 80 },
    round: { type: Boolean, default: true }
  },
  computed: {
    avatarStyle() {
      return {
        width: this.size + 'rpx',
        height: this.size + 'rpx',
        borderRadius: this.round ? '50%' : '8rpx',
        objectFit: 'cover'
      }
    }
  }
}
</script>

<style scoped>
.user-avatar {
  display: block;
  background: #f1f4fa;
}
</style> 