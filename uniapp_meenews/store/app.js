import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    theme: 'light',
    network: 'online'
  }),
  actions: {
    setTheme(theme) { this.theme = theme },
    setNetwork(status) { this.network = status }
  }
}) 