

<template>
  <div class="profile">
    <h1>Hier kommt das Profil hin :P</h1>
    <div class="settings-container">
      <button class="settings-btn" @click="router.push('/settings/')" aria-label="Einstellungen">
        <IconSettings />
      </button>
      <div v-if="showMenu" class="settings-popup">
        <button class="logout-btn" @click="handleLogout">Ausloggen</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { logout, isAuthenticated } from '@/services/auth'
import IconSettings from '@/components/icons/IconSettings.vue'

const showMenu = ref(false)
const router = useRouter()

async function handleLogout() {
  try {
    await logout()
    isAuthenticated.value = false;
    router.push('/login')
  } catch (e) {
    // Fehlerbehandlung (optional)
    console.error(e)
  }
}
</script>

<style scoped>
.profile {
  position: relative;
}
.settings-container {
  position: absolute;
  top: 20px;
  right: 30px;
}
.settings-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  padding-top: 8px;
  margin-left: auto;
  display: flex;
  align-items: center;
  color: var(--color-primary);
  transition: color 0.2s;
}
.settings-btn:hover {
  color: var(--color-accent);
}

.settings-btn svg {
  width: 2.2rem;
  height: 2.2rem;
}
</style>
