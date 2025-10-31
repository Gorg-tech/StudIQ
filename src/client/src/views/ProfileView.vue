

<template>
  <div class="profile">
    <!-- Header -->
    <header class="app-header">
      <div class="logo-container">
        <h1><LogoStudIQ /></h1>
        <p class="tagline">Dein Begleiter für die Prüfungsvorbereitung</p>
      </div>
      <button class="settings-btn" @click="showMenu = !showMenu">
        <IconSettings />
      </button>
      <div v-if="showMenu" class="settings-popup">
        <button class="logout-btn" @click="handleLogout">Ausloggen</button>
      </div>
    </header>

    <!-- Top Profile Section: Penguin + Leaderboard -->
    <div class="profile-top">
      <div class="profile-info">
        <h2>{{ store.user.name }}</h2>
        <p>Platz: {{ leaderboardPosition }}/{{ totalUsers }}</p>
      </div>
      <div class="penguin-bubble">
        <div class="bubble">{{ penguinSpeech }}</div>
        <Penguin class="penguin" :class="{ clap: streakCount > 3 }" />
      </div>
    </div>

    <!-- Streak Calendar Full Width -->
    <div class="streak-card full-width">
      <div class="week-row">
        <div class="day-box" v-for="(day, index) in currentWeekStreak" :key="index">
          <IconFlame v-if="day.learned" />
          <IconFlame v-else class="inactive" />
          <div class="day-label">{{ day.label }}</div>
        </div>
      </div>
      <div class="streak-count">Aktuelle Serie: <strong>{{ streakCount }} Tage</strong></div>
    </div>

    <!-- Recent Quizzes Section (Home-style cards) -->
    <div class="suggested-quizzes">
      <h3>Zuletzt bearbeitete Quizze</h3>
      <div class="quiz-suggestions-row">
        <div
          v-for="(quiz, index) in recentQuizzes"
          :key="index"
          class="quiz-suggestion-item"
        >
          <div class="quiz-suggestion-icon" :style="{ backgroundColor: '#2196f3' + '1A' }">
            <IconCode /> <!-- can change based on type if needed -->
          </div>
          <div class="quiz-suggestion-content">
            <h4>{{ quiz.title }}</h4>
            <p class="quiz-meta">{{ quiz.score }}/{{ quiz.total }} - {{ quiz.date }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import LogoStudIQ from '@/components/LogoStudIQ.vue'
import Penguin from '@/components/Penguin.vue'
import IconFlame from '@/components/icons/IconFlame.vue'
import IconSettings from '@/components/icons/IconSettings.vue'
import IconCode from '@/components/icons/IconCode.vue'

// Hardcoded user
const store = {
  user: { name: "Max Mustermann" }
}

const router = useRouter()
const showMenu = ref(false)

const leaderboardPosition = ref(12)
const totalUsers = ref(20)
const penguinSpeech = ref("Super gemacht! Weiter so 🐧")

const currentWeekStreak = ref([
  { label: "Mo", learned: true },
  { label: "Di", learned: true },
  { label: "Mi", learned: true },
  { label: "Do", learned: false },
  { label: "Fr", learned: true },
  { label: "Sa", learned: true },
  { label: "So", learned: false }
])

const streakCount = computed(() => {
  let count = 0
  for (let i = currentWeekStreak.value.length - 1; i >= 0; i--) {
    if (currentWeekStreak.value[i].learned) count++
    else break
  }
  return count
})

// Hardcoded recent quiz results
const recentQuizzes = ref([
  { title: "Analysis", date: "2025-02-20", score: 8, total: 10 },
  { title: "Programmierung", date: "2025-02-18", score: 7, total: 10 },
  { title: "BWL Grundlagen", date: "2025-02-16", score: 9, total: 10 }
])

function handleLogout() {
  router.push("/login")
}
</script>

<style scoped>
/* Keep your original profile styles for header, penguin, streak, etc. */
.profile {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 800px;
  margin: 0 auto;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.settings-btn {
  background: none;
  border: none;
  cursor: pointer;
}

.settings-popup {
  position: absolute;
  top: 40px;
  right: 0;
  background: #fff;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(34,34,34,0.1);
}

.profile-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.penguin-bubble {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.penguin.clap {
  animation: clap 0.6s infinite;
}

@keyframes clap {
  0%,100% { transform: rotate(0deg) }
  25% { transform: rotate(15deg) }
  50% { transform: rotate(0deg) }
  75% { transform: rotate(-15deg) }
}

.streak-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(34,34,34,0.08);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.streak-card.full-width {
  width: 100%;
}

.week-row {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 8px;
  margin-bottom: 8px;
}

.day-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.day-label {
  font-size: 0.75rem;
  color: #888;
}

.inactive {
  opacity: 0.25;
  filter: grayscale(1);
}

.streak-count {
  font-weight: 500;
  margin-top: 8px;
  text-align: center;
}

/* Suggested quizzes layout (bottom section) */
.suggested-quizzes {
  margin-top: 24px;
}

.suggested-quizzes h3 {
  margin-bottom: 16px;
  color: var(--color-accent);
}

.quiz-suggestions-row {
  display: flex;
  flex-direction: row;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.quiz-suggestion-item {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 16px;
  min-width: 180px;
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid #eee;
}

.quiz-suggestion-item:hover {
  background-color: #f5f5f5;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.quiz-suggestion-icon {
  color: var(--color-primary);
  background-color: rgba(33, 150, 243, 0.1);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
}

.quiz-suggestion-content h4 {
  margin: 0 0 4px 0;
  font-size: 1rem;
  color: var(--color-text);
}

.quiz-meta {
  margin: 0;
  font-size: 0.8rem;
  color: var(--color-muted);
}
</style>
