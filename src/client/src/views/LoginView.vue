<script setup>
// Importiere benötigte Funktionen von Vue
import { ref } from 'vue'
// Importiere Router für Navigation
import { useRouter } from 'vue-router'

import { login } from '@/services/auth'

// Router-Instanz initialisieren
const router = useRouter()
// Reaktive Variablen für E-Mail und Passwort
const username = ref('')
const password = ref('')
const error = ref('')

// Login-Funktion, hier sollte der API-Call erfolgen


  async function handleLogin() {
    if (username.value === '' || password.value === '') {
    error.value = 'Bitte Email und Passwort eingeben.'
    return
  }
  try {
    //übergeben die Strings zum Server
    const user = await login({ username: username.value, password: password.value });
     if (user) {
      router.push('/')
    } else {
      error.value = 'Falscher Username oder Passwort.'
    }
    // Weiterleitung oder User speichern
  } catch (err) {
    error.value = 'Fehler beim Login.'

  }
}

</script>

<template>
  <div class="login">
    <h1>Login</h1>
    <!-- Login-Formular -->
    <form @submit.prevent="handleLogin">
      <input
        v-model="username"
        type="username"
        placeholder="Username"
        required
        class="form-control"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Passwort"
        required
        class="form-control"
      />
      <button class="btn btn-primary" type="submit">
        Einloggen
      </button>
      <!-- Fehlermeldung anzeigen -->
      <div v-if="error" style="color: red; margin-top: 10px;">{{ error }}</div>
    </form>
    <br>
    <!-- Button zur Registrierungsseite -->
    <button class="btn btn-secondary" @click="router.push('/register')">
      Zur Registrierung
    </button>
  </div>
</template>

<style>
.login {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}
.form-control {
  display: block;
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.5rem;
}
</style>
