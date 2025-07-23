<template>
  <view :class="['content-list', direction]">
    <ContentCard v-for="item in list" :key="item.id" :content="item" :cardType="cardType" @click="$emit('itemClick', item)" @like="$emit('itemLike', item)" />
  </view>
</template>

<script>
import ContentCard from './ContentCard.vue'
export default {
  name: 'ContentList',
  components: { ContentCard },
  props: {
    list: { type: Array, default: () => [] },
    cardType: { type: String, default: 'small' },
    direction: { type: String, default: 'vertical' } // vertical | horizontal
  },
  emits: ['itemClick', 'itemLike']
}
</script>

<style scoped>
.content-list.vertical {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}
.content-list.horizontal {
  display: flex;
  flex-direction: row;
  gap: 24rpx;
  overflow-x: auto;
}
</style> 