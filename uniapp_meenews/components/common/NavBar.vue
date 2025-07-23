<template>
  <fui-navbar :title="title" :background="background" :color="color" :fixed="fixed">
    <template #left>
      <slot name="left"></slot>
    </template>
    <template #center>
      <slot name="center">{{ title }}</slot>
    </template>
    <template #right>
      <slot name="right"></slot>
    </template>
  </fui-navbar>
</template>

<script>
export default {
  name: 'NavBar',
  props: {
    title: { type: String, default: '' },
    background: { type: String, default: '#fff' },
    color: { type: String, default: '#2c3038' },
    fixed: { type: Boolean, default: true }
  }
}
</script> 