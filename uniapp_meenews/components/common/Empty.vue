<template>
  <fui-empty :show="show" :text="text" :imgUrl="imgUrl" />
</template>

<script>
export default {
  name: 'Empty',
  props: {
    show: { type: Boolean, default: true },
    text: { type: String, default: '暂无数据' },
    imgUrl: { type: String, default: '/static/images/component/empty/img_data_3x.png' }
  }
}
</script> 