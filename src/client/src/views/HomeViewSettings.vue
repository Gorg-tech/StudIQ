<script setup>
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { ref } from 'vue'

const router = useRouter()
const themeStore = useThemeStore()

const goBack = () => {
  router.push('/')
}

// Dummy-Daten
const username = ref('DemoUser')
const email = ref('demo@example.com')
const language = ref('Deutsch')

// Darkmode umschalten
const toggleDarkmode = () => {
  themeStore.toggleTheme()
}

// Dummy-Funktionen für Buttons
const changeUsername = () => alert('✏️ Benutzername ändern (noch Dummy)')
const changeEmail = () => alert('✏️ E-Mail ändern (noch Dummy)')
const changePassword = () => alert('✏️ Passwort ändern (noch Dummy)')
const changeLanguage = () => alert('🌐 Sprache ändern (noch Dummy)')
</script>

<template>
  <div class="edit-quiz-view">
    <header class="edit-header">
      <h1>Einstellungen</h1>
    </header>

    <main class="edit-main">
      <!-- Allgemein -->
      <section class="quiz-title-section card">
        <label class="block-label">Allgemein</label>
        <div class="setting-item">
          <p>Benutzername: <b>{{ username }}</b></p>
          <button class="edit-btn" @click="changeUsername">✏️</button>
        </div>
        <div class="setting-item">
          <p>E-Mail: <b>{{ email }}</b></p>
          <button class="edit-btn" @click="changeEmail">✏️</button>
        </div>
        <div class="setting-item">
          <p>Passwort: <b>••••••••</b></p>
          <button class="edit-btn" @click="changePassword">✏️</button>
        </div>
      </section>

      <!-- Darstellung -->
      <section class="quiz-questions-section card">
        <h2 class="questions-section-title">Darstellung</h2>

        <div class="setting-item">
          <p>Dunkelmodus</p>
            <label class="switch">
              <input
                 type="checkbox"
                  :checked="themeStore.darkmode"
                  @change="toggleDarkmode"
                />
              <span class="slider"></span>
            </label>
        </div>


        <div class="setting-item">
          <p>Sprache: <b>{{ language }}</b></p>
          <button class="edit-btn" @click="changeLanguage">✏️</button>
        </div>
      </section>

      <!-- Benachrichtigungen -->
      <section class="quiz-questions-section card">
        <h2 class="questions-section-title">Benachrichtigungen</h2>
        <div style="margin-top: 10px;">
          <p>• E-Mail-Benachrichtigungen: <b>Aktiviert</b></p>
          <p>• Push-Benachrichtigungen: <b>Deaktiviert</b></p>
        </div>
      </section>

      <!-- Zurück -->
      <div class="edit-actions">
        <button class="btn btn-secondary" @click="goBack">
          Zurück
        </button>
      </div>
    </main>
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
  text-align: center;
}
.edit-header h1 {
  font-size: 2rem;
  font-weight: 700;
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
  transition: background-color 0.3s ease, color 0.3s ease;
}
.block-label {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 6px;
  display: block;
  color: var(--color-muted, #888);
}
.questions-section-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-accent);
  margin: 0;
}
.edit-actions {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  margin-top: 10px;
}

/* Buttons */
.edit-btn {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  transition: transform 0.1s;
}
.edit-btn:hover {
  transform: scale(1.2);
}

/* Switch-Stil */
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
</style>
