<template>
  <div class="quiz-overview-container">
    <div v-if="loading" class="loading-card">Lade Quiz …</div>
    <div v-else-if="error" class="error-card">{{ error }}</div>

    <template v-else-if="quiz">
      <div class="card quiz-card hero-card">
        <div class="hero-left">
          <div class="quiz-header">
            <h1 class="hero-title">{{ quiz.title }}</h1>
            <p class="hero-sub">{{ quiz.description }}</p>
          </div>

          <div class="meta-row">
            <div class="meta-item">
              <strong>Erstellt</strong>
              <div>{{ formatDate(quiz.created_at) }}</div>
            </div>
            <div class="meta-item">
              <strong>von</strong>
              <div>{{ quiz.created_by ?? '-' }}</div>
            </div>
            <div class="meta-item">
              <strong>Fragen</strong>
              <div>{{ quiz.questions.length }}</div>
            </div>
            <div class="meta-item">
              <strong>Ø Zeit</strong>
              <div>{{ quiz.avg_time_spent ? quiz.avg_time_spent + 's' : '-' }}</div>
            </div>
            <div class="meta-item">
              <strong>Lernset</strong>
              <div>{{ quiz.lernset?.title || '-' }}</div>
            </div>
          </div>

          <div class="button-row hero-actions">
            <button class="btn btn-primary" @click="startQuiz">Quiz starten</button>
            <button class="btn btn-ghost" @click="goToLernset">Zum Lernset</button>
            <button class="btn btn-outline" @click="showStats = true">Statistiken</button>
            <button v-if="canEdit" class="settings-btn" @click="goToEditQuiz" :disabled="loading" aria-label="Einstellungen">
              <IconSettings />
            </button>
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
          <li v-for="(h, i) in quizHistory.slice().reverse()" :key="i" class="history-item" @click="showRun(quizHistory.length - 1 - i); showStats = true">
            <div class="history-left">
              <div class="history-percent">{{ h.percentage ?? '-' }}%</div>
              <div class="history-info">
                <div class="muted">{{ formatDate(h.timestamp) }}</div>
                <div>{{ h.correctAnswers ?? 0 }} / {{ h.totalQuestions ?? 0 }} richtig</div>
              </div>
            </div>
            <div class="history-right">
              <button class="btn btn-sm" @click.stop="showRun(quizHistory.length - 1 - i); showStats = true">Anzeigen</button>
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
            <div class="stats-grid two-columns">
              <div class="stat-column">
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

              <div class="stat-column">
                <div class="stat-card">
                  <div class="stat-label">Insgesamt (Alle Durchläufe)</div>
                  <div class="stat-value">{{ aggregate.avgPercentage }}%</div>
                </div>
                <div class="stat-card">
                  <div class="stat-label">Richtig Gesamt</div>
                  <div class="stat-value">{{ aggregate.correctAnswers }}</div>
                </div>
                <div class="stat-card">
                  <div class="stat-label">Gesamtfragen</div>
                  <div class="stat-value">{{ aggregate.totalQuestions }}</div>
                </div>
              </div>
            </div>
            <div class="muted" style="margin-top:.5rem">Versuche: {{ aggregate.attempts }}</div>

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
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getQuiz, getQuizSessions } from '@/services/quizzes'    // <-- added getQuizSessions
import IconSettings from '@/components/icons/IconSettings.vue'
import { useQuizEditStore } from '@/stores/editQuiz'
import { useUserStore } from '@/stores/user'

const showStats = ref(false)
const router = useRouter()
const route = useRoute()
const quizEdit = useQuizEditStore()
const userStore = useUserStore()

// Replace local dummy quiz with API-driven state
const quiz = ref(null)
const loading = ref(true)
const error = ref(null)

// Keep existing quizHistory/dummy fallback if needed
const quizHistory = ref([])

// ensure currentRunIndex exists early so loader can set it
const currentRunIndex = ref(0)

// helper to load per-quiz history (try server first, fallback to localStorage)
async function loadHistoryFromStorage() {
  const qid = route.params.quizId
  if (!qid) {
    quizHistory.value = []
    currentRunIndex.value = 0
    return
  }

  // Try server sessions first
  try {
    const sessions = await getQuizSessions(qid)
    // apiClient.get may return response body directly (service helpers in this project return parsed body)
    const runs = Array.isArray(sessions) ? sessions : (sessions?.results || sessions?.data || [])
    if (Array.isArray(runs) && runs.length > 0) {
      // normalize server session shape to expected run shape used in the UI
      quizHistory.value = runs.map(s => {
        const results = Array.isArray(s.results) ? s.results : (s.answers || [])
        const correctAnswers = typeof s.score === 'number' ? s.score : results.filter(r => r.isCorrect).length
        const totalQuestions = typeof s.total === 'number' ? s.total : results.length
        const percentage = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : (s.percentage || 0)
        return {
          timestamp: s.end_time || s.created_at || s.start_time || s.timestamp || null,
          results: results,
          correctAnswers,
          totalQuestions,
          percentage
        }
      })
      currentRunIndex.value = Math.max(quizHistory.value.length - 1, 0)
      return
    }
  } catch (err) {
    // server call failed -> fallback to localStorage silently
    console.warn('Failed to fetch quiz sessions from server, falling back to localStorage', err)
  }

  // Fallback: localStorage key
  const key = `quizHistory_${qid}`
  try {
    const raw = localStorage.getItem(key)
    const parsed = raw ? JSON.parse(raw) : []
    quizHistory.value = Array.isArray(parsed) ? parsed : []
    currentRunIndex.value = Math.max(quizHistory.value.length - 1, 0)
  } catch (err) {
    console.error('Error loading quizHistory from localStorage', err)
    quizHistory.value = []
    currentRunIndex.value = 0
  }
}

// Fetch quiz from API on mount
onMounted(async () => {
  const qid = route.params.quizId
  if (!qid) {
    error.value = 'Keine Quiz-ID vorhanden'
    loading.value = false
    return
  }

  try {
    loading.value = true
    const data = await getQuiz(qid)
    quiz.value = data
    // Persist creator for later permission checks (mirrors edit route behavior)
    const creator = data.created_by || data.createdBy || data.creator_username || null
    if (creator) quizEdit.quizCreator = creator
    // Ensure user data loaded for permission checks
    await userStore.loadCurrentUser()
    // load history after quiz known
    loadHistoryFromStorage()
  } catch (err) {
    console.error('Error fetching quiz:', err)
    error.value = 'Fehler beim Laden des Quiz'
    quiz.value = null
  } finally {
    loading.value = false
  }
})

// refresh history when the stats modal opens
watch(showStats, (val) => {
  if (val) loadHistoryFromStorage()
})

// refresh whenever route changes (user navigated back here)
watch(() => route.fullPath, () => {
  loadHistoryFromStorage()
})

// also listen to storage events (other tabs) to keep UI in sync
function onStorageEvent(e) {
  const qid = route.params.quizId
  if (!qid) return
  if (e.key === `quizHistory_${qid}`) loadHistoryFromStorage()
}
window.addEventListener('storage', onStorageEvent)
onBeforeUnmount(() => window.removeEventListener('storage', onStorageEvent))

const current = computed(() => {
  if (!Array.isArray(quizHistory.value) || quizHistory.value.length === 0) {
    return {
      timestamp: null,
      results: [],
      correctAnswers: 0,
      totalQuestions: 0,
      percentage: 0
    }
  }
  const idx = Math.min(Math.max(currentRunIndex.value || 0, 0), quizHistory.value.length - 1)
  const entry = quizHistory.value[idx] || { results: [] }
  const resultsArr = Array.isArray(entry.results) ? entry.results : []
  const correctAnswers = resultsArr.filter(r => r.isCorrect).length
  const totalQuestions = resultsArr.length
  const percentage = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : (entry.percentage || 0)
  return {
    ...entry,
    results: resultsArr,
    correctAnswers,
    totalQuestions,
    percentage
  }
})

// Aggregate across all runs (for modal "Insgesamt")
const aggregate = computed(() => {
  const runs = Array.isArray(quizHistory.value) ? quizHistory.value : []
  if (runs.length === 0) {
    return { attempts: 0, correctAnswers: 0, totalQuestions: 0, avgPercentage: 0, runs: [] }
  }
  let totalCorrect = 0
  let totalQ = 0
  runs.forEach(run => {
    const results = Array.isArray(run.results) ? run.results : []
    totalCorrect += results.filter(r => r.isCorrect).length
    totalQ += results.length
  })
  const avgPercentage = totalQ > 0 ? Math.round((totalCorrect / totalQ) * 100) : 0
  return { attempts: runs.length, correctAnswers: totalCorrect, totalQuestions: totalQ, avgPercentage, runs }
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

function goToEditQuiz() {
  if (!quiz.value || !quiz.value.id) {
    error.value = 'Quiz konnte nicht bearbeitet werden (ID fehlt)'
    return
  }
  // Try to read lernset id: could be a number or object with id
  const lernsetId = quiz.value.lernset && typeof quiz.value.lernset === 'object'
    ? quiz.value.lernset.id
    : quiz.value.lernset
  if (lernsetId) {
    quizEdit.setLernset(lernsetId)
  }
  router.push({ name: 'edit-quiz', params: { quizId: quiz.value.id, lernsetId } })
}

function showRun(idx) {
  const clamped = Math.min(Math.max(idx, 0), Math.max(quizHistory.value.length - 1, 0))
  currentRunIndex.value = clamped
}

function formatDate(ts) {
  if (!ts) return '-'
  const d = new Date(ts)
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Only allow edit if current user is creator or has moderator role
const canEdit = computed(() => {
  if (!quiz.value) return false
  const creator = quiz.value.created_by || quiz.value.createdBy || quiz.value.creator_username || quizEdit.quizCreator
  if (!userStore.loaded) return false
  return userStore.isOwner(creator) || userStore.isModerator()
})
</script>

<style scoped>
/* Enhanced visual styles for QuizOverview */

.quiz-overview-container { max-width: 1100px; margin: 2rem auto; padding: 0 1rem; font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; color: #0f172a; }

/* Hero card */
.hero-card { display: flex; gap: 1.25rem; background: linear-gradient(180deg,#fff 0%, #fff9f2 60%); padding: 1.25rem; border-radius: 14px; box-shadow: 0 12px 30px rgba(16,24,40,0.06); align-items: stretch; }
.hero-left { flex: 1 1 70%; display:flex; flex-direction:column; gap: 14px; }
.hero-right { width: 300px; display:flex; align-items:center; justify-content:center; }

/* Title */
.hero-title { margin:0; font-size:1.6rem; line-height:1.15; color:#0b1220; font-weight:700; }
.hero-sub { margin:0; color:#374151; font-size:0.98rem; }

/* Meta */
.meta-row { display:flex; gap: .75rem; flex-wrap:wrap; margin-top:6px; }
.meta-item { background: rgba(15,23,42,0.03); padding:.5rem .7rem; border-radius:10px; min-width:120px; }
.meta-item strong { display:block; color:#6b7280; font-size:0.78rem; margin-bottom:4px; }
.meta-item div { font-weight:600; color:#0f172a; }

/* Actions */
.hero-actions { display:flex; gap:.6rem; align-items:center; margin-top: 6px; flex-wrap:wrap; }
.btn { padding:.55rem .9rem; border-radius:10px; border:none; cursor:pointer; background:transparent; font-weight:600; }
.btn-primary { background: linear-gradient(90deg,#ff8a3d,#ff6a00); color:#fff; box-shadow: 0 6px 20px rgba(255,106,0,0.12); }
.btn-ghost { border:1px solid rgba(15,23,42,0.06); color:#0f172a; background:#fff; }
.btn-outline { border:1px solid rgba(255,106,0,0.14); color:#ff6a00; background:#fff; }
.settings-btn { background: transparent; border: none; margin-left: 6px; align-self:flex-start; }

/* Right stat card */
.card-stats { background: #fff; padding:1rem; border-radius:12px; text-align:center; box-shadow: 0 8px 24px rgba(16,24,40,0.04); width:100%; }
.card-stats h4 { margin:0; color:#475569; font-size:0.95rem; }
.stat-big { font-size:2rem; margin-top:.6rem; color:#ff6a00; font-weight:700; }
.stat-sub { color:#6b7280; font-size:0.9rem; margin-top:.5rem; display:flex; gap:.5rem; justify-content:center; align-items:center; }

/* Progress */
.progress-bar { height:9px; background:#fff5ec; border-radius:99px; margin-top:12px; overflow:hidden; }
.progress-fill { height:100%; background: linear-gradient(90deg,#ff8a3d,#ff6a00); transition: width .5s ease; }

/* History */
.history-section { margin-top:1.25rem; }
.history-list { list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:.6rem; }
.history-item { display:flex; justify-content:space-between; align-items:center; padding:.75rem; border-radius:10px; background:#fff; border:1px solid rgba(15,23,42,0.03); transition:transform .12s, box-shadow .12s; cursor:pointer; }
.history-item:hover { transform:translateY(-4px); box-shadow: 0 12px 30px rgba(16,24,40,0.06); }
.history-left { display:flex; gap:.75rem; align-items:center; }
.history-percent { font-weight:700; color:#ff6a00; font-size:1.05rem; margin-right:.6rem; }
.history-info .muted { color:#6b7280; font-size:0.86rem; }

/* Modal */
.modal-overlay { position:fixed; inset:0; background: rgba(2,6,23,0.45); display:flex; align-items:center; justify-content:center; z-index:9999; padding:20px; }
.modal-content { width:min(880px,96%); background:#fff; border-radius:12px; padding:1rem 1.15rem; box-shadow:0 20px 50px rgba(2,6,23,0.35); }
.modal-content header { display:flex; justify-content:space-between; align-items:center; gap:10px; }
.modal-body { margin-top:.9rem; }
.stats-grid { display:flex; gap:.75rem; margin-bottom:.9rem; }
.stat-card { flex:1; background:#fff7f3; padding:.6rem; border-radius:8px; text-align:center; }
.stat-label { color:#6b7280; font-size:.85rem; }
.stat-value { font-weight:700; color:#ff6a00; font-size:1.25rem; margin-top:.25rem; }

/* Results list */
.results-list { list-style:none; padding:0; margin:0; display:grid; gap:.5rem; max-height:320px; overflow:auto; }
.result-item { padding:.6rem; border-radius:8px; background:#fff; border:1px solid #fff3ea; }
.q-text { font-weight:600; color:#0f172a; }
.a-row { display:flex; gap:.5rem; align-items:center; margin-top:.35rem; }
.tag { padding:.18rem .45rem; border-radius:999px; font-size:.78rem; }
.tag-good { background:#ecfdf5; color:#059669; }
.tag-bad { background:#fff1f2; color:#dc2626; }

.muted { color:#6b7280; font-size:.9rem; }

/* small helpers */
.loading-card, .error-card { padding:1rem; background:#fff; border-radius:10px; text-align:center; box-shadow:0 10px 30px rgba(2,6,23,0.04); }
.btn-icon { background:transparent; border:none; cursor:pointer; font-size:1.05rem; }
@media (max-width: 900px) {
  .hero-card { flex-direction:column; }
  .hero-right { width:auto; }
  .meta-item { min-width:120px; flex:1 1 45%; }
}
</style>
