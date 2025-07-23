<template>
  <fui-loading :show="show" :text="text" :size="size" :color="color" />
</template>

<script>
export default {
  name: 'Loading',
  props: {
    show: { type: Boolean, default: true },
    text: { type: String, default: '加载中...' },
    size: { type: [Number, String], default: 48 },
    color: { type: String, default: '#4CD964' }
  }
}
</script> 