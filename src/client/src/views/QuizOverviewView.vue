<template>
  <div class="quiz-overview-container">
    <!-- Main Quiz Card -->
    <div class="card quiz-card">
      <div class="quiz-header">
        <h2>{{ quiz.title }}</h2>
      </div>
      <div class="quiz-content">
        <div class="quiz-info">
          <p class="quiz-description">{{ quiz.description }}</p>
          <div class="quiz-meta-grid">
            <div class="meta-item">
              <span>Erstellt am: {{ formatDate(quiz.created_at) }}</span>
            </div>
            <div class="meta-item">
              <span>von: {{ quiz.created_by }}</span>
            </div>
            <div class="meta-item">
              <span>Fragen: {{ quiz.questions.length }}</span>
            </div>
            <div class="meta-item">
              <span>Ø Zeit: {{ quiz.avg_time_spent || '-' }}s</span>
            </div>
            <div class="meta-item">
              <span>Lernset: {{ quiz.lernset?.title || '-' }}</span>
            </div>
          </div>
          <div class="button-row">
            <button class="btn btn-primary" @click="startQuiz">
              Quiz starten
            </button>
            <button class="btn" @click="goToLernset">
              Zum Lernset
            </button>
            <button class="btn" @click="showStats = true">
              Statistiken
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistik-Popup -->
    <div v-if="showStats" class="modal-overlay" @click.self="showStats = false">
      <div class="modal-content">
        <h3>Statistiken</h3>
        <div class="stats-row">
          <div class="stat-square error-rate">
            <div class="stat-label">Fehlerquote</div>
            <div class="stat-value">{{ errorRate }}%</div>
          </div>
          <div class="stat-square correct-rate">
            <div class="stat-label">Korrekte Antworten</div>
            <div class="stat-value">{{ 100 - errorRate }}%</div>
          </div>
        </div>
        <div class="stats-row">
          <div class="stat-square attempts">
            <div class="stat-label">Versuche</div>
            <div class="stat-value">{{ quizHistory.length }}</div>
          </div>
        </div>
        <button class="btn btn-secondary" @click="showStats = false" style="margin-top: 24px;">Schließen</button>
      </div>
    </div>

    <!-- History Section -->
    <div class="card history-section">
      <h3>Verlauf deiner Durchgänge</h3>
      <div class="history-list">
        <div v-for="(entry, idx) in quizHistory" 
             :key="entry.timestamp" 
             class="history-item" 
             @click="showRun(idx)"
             :class="{ active: idx === currentRunIndex }">
          <div class="history-date">
            <span>{{ formatDate(entry.timestamp) }}</span>
          </div>
          <div class="history-result">
            <span class="result-score">{{ entry.correctAnswers }} / {{ entry.totalQuestions }}</span>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: entry.percentage + '%' }"></div>
            </div>
            <span class="percentage">{{ entry.percentage }}%</span>
          </div>
        </div>
        <div class="no-history" v-if="quizHistory.length === 0">
          <p>Du hast dieses Quiz noch nicht absolviert. Starte jetzt deinen ersten Durchgang!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const showStats = ref(false)

// Dummy quiz data, replace with API call
const quiz = ref({
  title: 'Beispielquiz',
  description: 'Dies ist ein Beispiel für ein Quiz.',
  created_at: '2024-06-24T12:00:00Z',
  created_by: 'Max Mustermann',
  rating_score: 18,
  rating_count: 5,
  avg_time_spent: 42,
  lernset: { title: 'Mathematik Grundlagen' },
  questions: [
    { id: 1, text: 'Was ist 2 + 2?' },
    { id: 2, text: 'Hauptstadt von Frankreich?' }
  ]
})

const router = useRouter()

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

function startQuiz() {
  router.push('/quiz')
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
  gap: 24px;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 16px;
}

.card {
  background-color: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
  width: 100%;
}

.quiz-header {
  margin-bottom: 16px;
}

.quiz-header h2 {
  color: var(--color-accent);
  margin: 0;
  font-size: 1.8rem;
}

.quiz-description {
  font-size: 1.1rem;
  color: var(--color-text);
  margin-bottom: 20px;
  line-height: 1.5;
}

.quiz-meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 16px;
}

.meta-item {
  font-size: 0.95rem;
  color: var(--color-muted);
}

.button-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.stats-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.stat-square {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-width: 100px;
}

.error-rate {
  background-color: #ffebee;
}

.correct-rate {
  background-color: #e8f5e9;
}

.attempts {
  background-color: #e3f2fd;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--color-muted);
  margin-bottom: 4px;
}

.stat-value {
  font-size: 1.6rem;
  font-weight: bold;
  color: var(--color-text);
}

.history-section h3 {
  color: var(--color-accent);
  margin-bottom: 16px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background-color: #f9f9f9;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.history-item:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
}

.history-item.active {
  background-color: #e3f2fd;
  border: 1px solid #bbdefb;
}

.history-date {
  font-size: 0.9rem;
  color: var(--color-muted);
}

.history-result {
  display: flex;
  align-items: center;
  gap: 12px;
}

.result-score {
  font-weight: 500;
  color: var(--color-text);
}

.progress-bar {
  width: 100px;
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--color-primary);
}

.percentage {
  font-weight: 500;
  color: var(--color-primary);
  min-width: 48px;
  text-align: right;
}

.no-history {
  text-align: center;
  padding: 24px;
  color: var(--color-muted);
  background-color: #f9f9f9;
  border-radius: 12px;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  backdrop-filter: blur(2px);
}

.modal-content {
  background: #fff;
  border-radius: 16px;
  padding: 32px 24px;
  min-width: 320px;
  max-width: 90vw;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.modal-content h3 {
  color: var(--color-accent);
  margin-bottom: 24px;
  font-size: 1.4rem;
  text-align: center;
}

/* Responsive styles */
@media (max-width: 768px) {
  .stats-row {
    flex-wrap: wrap;
    justify-content: space-between;
  }
  
  .stat-square {
    flex: 0 0 calc(50% - 8px);
    margin-bottom: 16px;
  }
  
  .button-row {
    flex-direction: column;
    width: 100%;
  }
  
  .button-row .btn {
    width: 100%;
    margin-bottom: 8px;
  }
}

@media (max-width: 600px) {
  .quiz-meta-grid {
    grid-template-columns: 1fr;
  }
  
  .history-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .history-result {
    width: 100%;
  }
  
  .modal-content {
    padding: 24px 16px;
  }
}

@media (min-width: 1024px) {
  .quiz-overview-container {
    padding: 0;
  }
  
  .card {
    padding: 32px;
  }
}
</style>
