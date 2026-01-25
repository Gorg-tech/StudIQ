<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useUserStore } from '@/stores/user'
import { logout } from '@/services/auth'
import { getSelfUser } from '@/services/user'

const router = useRouter()
const themeStore = useThemeStore()
const userStore = useUserStore()

const username = ref('')
const password = ref('••••••••')   // niemals echtes Passwort laden
const email = ref('')
const language = ref('Deutsch')

const showPassword = ref(false)
const showCreditsModal = ref(false)

onMounted(async () => {
  try {
    const self = await getSelfUser()

    username.value = self.username
    email.value    = self.email
  } catch (error) {
    console.error('Fehler beim Laden der Nutzerdaten', error)
  }
})

// Aktionen
const goBack = () => router.push('/')
const toggleDarkmode = () => themeStore.toggleTheme()
const changePassword = () => alert('Passwort ändern (noch Dummy)')
const changeLanguage = () => alert('Sprache ändern (noch Dummy)')
const togglePasswordVisibility = () => (showPassword.value = !showPassword.value)
const showCredits = () => showCreditsModal.value = true
const closeCreditsModal = () => showCreditsModal.value = false

const handleLogout = async () => {
  try {
    await userStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
</script>


<template>
  <div class="edit-quiz-view">
    <header class="edit-header">
      <h1>Einstellungen</h1>
      <button class="credit-btn" @click="showCredits">i</button>
    </header>

    <main class="edit-main">
      <!-- Darstellung -->
      <section class="quiz-questions-section card">
        <label class="block-label">Darstellung</label>
        <div class="setting-item">
          <p>Darkmode</p>
          <label class="switch">
            <input type="checkbox" :checked="themeStore.darkmode" @change="toggleDarkmode" />
            <span class="slider"></span>
          </label>
        </div>
      </section>

      <!-- Allgemein -->
      <section class="quiz-title-section card">
        <label class="block-label">Allgemein</label>
        <div class="setting-item">
          <p>E-Mail: <b>{{ email }}</b></p>
        </div>
        <div class="setting-item">
          <p>Benutzername: <b>{{ username }}</b></p>
        </div>
        <div class="setting-item">
          <p>Passwort:
            <b>{{ showPassword ? password : '••••••••' }}</b>
          </p>
        </div>
      </section>

      <!-- Aktionen -->
      <div class="edit-actions-column">
        <button class="btn btn-secondary" @click="goBack">Zurück</button>
        <button class="btn btn-primary login-btn" @click="handleLogout">Ausloggen</button>
      </div>
    </main>

    <!-- Credits Modal -->
    <div v-if="showCreditsModal" class="modal-overlay" @click="closeCreditsModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Rechtliche Hinweise</h2>
          <button class="modal-close" @click="closeCreditsModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="legal-section">
            <h3>1. Verantwortliche Stelle</h3>
            <p>Diese Quiz-App wird im Rahmen eines studentischen Projekts vom StudIQ-Entwicklerteam betrieben.</p>
            <p>Kontakt: s86430@htw-dresden.de</p>
          </div>

          <div class="legal-section">
            <h3>2. Welche Daten werden verarbeitet?</h3>
            <p>Wir verarbeiten nur Daten, die für den Betrieb der App notwendig sind:</p>
            <ul>
              <li>Benutzername (Pseudonym)</li>
              <li>Studiengang</li>
              <li>Quiz-Ergebnisse, Punkte, Streaks und Lernfortschritt</li>
              <li>Erstellte Quizzes und Bewertungen</li>
              <li>Technisch notwendige Daten (z. B. Login-Status)</li>
            </ul>
          </div>

          <div class="legal-section">
            <h3>3. Zweck der Datenverarbeitung</h3>
            <p>Die Daten werden verwendet, um:</p>
            <ul>
              <li>Quizze durchzuführen und auszuwerten</li>
              <li>Punkte, Streaks und Lernfortschritte zu berechnen</li>
              <li>ein studiengangsbezogenes Leaderboard anzuzeigen</li>
              <li>selbst erstellte Quizzes zu verwalten</li>
            </ul>
          </div>

          <div class="legal-section">
            <h3>4. Rechtsgrundlage</h3>
            <p>Die Verarbeitung erfolgt gemäß Art. 6 Abs. 1 b DSGVO sowie Art. 6 Abs. 1 f DSGVO.</p>
          </div>

          <div class="legal-section">
            <h3>5. Speicherung & Löschung</h3>
            <p>Daten werden nur so lange gespeichert, wie das Nutzerkonto besteht.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.edit-quiz-view {
  max-width: 600px;
  margin: 0 auto;
  padding: 24px 12px 0 12px;
  display: flex;
  flex-direction: column;
}

.edit-header {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.edit-header h1 {
  font-size: 2rem;
  font-weight: 700;
}

/* Credit Button rechts von der Überschrift */
.credit-btn {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  background-color: darkorange;
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.credit-btn:hover {
  background-color: darkorange;
}

.edit-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.card {
  background: var(--bg-color, #fff);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
  padding: 20px;
}

.block-label {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 6px;
  display: block;
  color: var(--color-muted, #888);
}

.edit-actions-column {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 10px;
}

.edit-btn {
  background: transparent;
  border: none;
  font-size: 1.3rem;
  cursor: pointer;
  transition: transform 0.1s;
}

.edit-btn:hover {
  transform: scale(1.2);
}

.small-btn {
  background-color: #eee;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 4px 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s;
}

.small-btn:hover {
  background-color: #ddd;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 12px 0;
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background-color: #ccc;
  border-radius: 34px;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: #2196f3;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.btn.btn-primary.login-btn {
  width: 100%;
  font-size: 1.1rem;
  padding: 12px 0;
  background-color: var(--color-primary, #2196f3);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn.btn-primary.login-btn:hover {
  background-color: #1976d2;
}

.btn.btn-secondary {
  width: 100%;
  background-color: #ccc;
  color: #222;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  padding: 12px 0;
  cursor: pointer;
  transition: background 0.2s;
}

.btn.btn-secondary:hover {
  background-color: #bdbdbd;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: var(--bg-color, #fff);
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid var(--border-color, #eee);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-color, #333);
}

.modal-close {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: var(--text-color, #333);
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.modal-close:hover {
  background-color: var(--hover-color, #f5f5f5);
}

.modal-body {
  padding: 20px;
  line-height: 1.6;
}

.legal-section {
  margin-bottom: 24px;
}

.legal-section h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-color, #333);
}

.legal-section p {
  margin: 8px 0;
  color: var(--text-color, #555);
}

.legal-section ul {
  margin: 8px 0;
  padding-left: 20px;
}

.legal-section li {
  margin: 4px 0;
  color: var(--text-color, #555);
}
</style>
