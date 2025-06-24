<template>
  <div class="register-container">
    <div class="logo-top">
      <LogoStudIQ />
    </div>
    <div class="register-card">
      <h1 class="register-title">Registrierung</h1>
      <form @submit.prevent="handleRegister" class="register-form">
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
          <label for="studiengruppe">Studiengruppe <span class="hint">(Immat.jahr/Studiengang/Gruppe)</span>:</label>
          <input id="studiengruppe" v-model="studiengruppe" placeholder="z.B. 2022/INF/1" required />
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/services/auth'
import LogoStudIQ from '@/components/LogoStudIQ.vue'

const username = ref('')
const email = ref('')
const password = ref('')
const studiengruppe = ref('')
const router = useRouter()

async function handleRegister() {
  try {
    const [immatJahr, studiengang, gruppe] = studiengruppe.value.split('/')

    const response = await register({
      username: username.value,
      email: email.value,
      password: password.value,
      immatJahr,
      studiengang,
      gruppe,
    })

    router.push('/')
  } catch (err) {
    if (err.data) {
      console.log('Registrierung fehlgeschlagen: ' + JSON.stringify(err.data))
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
  background: #fff;
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
</style>