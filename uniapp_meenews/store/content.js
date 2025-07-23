import { defineStore } from 'pinia'

export const useContentStore = defineStore('content', {
  state: () => ({
    recommendList: [],
    categoryList: [],
    recentPlayed: [],
    artistList: [],
    albumList: [],
    pageStartTime: null // 新增：页面进入时间
  }),
  actions: {
    setRecommendList(list) { this.recommendList = list },
    setCategoryList(list) { this.categoryList = list },
    setRecentPlayed(list) { this.recentPlayed = list },
    setArtistList(list) { this.artistList = list },
    setAlbumList(list) { this.albumList = list },
    // 新增：设置页面进入时间
    setPageStartTime(time) { this.pageStartTime = time },
    // 新增：获取页面进入时间
    getPageStartTime() { return this.pageStartTime }
  }
}) 