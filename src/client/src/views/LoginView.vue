<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Benutzername:</label>
        <input id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Passwort:</label>
        <input id="password" type="password" v-model="password" required />
      </div>
      <button type="submit">Einloggen</button>
    </form>

    <p>
      Noch keinen Account?
      <router-link to="/register">Registrieren</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/services/auth'

const username = ref('')
const password = ref('')
const router = useRouter()

async function handleLogin() {
  try {
    const response = await login({ username: username.value, password: password.value })
    const { tokens, user } = response.data

    // Save access token (you can also save refresh if needed)
    localStorage.setItem('access_token', tokens.access)

    // Optional: save user info or role
    localStorage.setItem('user', JSON.stringify(user))

    // Go to home/dashboard
    router.push('/')
  } catch (err) {
    console.error(err)
    alert('Login fehlgeschlagen: Benutzername oder Passwort falsch.')
  }
}
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: auto;
  padding: 1rem;
}
.login label {
  display: block;
  margin-top: 1rem;
}
.login input {
  width: 100%;
  padding: 0.5rem;
}
.login button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
}
</style>
