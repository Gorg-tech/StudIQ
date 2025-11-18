<template>
  <div class="profile">
    <!-- Header -->
    <header class="app-header">
      <div class="logo-container">
        <h1><LogoStudIQ /></h1>
        <p class="tagline">Dein Begleiter für die Prüfungsvorbereitung</p>
      </div>
      <button class="settings-btn" @click="router.push('/settings/')" aria-label="Einstellungen">
        <IconSettings />
      </button>
      
    </header>
    <div v-if="loading">Lädt...</div>
    <div v-else-if="error">Fehler: {{ error.message }}</div>
    <div v-if="!loading">
    <!-- Top Profile Section-->
    <div class="profile-top">
      <!-- Left side: Name + Leaderboard + Level Bar -->
      <div class="profile-left">
        <div class="profile-info">
          <h2>{{ user.username }}</h2>
          <p>Platz #{{ leaderboardPosition }}</p>
        </div>

        <!-- Level Circle + Bar -->
        <div class="level-bar-container">
          <div class="level-circle">{{ userLevel }}</div>
          <div class="level-bar-wrapper">
            <div class="level-bar">
              <div class="level-fill" :style="{ width: levelProgress + '%' }"></div>
            </div>
            <div class="level-percentage">{{ levelProgress }}%</div>
          </div>
        </div>
        
      </div>

      <!-- Right side: Penguin aligned to top of name -->
      <div class="profile-right">
        <div class="penguin-bubble top-aligned">
          <div class="bubble">{{ penguinSpeech }}</div>
          <Penguin :clap="streakCount >= 3" />
        </div>
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
      <div class="streak-count">Aktuelle Serie: <strong>{{ streakCount }} Tage</strong><br>Beste Serie: <strong>{{ longestStreak }} Tage</strong></div>
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

</div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSelfUserStreaks, getSelfUserStats } from '@/services/user.js'
import { store } from '@/stores/app.js'
import LogoStudIQ from '@/components/LogoStudIQ.vue'
import Penguin from '@/components/Penguin.vue'
import IconFlame from '@/components/icons/IconFlame.vue'
import IconSettings from '@/components/icons/IconSettings.vue'
import IconCode from '@/components/icons/IconCode.vue'

const router = useRouter()
const user = ref(null)

const loading = ref(true)
const error = ref(null)

const leaderboardPosition = ref(12)
const penguinSpeech = ref("Super gemacht! Weiter so 🐧")

// Level progress (hardcoded example)
const userLevel = ref(3)
const levelProgress = ref(60) // percentage filled of the current level

// Will be fetched from server
const currentWeekStreak = ref([
  { label: "Mo", learned: true },
  { label: "Di", learned: false },
  { label: "Mi", learned: false },
  { label: "Do", learned: false },
  { label: "Fr", learned: true },
  { label: "Sa", learned: true },
  { label: "So", learned: true }
])

const streakCount = ref(0)
const longestStreak = ref(0)

// Hardcoded recent quiz results
const recentQuizzes = ref([
  { title: "Analysis", date: "2025-02-20", score: 8, total: 10 },
  { title: "Programmierung", date: "2025-02-18", score: 7, total: 10 },
  { title: "BWL Grundlagen", date: "2025-02-16", score: 9, total: 10 }
])

onMounted(async () => {
  try {
    user.value = await store.getUser()
    const [stats, streaks] = await Promise.all([
      getSelfUserStats(),
      getSelfUserStreaks()
    ])

    leaderboardPosition.value = stats.rank

    streakCount.value = streaks.streak
    longestStreak.value = streaks.longest_streak
    // TODO: user_level, level_progress (only "iq_level" in backend)
    // TODO: Total users (no backend support yet)

    const days = streaks.days || []
    const today = new Date()
    const weekDays = ['So', 'Mo','Di','Mi','Do','Fr','Sa']

    // current week streak
    const currentWeek = []
    for (let i = 0; i < 7; i++) {
      const day = new Date(today)
      day.setDate(today.getDate() - (6 - i))
      const iso = day.toISOString().split('T')[0]
      currentWeek.push({
        label: weekDays[day.getDay()],
        learned: days.includes(iso)
      })
    }
    currentWeekStreak.value = currentWeek
  } catch(err) {
    error.value = `Fehler beim Laden des Profils: ${err.message}`
  } finally {
    loading.value = false
  }
  
})
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
  padding: 4px;
  padding-top: 8px;
  margin-left: auto;
  display: flex;
  align-items: center;
  color: var(--color-primary);
  transition: color 0.2s;
}
.settings-btn:hover {
  color: var(--color-accent);
}

.settings-btn svg {
  width: 2.2rem;
  height: 2.2rem;
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
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}

/* Left Side */
.profile-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

/* Right Side */
.profile-right {
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
}

/* Profile Info */
.profile-info h2 {
  margin: 0;
  font-size: 1.5rem;
}

.profile-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

/* Level Bar Container */
.level-bar-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
  width: 200px;
}

/* Smaller Circle */
.level-circle {
  width: 40px;
  height: 40px;
  font-size: 1rem;
  border-radius: 50%;
  background-color: var(--color-primary);
  color: #fff;
  font-weight: 600;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
}

/* Smaller Bar */
.level-bar {
  flex: 1;
  height: 10px;
  background-color: #eee;
  border-radius: 8px;
  overflow: hidden;
  min-width:100px;
}

.level-fill {
  height: 100%;
  width: 60%;
  background-color: var(--color-accent);
  border-radius: 8px 0 0 8px;
  transition: width 0.5s ease;
}

.level-percentage {
  font-size: 0.85rem;
  font-weight: 500;
  color: #666;
  white-space: nowrap;
}

.penguin-bubble {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.streak-card {
  background: var(--card-bg);
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
  background-color: var(--card-bg);
  border-radius: 10px;
  padding: 16px;
  min-width: 180px;
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quiz-suggestion-item:hover {
  background-color: color-mix(in oklab, var(--card-bg) 80%, #888 20%);
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
