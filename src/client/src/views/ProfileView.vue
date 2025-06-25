<template>
  <div class="profile">
    <h1>Hier kommt das Profil hin :P</h1>
    <div class="settings-container">
      <button class="settings-btn" @click="showMenu = !showMenu">
        Einstellungen ⚙️
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
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 1rem;
}
.settings-popup {
  position: absolute;
  top: 40px;
  right: 0;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(34,34,34,0.08);
  padding: 12px 18px;
  z-index: 10;
}
.logout-btn {
  background: #ffdddd;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  color: #c00;
  cursor: pointer;
  font-weight: 500;
}
</style>
