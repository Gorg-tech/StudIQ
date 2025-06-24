<script setup>
// Importiere benötigte Funktionen von Vue
import { ref } from 'vue'
// Importiere Router für Navigation
import { useRouter } from 'vue-router'

import { login } from '@/services/auth'
import LogoStudIQ from '@/components/LogoStudIQ.vue'

// Router-Instanz initialisieren
const router = useRouter()
// Reaktive Variablen für E-Mail und Passwort
const username = ref('')
const password = ref('')
const error = ref('')

  async function handleLogin() {
    if (username.value === '' || password.value === '') {
    error.value = 'Bitte Benutzername und Passwort eingeben.'
    return
  }
  try {
    //übergeben die Strings zum Server
    const user = await login({ username: username.value, password: password.value });
     console.log('User:' + user)
     if (user) {
      router.push('/')
    } else {
      error.value = 'Falscher Benutzername oder Passwort.'

    }
    // Weiterleitung oder User speichern
  } catch (err) {
    error.value = 'Fehler beim Login.'

  }
}

</script>

<template>
  <div class="login-container">
    <div class="logo-top">
      <LogoStudIQ />
    </div>
    <div class="login-card">
      <h1 class="login-title">Login</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Benutzername:</label>
          <input
            id="username"
            v-model="username"
            required
            class="form-control"
            autocomplete="username"
          />
        </div>
        <div class="form-group">
          <label for="password">Passwort:</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="form-control"
            autocomplete="current-password"
          />
        </div>
        <button class="btn btn-primary login-btn" type="submit">
          Einloggen
        </button>
        <div
  v-if="error"
  class="login-error"
  :style="{ opacity: error ? 1 : 0 }"
>
  {{ error }}
</div>
      </form>
      <p class="login-register-hint">
        Noch kein Account?
        <router-link to="/register" class="register-link">Zur Registrierung</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  background: none;
}

.logo-top {
  margin-bottom: 18px;
  font-size: 2.8rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
  padding: 32px 24px 24px 24px;
  max-width: 420px;
  width: 100%;
  margin: 32px 0;
  text-align: center;
}

.login-title {
  margin-bottom: 18px;
  color: var(--color-accent);
  font-size: 2rem;
  font-weight: 500;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  color: var(--color-muted);
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  border: 1px solid #eee;
  font-size: 1rem;
  background: #f9f9f9;
  transition: border 0.2s;
}

.form-group input:focus {
  border: 1.5px solid var(--color-primary);
  outline: none;
  background: #fff;
}

.login-btn {
  margin-top: 10px;
  width: 100%;
  font-size: 1.1rem;
  padding: 12px 0;
}

.login-register-hint {
  margin-top: 18px;
  color: var(--color-muted);
  font-size: 1rem;
}

.register-link {
  color: var(--color-primary);
  text-decoration: underline;
  margin-left: 4px;
}

.login-error {
  color: red;
  margin-top: 10px;
  opacity: 0;
  transition: opacity 0.7s;
  min-height: 24px;
}
.login-error[style] {
  opacity: 1 !important;
}
</style>
