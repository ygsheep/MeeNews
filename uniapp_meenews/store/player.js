import { defineStore } from 'pinia'

export const usePlayerStore = defineStore('player', {
  state: () => ({
    currentTrack: null,
    isPlaying: false,
    currentTime: 0,
    duration: 0,
    playlist: [],
    currentIndex: 0,
    currentContent: null
  }),
  actions: {
    playTrack(track) {
      this.currentTrack = track
      this.isPlaying = true
      // 这里可扩展音频API调用
    },
    pause() { this.isPlaying = false },
    setCurrentTime(time) { this.currentTime = time },
    setDuration(duration) { this.duration = duration },
    setPlaylist(list) { this.playlist = list },
    setCurrentIndex(idx) { this.currentIndex = idx },
    setCurrentContent(content) {
      this.currentContent = content
    }
  }
}) 