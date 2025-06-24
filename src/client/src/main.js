import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { checkAuth } from './services/auth'

checkAuth().then(() => {
  const app = createApp(App)
  app.config.devtools = false; // Disable Vue DevTools

  app.use(createPinia())
  app.use(router)

  app.mount('#app')
})
