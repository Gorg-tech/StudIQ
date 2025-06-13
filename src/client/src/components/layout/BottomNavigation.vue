<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import IconHome from '../icons/IconHome.vue'
import IconSearch from '../icons/IconSearch.vue'
import IconProfile from '../icons/IconProfile.vue'

const router = useRouter()
const activeTab = ref('home')

const navigateTo = (route, tab) => {
  activeTab.value = tab
  router.push(route)
}
</script>

<template>
  <nav class="bottom-navigation">
    <button
      @click="navigateTo('/', 'home')"
      :class="{ active: activeTab === 'home' }"
      aria-label="Home"
    >
      <IconHome />
      <span>Home</span>
    </button>
    <button
      @click="navigateTo('/search', 'search')"
      :class="{ active: activeTab === 'search' }"
      aria-label="Suche"
    >
      <IconSearch />
      <span>Suche</span>
    </button>
    <button
      @click="navigateTo('/profile', 'profile')"
      :class="{ active: activeTab === 'profile' }"
      aria-label="Profil"
    >
      <IconProfile />
      <span>Profil</span>
    </button>
  </nav>
</template>

<style scoped>
.bottom-navigation {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  background-color: var(--color-bg);
  box-shadow: 0 -2px 5px rgba(34, 34, 34, 0.08);
  padding: 8px 0;
  z-index: 100;
}

button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px 16px;
  color: var(--color-muted);
  transition: color 0.3s;
  flex: 1;
}

button span {
  font-size: 12px;
  margin-top: 4px;
}

button.active {
  color: var(--color-primary);
}

/* Desktop adjustments */
@media (min-width: 1024px) {
  .bottom-navigation {
    position: fixed;
    width: 100%;
    max-width: 500px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 24px 24px 0 0;
  }
}
</style>