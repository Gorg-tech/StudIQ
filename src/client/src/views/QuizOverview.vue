<template>
  <div class="quiz-overview-container">
    <div class="quiz card">
      <div class="quiz-card-content">
        <div class="quiz-card-main">
          <h2>Quiz-Übersicht</h2>
          <div class="quiz-summary">
            <div class="error-rate">
              Fehlerquote: {{ errorRate }}%
            </div>
            <div class="ranking">
              <span v-if="rankingLabel">
                Dein Rang: <span :class="'rank-badge ' + rankingClass">{{ rankingLabel }}</span>
              </span>
            </div>
            <div class="rating-section">
              <span>Bewertung:</span>
              <span
                v-for="star in 5"
                :key="star"
                class="star"
                :class="{ filled: star <= rating }"
                @click="setRating(star)"
              >&#9733;</span>
            </div>
          </div>
          <div class="button-row">
            <button class="btn btn-primary" @click="startQuiz">Quiz starten</button>
            <button class="btn btn-secondary" @click="goToLernset">Zum Lernset</button>
          </div>
        </div>
        <div class="quiz-card-penguin">
          <Penguin style="width: 80px; height: 80px;" />
        </div>
      </div>
    </div>

    <div class="history-section">
      <h3>Verlauf deiner Durchgänge</h3>
      <ul class="history-list">
        <li v-for="(entry, idx) in quizHistory" :key="entry.timestamp" class="history-item" @click="showRun(idx)">
          <div>
            <strong>{{ formatDate(entry.timestamp) }}</strong> – 
            {{ entry.correctAnswers }} / {{ entry.totalQuestions }} richtig ({{ entry.percentage }}%)
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Penguin from '@/components/Penguin.vue'

const router = useRouter()

const initialResults = [
  { question: 'Was ist 2 + 2?', userAnswer: '4', correctAnswer: '4', isCorrect: true },
  { question: 'Hauptstadt von Frankreich?', userAnswer: 'Berlin', correctAnswer: 'Paris', isCorrect: false }
]

const quizHistory = ref([
  {
    timestamp: Date.now() - 86400000 * 2,
    results: [
      { question: 'Was ist 2 + 2?', userAnswer: '3', correctAnswer: '4', isCorrect: false },
      { question: 'Hauptstadt von Frankreich?', userAnswer: 'Paris', correctAnswer: 'Paris', isCorrect: true }
    ]
  },
  {
    timestamp: Date.now() - 86400000,
    results: [
      { question: 'Was ist 2 + 2?', userAnswer: '4', correctAnswer: '4', isCorrect: true },
      { question: 'Hauptstadt von Frankreich?', userAnswer: 'Berlin', correctAnswer: 'Paris', isCorrect: false }
    ]
  },
  {
    timestamp: Date.now(),
    results: initialResults
  }
])

const currentRunIndex = ref(quizHistory.value.length - 1)
const current = computed(() => {
  const entry = quizHistory.value[currentRunIndex.value]
  const correctAnswers = entry.results.filter(r => r.isCorrect).length
  const totalQuestions = entry.results.length
  const percentage = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0
  return {
    ...entry,
    correctAnswers,
    totalQuestions,
    percentage
  }
})

const errorRate = computed(() =>
  current.value.totalQuestions > 0
    ? 100 - Math.round((current.value.correctAnswers / current.value.totalQuestions) * 100)
    : 0
)

const rankingLabel = computed(() => {
  if (errorRate.value < 30) return 'Platin'
  if (errorRate.value < 50) return 'Gold'
  if (errorRate.value < 70) return 'Silber'
  return 'Eisen'
})
const rankingClass = computed(() => {
  if (errorRate.value < 30) return 'rank-platin'
  if (errorRate.value < 50) return 'rank-gold'
  if (errorRate.value < 70) return 'rank-silber'
  return 'rank-eisen'
})

const rating = ref(0)
function setRating(star) {
  rating.value = star
}

function startQuiz() {
  router.push('/quizresultat')
}

function goToLernset() {
  router.push('/')
}

function showRun(idx) {
  currentRunIndex.value = idx
}

function formatDate(ts) {
  const d = new Date(ts)
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.quiz-overview-container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 32px;
  max-width: 800px;
  margin: 0 auto;
}

.quiz.card {
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.quiz-card-content {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
}

.quiz-card-main {
  flex: 1;
  text-align: left;
}

.quiz-card-penguin {
  margin-left: 32px;
  display: flex;
  align-items: flex-start;
}

.quiz.card h2 {
  color: var(--color-accent);
  margin-bottom: 16px;
  text-align: left;
}

.result-summary {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 8px;
}

.result-score {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-primary);
}

.result-percentage {
  font-size: 1.1rem;
  color: var(--color-muted);
}

.error-rate {
  font-size: 1.1rem;
  color: #f44336;
  margin-bottom: 8px;
}

.ranking {
  font-size: 1.1rem;
  margin-bottom: 8px;
}
.rank-badge {
  font-weight: bold;
  padding: 2px 10px;
  border-radius: 12px;
  margin-left: 8px;
}
.rank-platin {
  background: #4caf50;
  color: #fff;
}
.rank-gold {
  background: #ffd700;
  color: #222;
}
.rank-silber {
  background: #b0bec5;
  color: #222;
}
.rank-eisen {
  background: #bdbdbd;
  color: #222;
}

.rating-section {
  margin: 12px 0 10px 0;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 8px;
}
.star {
  cursor: pointer;
  font-size: 2rem;
  color: #ccc;
  transition: color 0.2s;
  user-select: none;
}
.star.filled {
  color: #ffd700;
}

.button-row {
  display: flex;
  gap: 16px;
  margin-top: 24px;
}

.btn-primary {
  padding: 12px 20px;
  font-size: 1.1rem;
  background: var(--color-accent);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 12px;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: var(--color-primary);
}

.btn-secondary {
  padding: 12px 20px;
  font-size: 1.1rem;
  background: var(--color-accent);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 12px;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: var(--color-primary);
}

.history-section {
  margin-top: 32px;
  width: 100%;
}

.history-list {
  list-style: none;
  padding: 0;
  margin: 18px 0 0 0;
  text-align: left;
}

.history-item {
  background: #f1f3f4;
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.history-item:hover {
  background: #e0e0e0;
}
</style>
