<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import IconSettings from '@/components/icons/IconSettings.vue'
import LogoStudIQ from '@/components/LogoStudIQ.vue'
import Penguin from '@/components/Penguin.vue' 
import IconFlame from '@/components/icons/IconFlame.vue'
import IconLeaderboard from '@/components/icons/IconLeaderboard.vue'
import IconSearch from '@/components/icons/IconSearch.vue'
import IconTimer from '@/components/icons/IconTimer.vue'
import IconCode from '@/components/icons/IconCode.vue'
import IconChart from '@/components/icons/IconChart.vue'
import { fetchUserStats } from '@/services/leaderboard'


const startQuiz = () => {
  // TODO: Implement quiz start functionality
  console.log('Starting quiz');
}
const openSettings = () => {
  // TODO: Implement settings navigation
  alert('Einstellungen öffnen');
}

const router = useRouter()
const userStats = ref({
  streak: 0,
  rank: null
})

onMounted(async () => {
  try {
    const stats = await fetchUserStats()
    userStats.value = stats
  } catch (error) {
    console.error('Fehler beim Laden der User-Statistiken:', error)
  }
})

// Calculate days until exam period
const examPeriodStart = new Date('2026-02-01');
const daysUntilExams = computed(() => {
  const today = new Date();
  const diffTime = examPeriodStart - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
})

// Sample data for suggested quizzes
const suggestedQuizzes = ref([
  { id: 1, title: 'Laufzeitberechnung', questions: 10, duration: 5, iconColor: '#ff9800', iconType: 'timer' },
  { id: 2, title: 'Analysis', questions: 15, duration: 7, iconColor: '#4caf50', iconType: 'chart' },
  { id: 3, title: 'C - Programmierung', questions: 33, duration: 13, iconColor: '#2196f3', iconType: 'code' },
]);
</script>

<template>
  <div class="home">
    <header class="app-header">
      <div class="logo-container">
        <h1>
          <LogoStudIQ />
        </h1>
        <p class="tagline">Dein Begleiter für die Prüfungsvorbereitung</p>
      </div>
      <button class="settings-btn" @click="router.push('/settings/')" aria-label="Einstellungen">
        <IconSettings />
      </button>
    </header>

    <section class="main-content">
      <div class="card welcome-card">
        <h2>Willkommen zurück!</h2>
        <p>Lerne und verbessere dein Wissen mit interaktiven Quizzen.</p>
        <div class="exam-countdown">
          <p>Nur noch <span class="days-count">{{ daysUntilExams }}</span> Tage bis zum Prüfungszeitraum!</p>
        </div>
      </div>
      <section class="stats-section">
        <div class="stats-row desktop-row">
          <!-- Streak -->
          <div class="stat-square">
            <span class="stat-icon flame">
              <IconFlame />
            </span>
            <div class="stat-label-big">Streak</div>
            <div class="stat-value-big">{{ userStats.streak }}</div>
          </div>
          
          <!-- Platz (Leaderboard) -->
          <div class="stat-square">
            <span class="stat-icon leaderboard">
              <IconLeaderboard />
            </span>
            <div class="stat-label-big">Platz</div>
            <div class="stat-value-big leaderboard-rank">
              <span class="rank-number">{{ userStats.rank || '-' }}</span>
            </div>
          </div>
          
          <!-- Weekly Goal -->
          <div class="stat-square">
            <span class="stat-icon goal">
              <IconTimer color="#ff9800" />
            </span>
            <div class="stat-label-big">Weekly Goal</div>
            <div class="stat-value-big">4/7</div>
          </div>
          
          <!-- Penguin -->
          <div class="penguin-bubble">
            <div class="bubble">
              <span>Mach ein Quiz - sonst kommt der Pinguin! 🐧</span>
            </div>
            <Penguin class="penguin" />
          </div>
        </div>
        
        <!-- Mobile layout rows -->
        <div class="stats-row mobile-row top-row">
          <div class="stat-square">
            <span class="stat-icon flame">
              <IconFlame />
            </span>
            <div class="stat-label-big">Streak</div>
            <div class="stat-value-big">5</div>
          </div>
          <div class="penguin-bubble">
            <div class="bubble">
              <span>Mach ein Quiz - sonst kommt der Pinguin! 🐧</span>
            </div>
            <Penguin class="penguin" />
          </div>
        </div>
        
        <div class="stats-row mobile-row bottom-row">
          <div class="stat-square">
            <span class="stat-icon leaderboard">
              <IconLeaderboard />
            </span>
            <div class="stat-label-big">Platz</div>
            <div class="stat-value-big leaderboard-rank">
              <span class="rank-number">12</span>
            </div>
          </div>
          <div class="stat-square">
            <span class="stat-icon goal">
              <!-- Goal SVG -->
              <svg
                viewBox="0 0 24 24"
                width="36"
                height="36"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <circle cx="12" cy="12" r="10" stroke="#ff9800" fill="#fff3e0" />
                <path
                  d="M12 6v6l4 2"
                  stroke="#ff9800"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </span>
            <div class="stat-label-big">Weekly Goal</div>
            <div class="stat-value-big">4/7</div>
          </div>
        </div>
      </section>
      <div class="quiz-options">
        <button class="btn btn-primary" @click="router.push('/search')">
          <IconSearch />
          <span>Quiz suchen</span>
        </button>
      </div>

      <!-- Suggested Quizzes Section -->
      <div class="suggested-quizzes">
        <h3>Vorgeschlagene Quizze</h3>
        <div class="quiz-suggestions-row">
          <div
            v-for="(quiz, index) in suggestedQuizzes"
            :key="index"
            class="quiz-suggestion-item"
            @click="router.push('/quiz')"
          >
            <div class="quiz-suggestion-icon" :style="{ backgroundColor: quiz.iconColor + '1A' }">
              <!-- Different icon based on quiz type -->
              <IconTimer v-if="quiz.iconType === 'timer'" :color="quiz.iconColor" />
              <IconChart v-else-if="quiz.iconType === 'chart'" :color="quiz.iconColor" />
              <IconCode v-else-if="quiz.iconType === 'code'" :color="quiz.iconColor" />
            </div>
            <div class="quiz-suggestion-content">
              <h4>{{ quiz.title }}</h4>
              <p class="quiz-meta">{{ quiz.questions }} Fragen - {{ quiz.duration }} Min</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
  min-height: 100vh;
}

.app-header {
  margin-bottom: 20px;
  text-align: left;
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  z-index: 1;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.home .app-header h1 {
  font-size: 2rem;
  margin-bottom: 4px;
  font-weight: 500;
}

.tagline {
  color: var(--color-muted);
  font-size: 0.9rem;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
  z-index: 1;
}

.card {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
}

.welcome-card {
  text-align: center;
}

.welcome-card h2 {
  margin-bottom: 12px;
  color: var(--color-accent);
}

.welcome-card p {
  color: var(--color-muted);
}

.exam-countdown {
  margin-top: 12px;
  font-weight: 500;
}

.exam-countdown p {
  color: var(--color-accent);
}

.days-count {
  font-weight: 700;
  font-size: 1.1em;
}

.stats-card h3 {
  margin-bottom: 16px;
  color: var(--color-accent);
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--color-primary);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--color-muted);
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

.stats-section {
  margin-bottom: 24px;
}

.stats-row {
  display: flex;
  align-items: stretch;
  gap: 18px;
  margin-bottom: 18px;
}

.stats-row:last-child {
  margin-bottom: 0;
}

.top-row {
  flex-direction: row;
  justify-content: space-between;
}

.bottom-row {
  flex-direction: row;
  justify-content: space-between;
}

.stat-square {
  background: var(--card-bg);
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
  flex: 1 1 0;
  min-width: 90px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 18px 8px 12px 8px;
  justify-content: center;
  text-align: center;
  cursor: pointer; 
}

.stat-icon {
  margin-bottom: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.stat-icon svg {
  width: 52px;
  height: 52px;
}

.stat-label-big {
  font-size: 1.05rem;
  color: var(--color-muted);
  margin-bottom: 2px;
}

.stat-value-big {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--color-primary);
}

.leaderboard-rank {
  color: var(--color-accent);
  font-size: 2rem;
  font-weight: 900;
  letter-spacing: 0.01em;
}

.penguin-bubble {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  min-width: 90px;
  margin-left: 10px;
  position: relative;
}

.bubble {
  background: var(--card-bg);
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
  padding: 6px 14px;
  font-size: 0.95rem;
  color: var(--color-accent);
  margin-bottom: 4px;
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
  z-index: 2;
}

.penguin {
  display: block;
  margin-top: 8px;
  width: 196px;
  height: auto;
  overflow: visible;  
}

/* Suggested Quizzes Styles */
.suggested-quizzes {
  margin-top: 10px;
}

.suggested-quizzes h3 {
  margin-bottom: 16px;
  color: var(--color-accent);
}

.quiz-suggestions-row {
  display: flex;
  flex-direction: row;
  gap: 16px;
  padding-bottom: 10px;
}

.quiz-suggestion-item {
  background-color: var(--color-bg-light);
  border-radius: 10px;
  padding: 16px;
  min-width: 180px;
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid var(--color-border);
}

.quiz-suggestion-item:hover {
  background-color: var(--color-bg-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.quiz-suggestion-icon {
  color: var(--color-primary);
  background-color: rgba(255, 152, 0, 0.1);
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

/* Mobile responsiveness */
@media (max-width: 600px) {
  .quiz-suggestions-row {
    flex-direction: column;
    gap: 10px;
  }
  
  .quiz-suggestion-item {
    min-width: auto;
    width: 100%;
  }
}

@media (min-width: 768px) {
  .quiz-options {
    flex-direction: row;
  }
  .quiz-button {
    flex: 1;
  }
}

/* Desktop adjustments */
@media (min-width: 1024px) {
  .home {
    max-width: 800px;
    margin: 0 auto;
  }
  .app-header h1 {
    font-size: 3rem;
  }
  .app-header {
    width: 100%;
  }
  .main-content {
    gap: 30px;
  }
  .card {
    padding: 30px;
  }
}

/* Mobile styles */
@media (max-width: 600px) {
  .stats-row {
    gap: 10px;
    margin-bottom: 10px;
  }
  
  .stats-row.top-row, .stats-row.bottom-row {
    flex-direction: row;
  }
  
  .stats-row .stat-square,
  .stats-row .penguin-bubble {
    flex: 1;
  }
  
  .penguin-bubble {
    margin-left: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
  }
  
  .bubble {
    position: static;
    transform: none;
    margin-bottom: 8px;
    font-size: 0.85rem;
    padding: 4px 10px;
    text-align: center;
    white-space: normal;
    width: 100%;
  }
  
  .penguin {
    width: 120px;
    height: 120px;
  }
}

/* For desktop, ensure the original layout is maintained */
@media (min-width: 601px) {
  .stats-section {
    display: flex;
    flex-direction: column;
  }
  
  .stats-row.top-row, .stats-row.bottom-row {
    flex-direction: row;
  }
  
  .stats-section .stats-row:first-child {
    margin-bottom: 0;
  }
  
  .stats-section .stats-row:last-child {
    display: none;
  }
  
  .stats-section .stats-row.top-row {
    margin-bottom: 0;
  }
  
  .stats-section .top-row .penguin-bubble {
    order: 3;
  }
  
  .stats-section .top-row .stat-square:nth-child(2),
  .stats-section .top-row .stat-square:nth-child(3) {
    display: inline-flex;
  }
}

/* Desktop/mobile layout control */
.desktop-row {
  display: none;
}

.mobile-row {
  display: flex;
}

@media (min-width: 601px) {
  .desktop-row {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 0;
  }
  
  .mobile-row {
    display: none;
  }
}

.quiz-options {
  width: 100%;
  display: flex;
  margin-bottom: 20px;
}

.quiz-options .btn {
  width: 100%;
  justify-content: center;
}

.quiz-options .btn-primary {
  padding: 14px 20px;
  font-size: 1.1rem;
}

.quiz-options .btn-icon svg {
  width: 22px;
  height: 22px;
}
</style>
