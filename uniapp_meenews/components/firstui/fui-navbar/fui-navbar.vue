<template>
  <view class="fui-navbar">
    <slot name="left"></slot>
    <text class="fui-navbar-title">{{ title }}</text>
    <slot name="right"></slot>
  </view>
</template>

<script>
export default {
  name: 'FuiNavbar',
  props: {
    title: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.fui-navbar {
  display: flex;
  align-items: center;
  height: 88rpx;
  background: #fff;
  border-bottom: 1rpx solid #eee;
  padding: 0 24rpx;
}
.fui-navbar-title {
  flex: 1;
  text-align: center;
  font-size: 32rpx;
  font-weight: bold;
}
</style> 