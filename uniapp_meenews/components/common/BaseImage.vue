<template>
  <image
    :src="src || defaultSrc"
    :mode="mode"
    lazy-load
    :class="imgClass"
    @error="onError"
  />
</template>

<script>
export default {
  name: 'BaseImage',
  props: {
    src: String,
    mode: { type: String, default: 'aspectFill' },
    imgClass: String,
    defaultSrc: { type: String, default: '/static/images/common/img_logo.png' }
  },
  methods: {
    onError(e) {
      // 可设置默认占位图
      if (e && e.target) e.target.src = this.defaultSrc
    }
  }
}
</script> 