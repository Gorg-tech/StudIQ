<template>
  <div v-if="loading">Lädt...</div>
  <div v-else-if="error">Fehler: {{ error.message }}</div>
  <div v-if="!loading">
    <div class="result-card card">
      <h2>Dein Ergebnis</h2>
      <div class="iq-bar-container">
        <div class="iq-level-label">
          <span>IQ-Level</span>
          <div class="iq-level-value">{{ iq_level }}</div>
        </div>
        <div class="iq-bar">
          <div class="iq-segment iq-old" :style="{ width: iqOldWidth + '%', left: '0%' }" title="Bisheriger IQ-Level"></div>
          <div class="iq-segment iq-base" :style="{ width: iqBaseWidth + '%', left: iqOldWidth + '%' }" title="Punkte für das Quiz" @mouseenter="hoverSegment('base')" @mouseleave="hoverSegment('')"></div>
          <div class="iq-segment iq-perfect" :style="{ width: iqPerfectWidth + '%', left: (iqOldWidth + iqBaseWidth) + '%' }" title="Perfect-Score-Bonus" @mouseenter="hoverSegment('perfect')" @mouseleave="hoverSegment('')"></div>
          <div class="iq-segment iq-streak" :style="{ width: iqStreakWidth + '%', left: (iqOldWidth + iqBaseWidth + iqPerfectWidth) + '%' }" title="Streak-Bonus" @mouseenter="hoverSegment('streak')" @mouseleave="hoverSegment('')"></div>
          <div class="iq-segment iq-attempt" :style="{ width: iqAttemptWidth + '%', left: (iqOldWidth + iqBaseWidth + iqPerfectWidth + iqStreakWidth) + '%' }" title="Versuch-Bonus" @mouseenter="hoverSegment('attempt')" @mouseleave="hoverSegment('')"></div>
          <div v-if="hoveredSegment" class="iq-tooltip" :class="'iq-tooltip-' + hoveredSegment">
            <span v-if="hoveredSegment === 'base'">Basis-Punkte: Punkte für das Quiz</span>
            <span v-if="hoveredSegment === 'perfect'">Perfect-Score-Bonus: Alle Fragen richtig!</span>
            <span v-if="hoveredSegment === 'streak'">Streak-Bonus: Deine aktuelle Serie</span>
            <span v-if="hoveredSegment === 'attempt'">Versuch-Bonus: Bonus für die Anzahl der Versuche</span>
          </div>
        </div>
        <div class="iq-bar-scale">
          <span>0</span>
          <span>100</span>
        </div>
        <div class="iq-bar-labels">
          <transition name="fade"><div v-if="showBaseLabel" class="iq-label iq-base-label">+{{ iq_base }} Punkte für das Quiz</div></transition>
          <transition name="fade"><div v-if="showPerfectLabel" class="iq-label iq-perfect-label">+{{ iq_perfect }} Perfect-Score-Bonus</div></transition>
          <transition name="fade"><div v-if="showStreakLabel" class="iq-label iq-streak-label">+{{ iq_streak }} Streak-Bonus (du hast eine {{ streak }}er Streak)</div></transition>
          <transition name="fade"><div v-if="showAttemptLabel" class="iq-label iq-attempt-label">+{{ iq_attampt }} Versuch-Bonus (das ist dein {{ attempts }}. Versuch)</div></transition>
        </div>
      </div>
      <div class="iq-total">
        Gesamt: <span class="iq-total-value">+{{ iq_total }}</span>
      </div>
      <div class="iq-prev-next">
        <span class="iq-prev">{{ iq_prev }}</span>
        <span class="iq-arrow">→</span>
        <span class="iq-new">{{ iq_new }}</span>
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
const hoveredSegment = ref('')
function hoverSegment(seg) {
  hoveredSegment.value = seg
}
const iqOldWidth = ref(0)
const showBaseLabel = ref(false)
const showPerfectLabel = ref(false)
const showStreakLabel = ref(false)
const showAttemptLabel = ref(false)
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { completeQuiz } from '@/services/quiz_results'

const router = useRouter()
const route = useRoute()

const loading = ref(true)
const error = ref(null)

const results = ref([])
const quizId = ref(route.query.quizId)

const correctAnswers = computed(() => results.value.filter(r => r.isCorrect).length)
const totalQuestions = computed(() => results.value.length)
const percentage = computed(() =>
  totalQuestions.value > 0
    ? Math.round((correctAnswers.value / totalQuestions.value) * 100)
    : 0
)


const iq_level = ref(0)
const iq_base = ref(0)
const iq_perfect = ref(0)
const iq_streak = ref(0)
const iq_attampt = ref(0)
const iq_total = ref(0)
const iq_prev = ref(0)
const iq_new = ref(0)

const attempts = ref(1)
const streak = ref(0)

const iqBaseWidth = ref(0)
const iqPerfectWidth = ref(0)
const iqStreakWidth = ref(0)
const iqAttemptWidth = ref(0)

function animateBar() {

  iqOldWidth.value = 0
  iqBaseWidth.value = 0
  iqPerfectWidth.value = 0
  iqStreakWidth.value = 0
  iqAttemptWidth.value = 0
  showBaseLabel.value = false
  showPerfectLabel.value = false
  showStreakLabel.value = false
  showAttemptLabel.value = false

  // Berechne Prozentwerte
  const oldW = iq_prev.value
  const baseW = iq_base.value
  const perfectW = iq_perfect.value
  const streakW =iq_streak.value
  const attemptW = iq_attampt.value

  setTimeout(() => {
    iqOldWidth.value = oldW
    setTimeout(() => {
      iqBaseWidth.value = baseW
      showBaseLabel.value = true
      setTimeout(() => {
        iqPerfectWidth.value = perfectW
        showPerfectLabel.value = true
        setTimeout(() => {
          iqStreakWidth.value = streakW
          showStreakLabel.value = true
          setTimeout(() => {
            iqAttemptWidth.value = attemptW
            showAttemptLabel.value = true
          }, 400)
        }, 400)
      }, 400)
    }, 400)
  }, 400)
}

onMounted(async () => {
  const stored = localStorage.getItem('quizResults')
  if (stored) {
    results.value = JSON.parse(stored)
  }
  
  // Notify server of quiz completion
  if (quizId.value) {
    const iq_calc = await completeQuiz(quizId.value, correctAnswers.value)
    iq_base.value = iq_calc.base_points || 0
    iq_perfect.value = iq_calc.perfect_bonus_points || 0
    iq_streak.value = iq_calc.streak_bonus_points || 0
    iq_attampt.value = iq_calc.attempt_bonus_points || 0
    iq_total.value = iq_calc.total_points || 0
    iq_prev.value = iq_calc.prev_iq || 0
    iq_new.value = iq_calc.new_iq || 0
    iq_level.value = Math.floor(iq_calc.new_iq / 100)
    attempts.value = iq_calc.attempts || 1
    streak.value = iq_calc.streak || 0
    animateBar()
  } else {
    error.value = new Error('Keine Quiz-ID angegeben')
  }
  loading.value = false
})



function restartQuiz() {
  localStorage.removeItem('quizResults')
  router.push({ 
    name: 'quiz',
    params: { quizId: quizId.value }
  })
}

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
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 1px 6px rgba(34,34,34,0.08);
  position: relative;
  border: 2px solid var(--color-bg-light);
}
.iq-segment.iq-old {
  background: var(--color-primary);
  z-index: 1;
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
  padding: 2px 10px;
  border-radius: 8px;
  margin-bottom: 2px;
  animation: popIn 0.5s;
}
.iq-base-label { color: var(--color-secondary); background: var(--color-bg-light); }
.iq-perfect-label { color: color-mix(in oklab, var(--color-secondary) 90%, #ffffff 20%); background: var(--color-bg-light); }
.iq-streak-label { color: color-mix(in oklab, var(--color-secondary) 90%, #ffffff 40%); background: var(--color-bg-light); }
.iq-attempt-label { color: color-mix(in oklab, var(--color-secondary) 90%, #ffffff 60%); background: var(--color-bg-light); }
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
  cursor: pointer;
}
.iq-segment:hover {
  box-shadow: 0 0 0 3px rgba(33,150,243,0.18);
  filter: brightness(1.08);
  z-index: 2;
}
.iq-tooltip {
  position: absolute;
  top: -38px;
  left: 50%;
  transform: translateX(-50%);
  background: #fff;
  color: #222;
  padding: 7px 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(34,34,34,0.12);
  font-size: 1rem;
  font-weight: 500;
  pointer-events: none;
  white-space: nowrap;
  z-index: 10;
  animation: popIn 0.3s;
}
.iq-tooltip-base { border: 2px solid var(--color-secondary); color: var(--color-secondary); }
.iq-tooltip-perfect { border: 2px solid #ffd700; color: #ffd700; }
.iq-tooltip-streak { border: 2px solid #4caf50; color: #4caf50; }
.iq-tooltip-attempt { border: 2px solid #2196f3; color: #2196f3; }
.iq-base {
  background: var(--color-secondary);
}
.iq-perfect {
  background: color-mix(in oklab, var(--color-secondary) 90%, #ffffff 20%);
}
.iq-streak {
  background: color-mix(in oklab, var(--color-secondary) 90%, #ffffff 40%);
}
.iq-attempt {
  background: color-mix(in oklab, var(--color-secondary) 90%, #ffffff 60%);
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
</style>
