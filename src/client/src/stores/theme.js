import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    darkmode: false
  }),
  actions: {
    toggleTheme() {
      this.darkmode = !this.darkmode
      this.applyTheme()
      localStorage.setItem('darkmode', this.darkmode)
    },
    loadTheme() {
      const saved = localStorage.getItem('darkmode')
      this.darkmode = saved === 'true'
      this.applyTheme()
    },
    applyTheme() {
      if (this.darkmode) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }
  }
})
