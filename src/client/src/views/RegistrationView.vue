<template>
  <div class="register">
    <h1>Registrierung</h1>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="username">Benutzername:</label>
        <input id="username" v-model="username" required />
      </div>

      <div>
        <label for="email">E-Mail:</label>
        <input id="email" type="email" v-model="email" required />
      </div>

      <div>
        <label for="password">Passwort:</label>
        <input id="password" type="password" v-model="password" required />
      </div>

      <div>
        <label for="studiengang">Studiengang:</label>
        <input id="studiengang" v-model="studiengang" />
      </div>

      <div>
        <label for="semester">Semester:</label>
        <input id="semester" type="number" v-model="semester" />
      </div>

      <button type="submit">Registrieren</button>
    </form>

    <p>
      Schon registriert?
      <router-link to="/login">Zum Login</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/services/auth'

const username = ref('')
const email = ref('')
const password = ref('')
const studiengang = ref('')
const semester = ref(1)
const router = useRouter()

async function handleRegister() {
  try {
    const response = await register({
      username: username.value,
      email: email.value,
      password: password.value,
      studiengang: studiengang.value,
      semester: semester.value,
    })

    const { tokens, user } = response.data

    localStorage.setItem('access_token', tokens.access)
    localStorage.setItem('user', JSON.stringify(user))

    router.push('/')
  } catch (err) {
    console.error(err)
    alert('Registrierung fehlgeschlagen.')
  }
}
</script>

<style scoped>
.register {
  max-width: 500px;
  margin: auto;
  padding: 1rem;
}
.register label {
  display: block;
  margin-top: 1rem;
}
.register input {
  width: 100%;
  padding: 0.5rem;
}
.register button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
}
</style>
