<template>
  <div class="quiz-overview-container">
    <div v-if="loading" class="loading-card">Lade Quiz …</div>
    <div v-else-if="error" class="error-card">{{ error }}</div>

    <template v-else-if="quiz">
      <div class="hero-card">
        <div class="hero-left">
          <h1 class="hero-title">{{ quiz.title }}</h1>
          <p class="hero-sub">{{ quiz.description }}</p>

          <div class="meta-row">
            <div class="meta-item small">
              <strong>Fragen</strong>
              <span>{{ quiz.questions?.length ?? '-' }}</span>
            </div>
            <div class="meta-item small">
              <strong>Ø Zeit</strong>
              <span>{{ quiz.avg_time_spent ?? '-' }}s</span>
            </div>
            <div class="meta-item small">
              <strong>Erstellt</strong>
              <span>{{ formatDate(quiz.created_at) }}</span>
            </div>
            <div class="meta-item small">
              <strong>von</strong>
              <span>{{ quiz.created_by ?? '-' }}</span>
            </div>
          </div>

          <div class="button-row">
            <button class="btn btn-primary" @click="startQuiz">Quiz starten</button>
            <button class="btn btn-ghost" @click="goToLernset">Zum Lernset</button>
            <button class="btn btn-outline" @click="showStats = true">Statistiken</button>
          </div>
        </div>

        <div class="hero-right">
          <div class="card-stats">
            <h4>Letzte Runde</h4>
            <div class="stat-big">{{ current.percentage ?? '-' }}%</div>
            <div class="stat-sub">
              <span>{{ current.correctAnswers ?? 0 }} / {{ current.totalQuestions ?? 0 }} richtig</span>
              <span class="muted">• {{ formatDate(current.timestamp) }}</span>
            </div>

            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: (current.percentage ?? 0) + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- history -->
      <section class="history-section">
        <h3>Verlauf</h3>
        <div v-if="quizHistory.length === 0" class="no-history">Keine bisherigen Durchläufe</div>
        <ul v-else class="history-list">
          <li v-for="(h, i) in quizHistory.slice().reverse()" :key="i" class="history-item">
            <div class="history-left">
              <div class="history-percent">{{ h.percentage ?? '-' }}%</div>
              <div class="history-info">
                <div class="muted">{{ formatDate(h.timestamp) }}</div>
                <div>{{ h.correctAnswers ?? 0 }} / {{ h.totalQuestions ?? 0 }} richtig</div>
              </div>
            </div>
            <div class="history-right">
              <button class="btn btn-sm" @click="showRun(quizHistory.length - 1 - i); showStats = true">Anzeigen</button>
            </div>
          </li>
        </ul>
      </section>

      <!-- stats modal -->
      <div v-if="showStats" class="modal-overlay" @click.self="showStats = false">
        <div class="modal-content">
          <header>
            <h3>Statistiken — {{ quiz.title }}</h3>
            <button class="btn-icon" @click="showStats = false">✕</button>
          </header>

          <div class="modal-body">
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-label">Letzte Genauigkeit</div>
                <div class="stat-value">{{ current.percentage ?? 0 }}%</div>
              </div>
              <div class="stat-card">
                <div class="stat-label">Richtig</div>
                <div class="stat-value">{{ current.correctAnswers ?? 0 }}</div>
              </div>
              <div class="stat-card">
                <div class="stat-label">Gesamt</div>
                <div class="stat-value">{{ current.totalQuestions ?? 0 }}</div>
              </div>
            </div>

            <h4>Antworten</h4>
            <ul class="results-list">
              <li v-for="(r, idx) in current.results" :key="idx" class="result-item">
                <div class="q-text">{{ r.question }}</div>
                <div class="a-row">
                  <span :class="['tag', r.isCorrect ? 'tag-good' : 'tag-bad']">
                    {{ r.isCorrect ? 'Richtig' : 'Falsch' }}
                  </span>
                  <div class="muted">Gewählte: {{ r.selected ?? '-' }}</div>
                </div>
              </li>
            </ul>
          </div>

          <footer class="modal-footer">
            <button class="btn" @click="showStats = false">Schließen</button>
          </footer>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getQuiz } from '@/services/quizzes'
import IconSettings from '@/components/icons/IconSettings.vue'

const showStats = ref(false)
const router = useRouter()
const route = useRoute()

// Replace local dummy quiz with API-driven state
const quiz = ref(null)
const loading = ref(true)
const error = ref(null)

// Keep existing quizHistory/dummy fallback if needed
const quizHistory = ref([])

// Fetch quiz from API on mount
onMounted(async () => {
  const quizId = route.params.quizId
  if (!quizId) {
    error.value = 'Keine Quiz-ID vorhanden'
    loading.value = false
    return
  }

  try {
    loading.value = true
    const data = await getQuiz(quizId)
    // Expect service to return the quiz object directly (consistent with other services)
    quiz.value = data
  } catch (err) {
    console.error('Error fetching quiz:', err)
    error.value = 'Fehler beim Laden des Quiz'
    // Optional: keep a minimal fallback (previous dummy) or leave null
    quiz.value = null
  } finally {
    loading.value = false
  }
})

const currentRunIndex = ref(Math.max(quizHistory.value.length - 1, 0))

const current = computed(() => {
  // if no history, return a safe default object
  if (!Array.isArray(quizHistory.value) || quizHistory.value.length === 0) {
    return {
      timestamp: null,
      results: [],
      correctAnswers: 0,
      totalQuestions: 0,
      percentage: 0
    }
  }

  // clamp index into valid range
  const idx = Math.min(Math.max(currentRunIndex.value || 0, 0), quizHistory.value.length - 1)
  const entry = quizHistory.value[idx] || { results: [] }

  const resultsArr = Array.isArray(entry.results) ? entry.results : []
  const correctAnswers = resultsArr.filter(r => r.isCorrect).length
  const totalQuestions = resultsArr.length
  const percentage = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0

  return {
    ...entry,
    results: resultsArr,
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
  if (!quiz.value || !quiz.value.id) {
    error.value = 'Quiz konnte nicht gestartet werden (ID fehlt)'
    return
  }
  router.push({ name: 'quiz', params: { quizId: quiz.value.id } })
}

function goToLernset() {
  if (quiz.value?.lernset) {
    router.push({ name: 'lernset', params: { lernsetId: quiz.value.lernset } })
  } else {
    router.push('/')
  }
}

function showRun(idx) {
  // clamp incoming idx and update
  const clamped = Math.min(Math.max(idx, 0), Math.max(quizHistory.value.length - 1, 0))
  currentRunIndex.value = clamped
}

function formatDate(ts) {
  if (!ts) return '-'
  const d = new Date(ts)
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.quiz-overview-container {
  max-width: 1100px;
  margin: 2rem auto;
  padding: 0 1rem;
}

/* Hero card */
.hero-card {
  display: flex;
  gap: 1.25rem;
  background: linear-gradient(135deg, #ffffff 0%, #fff7f0 100%); /* softened to warm bg */
  padding: 1.25rem;
  border-radius: 12px;
  /* use orange shadow instead of blue */
  box-shadow: 0 8px 30px rgba(255,106,0,0.06);
  align-items: stretch;
}

.hero-left {
  flex: 1 1 60%;
}

.hero-title {
  margin: 0;
  font-size: 1.75rem;
  color: #0f172a;
}

.hero-sub {
  margin-top: 0.5rem;
  color: #111213ff;
}

/* meta */
.meta-row {
  display: flex;
  gap: .75rem;
  margin-top: 12px;
  flex-wrap: wrap;
}
.meta-item {
  background: rgba(15, 23, 42, 0.03);
  padding: .45rem .6rem;
  border-radius: 8px;
}
/* labels and values in meta boxes set to orange */
.meta-item.small strong { display:block; font-size: .75rem; color: #0e0d0dff; }
.meta-item.small span { font-weight:600; color:#ff6a00; }

/* Buttons */
.button-row { margin-top: 16px; display:flex; gap:.6rem; align-items:center; }
.btn { padding: .5rem .9rem; border-radius: 8px; border: none; cursor: pointer; background: transparent; }
.btn-primary { 
  background: linear-gradient(90deg,#ff8a3d,#ff6a00); 
  color: #fff; 
  box-shadow: 0 6px 18px rgba(255,106,0,0.12); 
}
.btn-ghost { border: 1px solid rgba(15,23,42,0.06); color:#0f172a; }
.btn-outline { 
  border: 1px solid rgba(255,106,0,0.12); 
  color:#ff6a00; 
}
.btn-sm { padding: .35rem .6rem; font-size: .85rem; }

/* Right stats card */
.hero-right { width: 280px; display:flex; align-items:center; justify-content:center; }
.card-stats {
  background: white;
  padding: 1rem;
  border-radius: 12px;
  text-align:center;
  box-shadow: 0 6px 20px rgba(10, 10, 10, 0.04);
  width:100%;
}
.card-stats h4 { margin:0; color:#475569; }
/* stat number color -> orange */
.stat-big { font-size: 2rem; margin-top: .5rem; color:#ff6a00; font-weight:700; }
.stat-sub { color:#6b7280; font-size:.9rem; margin-top:.5rem; }

/* progress */
/* warm progress background and orange fill */
.progress-bar { height:8px; background: #fff3ea; border-radius: 99px; margin-top:12px; overflow:hidden; }
.progress-fill { height:100%; background: linear-gradient(90deg,#ff8a3d,#ff6a00); transition: width .4s ease; }

/* history list */
.history-section { 
  margin-top: 1.25rem;
  /* constrain history width to the main/left column so it lines up with the overview box */
  max-width: calc(100% - 320px); /* 280px sidebar + ~40px gap */
  margin-left: 0;
  margin-right: auto;
}
.history-list { list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:.5rem; }
.history-item { display:flex; justify-content:space-between; align-items:center; padding:.6rem; border-radius:8px; background:#fff; box-shadow: 0 3px 12px rgba(2,6,23,0.03); }
/* history percent color -> orange */
.history-percent { font-weight:700; color:#ff6a00; font-size:1.05rem; margin-right:.6rem; }
.history-info .muted { color:#6b7280; font-size:.85rem; }

/* ensure full width on small screens */
@media (max-width: 899px) {
  .history-section {
    max-width: 100%;
  }
  .hero-right { width: auto; }
}

/* tweak for larger displays if the gap or sidebar width changes */
@media (min-width: 1200px) {
  .history-section {
    max-width: calc(100% - 320px);
  }
}

/* modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(2,6,23,0.45); display:flex; align-items:center; justify-content:center; z-index:9999;
}
.modal-content {
  width: min(880px, 96%);
  background: #fff; border-radius: 12px; padding: 1rem 1.15rem; box-shadow: 0 20px 50px rgba(2,6,23,0.35);
}
.modal-content header { display:flex; justify-content:space-between; align-items:center; }
.modal-body { margin-top: 0.9rem; }
.stats-grid { display:flex; gap: .75rem; margin-bottom: .9rem; }
/* stat card background warmer and values orange */
.stat-card { flex:1; background:#fff7f3; padding:.6rem; border-radius:8px; text-align:center; }
.stat-label { color:#6b7280; font-size:.85rem; }
.stat-value { font-weight:700; color:#ff6a00; font-size:1.25rem; margin-top:.25rem; }

.results-list { list-style:none; padding:0; margin:0; display:grid; gap:.5rem; max-height:240px; overflow:auto; }
/* result-item border warm */
.result-item { padding:.6rem; border-radius:8px; background:#fff; border:1px solid #fff3ea; }
.q-text { font-weight:600; color:#0f172a; }
.a-row { display:flex; gap:.5rem; align-items:center; margin-top:.35rem; }
.tag { padding: .18rem .45rem; border-radius:99px; font-size:.78rem; }
.tag-good { background: #ecfdf5; color: #059669; }
.tag-bad { background: #fff1f2; color: #dc2626; }
.muted { color:#6b7280; font-size:.9rem; }

/* small helpers */
.loading-card, .error-card { padding:1rem; background:#fff; border-radius:10px; text-align:center; box-shadow:0 10px 30px rgba(2,6,23,0.04); }
.btn-icon { background:transparent; border:none; cursor:pointer; font-size:1.05rem; }
</style>
