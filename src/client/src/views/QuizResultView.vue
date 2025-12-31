<template>
  <div v-if="loading">Lädt...</div>
  <div v-else-if="error" class="error">Fehler: {{ error.message }}</div>
  <div v-if="!loading && !error">
    <div class="result-card card">
      <h2>Dein Ergebnis</h2>
      <div class="iq-bar-container">
        <div class="iq-level-label">
          <span>IQ-Level</span>
          <span class="level-info">({{ level_info }})</span>
          <div class="iq-level-values">
            <span class="iq-prev">{{ iq_prev }}</span>
            <span class="iq-arrow">→</span>
            <span class="iq-new">{{ getIQPoints(iq_new) + (iq_new > getMaxPerPointsLevel() ? getMaxPerPointsLevel() : 0)}}</span>
          </div>
        </div>
        <div class="iq-attempt-info">
          <span class="iq-attempt-text">(Das ist dein {{ attempts }}. Versuch)</span>
        </div>
        <div class="iq-bar">
          <div class="iq-segment iq-old" :style="{ width: iqOldWidth + '%'}" title="Bisheriger IQ-Score"></div>
          <div class="iq-segment iq-base" :style="{ width: iqBaseWidth + iqOldWidth + '%'}" title="Punkte für das Quiz"></div>
          <div
            v-if="iq_perfect > 0"
            class="iq-segment iq-perfect"
            :style="{ width: iqOldWidth + iqBaseWidth + iqPerfectWidth + '%'}"
            title="Perfect-Score-Bonus"
          ></div>
          <div class="iq-segment iq-streak" :style="{ width: iqOldWidth + iqBaseWidth + iqPerfectWidth + iqStreakWidth + '%'}" title="Streak-Bonus"></div>
        </div>
        <div class="iq-bar-scale">
          <span>0</span>
          <span>{{ getMaxPerPointsLevel() }}</span>
        </div>
        <div class="iq-bar-labels">
          <transition name="fade"><div v-if="showOldLabel" class="iq-label iq-old-label"> {{ iq_prev }} Punkte vor dem Quiz</div></transition>
          <transition name="fade"><div v-if="showBaseLabel" class="iq-label iq-base-label">+ {{ iq_base }} Punkte - Lösen des Quizzes</div></transition>
          <transition name="fade"><div v-if="showStreakLabel" class="iq-label iq-streak-label">+ {{ iq_streak }} Punkte - {{ streak }}er Streak-Bonus</div></transition>
          <transition name="fade"><div v-if="showPerfectLabel && iq_perfect > 0" class="iq-label iq-perfect-label">+ {{ iq_perfect }} Punkte - Perfekt-Bonus</div></transition>
        </div>
      </div>
      <div class="iq-total">
        Gesamt: <span class="iq-total-value">+{{ iq_total }} Punkte</span>
      </div>
      <div class="result-summary">
        <div class="result-score">{{ correctAnswers }} / {{ totalQuestions }} richtig</div>
        <div class="result-percentage">({{ percentage }}%)</div>
      </div>
      <ul class="result-list">
        <li v-for="(result, idx) in results" :key="idx" class="result-item">
          <div class="question">{{ result.question }}</div>
          <div class="answers">
            <span :class="['user-answer', result.isCorrect ? 'correct' : 'incorrect']">
              Deine Antwort: {{ result.selected }}
            </span>
            <span v-if="!result.isCorrect" class="correct-answer">
              (Richtig: {{ result.correct }})
            </span>
          </div>
        </li>
      </ul>
      <div class="button-row">
        <button class="btn btn-primary" @click="restartQuiz">Quiz erneut starten</button>
        <button class="btn btn-secondary" @click="goToOverview">Zur Quiz Übersicht</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const iqOldWidth = ref(0)
const showOldLabel = ref(false)
const showBaseLabel = ref(false)
const showPerfectLabel = ref(false)
const showStreakLabel = ref(false)
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { completeQuiz } from '@/services/quizzes'
import { getMaxPerPointsLevel, getIQLevel, getIQPoints } from '@/services/iq'

const router = useRouter()
const route = useRoute()

const loading = ref(true)
const error = ref(null)

const results = ref([])
const quizId = ref(route.query.quizId)

const correctAnswers = ref(0)
const totalQuestions = ref(0)
const percentage = computed(() =>
  totalQuestions.value > 0
    ? Math.round((correctAnswers.value / totalQuestions.value) * 100)
    : 0
)


const iq_score = ref(0)
const iq_base = ref(0)
const iq_perfect = ref(0)
const iq_streak = ref(0)
const iq_total = ref(0)
const iq_prev = ref(0)
const iq_new = ref(0)
const level_info = ref(null)

const attempts = ref(1)
const streak = ref(0)

const iqBaseWidth = ref(0)
const iqPerfectWidth = ref(0)
const iqStreakWidth = ref(0)

/**
 * Animates the IQ bar segments sequentially.
 */
function animateBar() {

  iqOldWidth.value = 0
  iqBaseWidth.value = 0
  iqPerfectWidth.value = 0
  iqStreakWidth.value = 0
  showOldLabel.value = false
  showBaseLabel.value = false
  showPerfectLabel.value = false
  showStreakLabel.value = false

  // Calculate widths
  const oldW = iq_prev.value
  const baseW = iq_base.value
  const perfectW = iq_perfect.value
  const streakW = iq_streak.value

  const toPercent = 100 / getMaxPerPointsLevel()

  setTimeout(() => {
    iqOldWidth.value = oldW * toPercent
    showOldLabel.value = true
    setTimeout(() => {
      iqBaseWidth.value = baseW * toPercent
      showBaseLabel.value = true
      setTimeout(() => {
        iqStreakWidth.value = streakW * toPercent
        showStreakLabel.value = true
        setTimeout(() => {
          iqPerfectWidth.value = perfectW * toPercent
          showPerfectLabel.value = true
        }, 400)
      }, 400)
    }, 400)
  }, 400)
}

/**
 * Loads quiz results from local storage and notifies the server of quiz completion.
 */
onMounted(async () => {
  const stored = localStorage.getItem('quizResults')
  if (stored) {
    results.value = JSON.parse(stored)
  }
  
  // Notify server of quiz completion
  if (quizId.value) {
    try {
      const iq_calc = await completeQuiz(quizId.value)
      iq_base.value = iq_calc.base_points || 0
      iq_perfect.value = iq_calc.perfect_bonus_points || 0
      iq_streak.value = iq_calc.streak_bonus_points || 0
      iq_total.value = iq_base.value + iq_perfect.value + iq_streak.value
      iq_prev.value = getIQPoints(iq_calc.prev_iq || 0)
      iq_new.value = iq_prev.value + iq_total.value
      iq_score.value = Math.floor(iq_new.value / 100)
      attempts.value = iq_calc.attempts || 1
      streak.value = iq_calc.streak || 0
      correctAnswers.value = iq_calc.correct_answers || 0
      totalQuestions.value = iq_calc.total_answers || 0

      level_info.value = "Level " + getIQLevel(iq_calc.prev_iq || 0);
        if(iq_new.value > getMaxPerPointsLevel()) {
          level_info.value += " +1"
      }

      animateBar()
    } catch (err) {
      error.value = err
    }
  } else {
    error.value = new Error('Keine Quiz-ID angegeben')
  }
  
  loading.value = false
})


/**
 * Restarts the quiz by clearing stored results and navigating to the quiz view.
 */
function restartQuiz() {
  localStorage.removeItem('quizResults')
  router.push({
    name: 'quiz',
    params: { quizId: quizId.value }
  })
}

/**
 * Navigates to the quiz overview page or home if no quiz ID is available.
 */
function goToOverview() {
  if (!quizId.value) {
    console.error('No quiz ID available')
    router.push('/') // Fallback to home
    return
  }
  
  router.push({ 
    name: 'quiz-overview', 
    params: { quizId: quizId.value }
  })
}
</script>

<style scoped>
.iq-bar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 32px;
}
.iq-level-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 8px;
}
.iq-level-value {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--color-primary);
}
.iq-bar {
  display: flex;
  width: 420px;
  height: 38px;
  background: var(--color-bg-light);
  border: var(--color-border) 2px solid;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 1px 6px rgba(34,34,34,0.08);
  position: relative;
  border: 2px solid var(--color-bg-light);
}
.iq-segment {
  border-radius: 18px;
}

.iq-bar-labels {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  margin-top: 10px;
  min-height: 80px;
}
.iq-label {
  font-size: 1.08rem;
  font-weight: 600;
  padding: 0px 10px;
  border-radius: 8px;
  margin-bottom: 0px;
  animation: popIn 0.5s;
}
.iq-attempt-text {
  font-size: 0.95rem;
  font-style: italic;
  color: var(--color-muted);
  margin-bottom: 8px;
}
.iq-old-label { color: var(--color-primary); background: var(--color-bg-light); }
.iq-base-label { color: var(--color-secondary); background: var(--color-bg-light); }
.iq-streak-label { color: color-mix(in oklab, var(--color-secondary) 66%, #ffffff 33%); background: var(--color-bg-light); }
.iq-perfect-label { color: color-mix(in oklab, var(--color-secondary) 33%, #ffffff 66%); background: var(--color-bg-light); }
@keyframes popIn {
  0% { opacity: 0; transform: translateY(10px) scale(0.95); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.iq-segment {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0;
  transition: width 0.6s cubic-bezier(.4,1.4,.6,1), left 0.6s cubic-bezier(.4,1.4,.6,1), box-shadow 0.2s;
}
.iq-segment:hover {
  filter: brightness(1.2);
}
.iq-old {
  background: var(--color-primary);
  z-index: 4;
}
.iq-base {
  background: var(--color-secondary);
  z-index: 3;
}
.iq-streak {
  background: color-mix(in oklab, var(--color-secondary) 66%, #ffffff 33%);
  z-index: 2;
}
.iq-perfect {
  background: color-mix(in oklab, var(--color-secondary) 33%, #ffffff 66%);
  z-index: 1;
}
.iq-segment-label {
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  text-shadow: 0 1px 4px rgba(0,0,0,0.18);
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.iq-bar-scale {
  display: flex;
  justify-content: space-between;
  width: 420px;
  font-size: 0.95rem;
  color: var(--color-muted);
  margin-top: 4px;
}
.iq-total {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 8px;
}
.iq-total-value {
  font-size: 1.7rem;
  color: var(--color-accent);
}
.iq-prev-next {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 1.1rem;
  margin-bottom: 18px;
}
.iq-prev, .iq-new {
  font-weight: 600;
  color: var(--color-primary);
}
.iq-arrow {
  font-size: 1.3rem;
  color: var(--color-muted);
  padding: 0 10px;
}
.result-card {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px var(--card-shadow);
  margin: 0 auto;
  max-width: 600px;
  text-align: center;
}

.result-card h2 {
  color: var(--color-accent);
  margin-bottom: 16px;
}

.result-summary {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 18px;
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

.result-list {
  list-style: none;
  padding: 0;
  margin: 24px 0;
  text-align: left;
}

.result-item {
  background: var(--color-bg-light);
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 12px;
  box-shadow: 0 1px 4px rgba(34, 34, 34, 0.04);
}

.question {
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--color-text);
}

.answers {
  font-size: 0.98rem;
}

.user-answer.correct {
  color: var(--color-green);
  font-weight: 600;
}

.user-answer.incorrect {
  color: var(--color-red);
  font-weight: 600;
}

.correct-answer {
  color: var(--color-secondary);
  margin-left: 12px;
}

.button-row {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 24px;
}

.level-info {
  font-size: 0.8rem;
  color: var(--color-muted)
}

.error {
  color: var(--color-red);
  font-weight: 600;
  font-size: 1.5rem;
  text-align: center;
  margin-top: 20px;
}
</style>
