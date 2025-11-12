<template>
  <div class="register-container">
    <div class="logo-top">
      <LogoStudIQ />
    </div>
    <div class="register-card">
      <h1 class="register-title">Registrierung</h1>
      <form @submit.prevent="handleRegister" class="register-form">
        <div v-if="errorMsg" class="register-error">
          {{ errorMsg }}
        </div>
        <div class="form-group">
          <label for="username">Benutzername:</label>
          <input id="username" v-model="username" required />
        </div>

        <div class="form-group">
          <label for="email">E-Mail:</label>
          <input id="email" type="email" v-model="email" required />
        </div>

        <div class="form-group">
          <label for="password">Passwort:</label>
          <input id="password" type="password" v-model="password" required />
        </div>

        <div class="form-group">
          <label for="studiengang">Studiengang:</label>
          <!-- Removed separate search input; single dropdown only -->
          <select v-model="studiengang" required>
            <option value="">Wähle einen Studiengang</option>
            <option v-for="sg in studiengaenge" :key="sg.id" :value="sg.id">{{ sg.id }} - {{ sg.name }}</option>
          </select>
        </div>

        <button type="submit" class="btn btn-primary register-btn">Registrieren</button>
      </form>

      <p class="register-login-hint">
        Schon registriert?
        <router-link to="/login" class="login-link">Zum Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/services/auth'
import { getStudiengaenge } from '@/services/studiengaenge'
import LogoStudIQ from '@/components/LogoStudIQ.vue'

const username = ref('')
const email = ref('')
const password = ref('')
const studiengang = ref('')
const errorMsg = ref('')
const studiengaenge = ref([])
const router = useRouter()

onMounted(async () => {
  try {
    const response = await getStudiengaenge()

    studiengaenge.value = Array.isArray(response) ? response : []
  } catch (err) {
    console.error('Failed to fetch studiengaenge:', err)
    studiengaenge.value = []
  }
})

async function handleRegister() {
  errorMsg.value = ''
  try {
    await register({
      username: username.value,
      email: email.value,
      password: password.value,
      studiengang: studiengang.value,
    })
    router.push('/')
  } catch (err) {
    if (err?.data) {
      if (typeof err.data === 'object') {
        errorMsg.value = Object.values(err.data).flat().join(' ')
      } else {
        errorMsg.value = err.data
      }
    } else {
      errorMsg.value = 'Unbekannter Fehler bei der Registrierung.'
    }
  }
}
</script>

<style scoped>
.register-container {
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

.register-card {
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
  padding: 32px 24px 24px 24px;
  max-width: 420px;
  width: 100%;
  margin: 32px 0;
  text-align: center;
}

.register-title {
  margin-bottom: 18px;
  color: var(--color-accent);
  font-size: 2rem;
  font-weight: 500;
}

.register-form {
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

.form-group .hint {
  font-size: 0.9em;
  color: var(--color-muted);
  font-weight: 400;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  font-size: 1rem;
  background: var(--card-bg);
  color: var(--color-text);
  transition: border 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  border: 1.5px solid var(--color-primary);
  outline: none;
  background: var(--card-bg);
}

.register-btn {
  margin-top: 10px;
  width: 100%;
  font-size: 1.1rem;
  padding: 12px 0;
}

.register-login-hint {
  margin-top: 18px;
  color: var(--color-muted);
  font-size: 1rem;
}

.login-link {
  color: var(--color-primary);
  text-decoration: underline;
  margin-left: 4px;
}

.register-error {
  color: var(--color-danger);
  background: var(--color-danger-bg);
  border: 1px solid var(--color-danger-border);
  border-radius: 6px;
  padding: 10px 14px;
  margin-bottom: 12px;
  font-size: 1rem;
}
</style>
