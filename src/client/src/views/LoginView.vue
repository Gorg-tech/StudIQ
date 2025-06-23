<template>
  <div class="flex flex-col max-w-sm mx-auto p-4 gap-3">
    <h1 class="text-xl font-semibold text-center">Login</h1>

    <input
      v-model="username"
      type="text"
      placeholder="Benutzername"
      class="border rounded p-2"
    />

    <input
      v-model="password"
      type="password"
      placeholder="Passwort"
      class="border rounded p-2"
    />

    <button
      @click="doLogin"
      class="bg-blue-600 text-white rounded p-2 hover:bg-blue-700 transition"
    >
      Einloggen
    </button>

    <p v-if="errorMsg" class="text-red-600 text-sm">{{ errorMsg }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api/client.js'

const router = useRouter()
const username = ref('')
const password = ref('')
const errorMsg = ref('')

async function doLogin() {
  errorMsg.value = ''
  try {
    await apiClient.login(username.value, password.value)
    router.push({ name: 'search' })
  } catch (err) {
    // Backend liefert {detail: "..."}
    errorMsg.value = err?.detail || 'Login fehlgeschlagen'
  }
}
</script>

<style scoped>
/* minimaler Style, unverändert anpassbar */
</style>
