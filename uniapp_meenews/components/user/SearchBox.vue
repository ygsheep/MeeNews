<template>
  <view class="search-box">
    <input class="input" type="text" :placeholder="placeholder" v-model="keyword" @input="$emit('input', keyword)" @confirm="onSearch" />
    <fui-icon v-if="keyword" name="close" color="#8d96a0" size="24" class="clear-btn" @click="clear" />
    <fui-icon name="search" color="#4CD964" size="28" class="search-btn" @click="onSearch" />
  </view>
</template>

<script>
export default {
  name: 'SearchBox',
  props: {
    placeholder: { type: String, default: '搜索' },
    value: { type: String, default: '' }
  },
  emits: ['input', 'search', 'clear'],
  data() {
    return { keyword: this.value }
  },
  watch: {
    value(val) { this.keyword = val }
  },
  methods: {
    clear() {
      this.keyword = ''
      this.$emit('clear')
      this.$emit('input', '')
    },
    onSearch() {
      this.$emit('search', this.keyword)
    }
  }
}
</script>

<style scoped>
.search-box {
  display: flex;
  align-items: center;
  background: #f1f4fa;
  border-radius: 32rpx;
  padding: 0 24rpx;
  height: 64rpx;
  position: relative;
}
.input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 28rpx;
  color: #2c3038;
  outline: none;
  height: 100%;
}
.clear-btn {
  margin-left: 8rpx;
  cursor: pointer;
}
.search-btn {
  margin-left: 12rpx;
  cursor: pointer;
}
</style> 