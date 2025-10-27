import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { checkAuth } from './services/auth'
import { useThemeStore } from '@/stores/theme'

async function bootstrap() {
  await checkAuth() // Auth prüfen

  const app = createApp(App)
  app.config.devtools = false // Vue DevTools deaktivieren

  const pinia = createPinia()
  app.use(pinia)
  app.use(router)

  // Theme-Store laden **vor Mount**
  const themeStore = useThemeStore(pinia)
  themeStore.loadTheme()
  console.log('Darkmode nach loadTheme:', themeStore.darkmode)

  app.mount('#app')
}

bootstrap()
