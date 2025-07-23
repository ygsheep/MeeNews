<template>
  <button :class="['follow-btn', { followed }]" @click="$emit('toggle', !followed)">
    <fui-icon :name="followed ? 'check' : 'add'" :color="followed ? '#fff' : '#4CD964'" size="24" />
    <text>{{ followed ? '已关注' : '关注' }}</text>
  </button>
</template>

<script>
export default {
  name: 'FollowButton',
  props: {
    followed: { type: Boolean, default: false }
  },
  emits: ['toggle']
}
</script>

<style scoped>
.follow-btn {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 24rpx;
  border: none;
  border-radius: 32rpx;
  background: #4CD964;
  color: #fff;
  font-size: 26rpx;
  cursor: pointer;
  transition: background 0.2s;
}
.follow-btn.followed {
  background: #8d96a0;
  color: #fff;
}
</style> 