<template>
  <fui-backtop :bottom="bottom" :right="right" :color="color" :background="background" />
</template>

<script>
export default {
  name: 'BackToTop',
  props: {
    bottom: { type: [Number, String], default: 120 },
    right: { type: [Number, String], default: 32 },
    color: { type: String, default: '#fff' },
    background: { type: String, default: '#4CD964' }
  }
}
</script> 