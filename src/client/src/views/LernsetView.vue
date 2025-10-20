<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import IconPlus from '@/components/icons/IconPlus.vue' // Passe ggf. den Pfad an
import { getLernset, getLernsetQuizzes } from '@/services/lernsets'

const router = useRouter()
const route = useRoute()

// Reactive state
const lernsetName = ref('Lernset')
const modulName = ref('')
const lernsetBeschreibung = ref('')
const lernset = ref(null) // whole lernset object if needed

// Read lernsetId from route params (optional)
const lernsetId = route.params.lernsetId || null

// Always-shown hardcoded quizzes (IDs use 'local-' prefix to avoid collisions)
const defaultQuickQuiz = {
  id: 'local-quick-1',
  title: 'Schnelltest: Schlüsselbegriffe',
  description: 'Kurzes Schnellquiz zu den wichtigsten Begriffen (immer sichtbar)'
}

const defaultQuiz = {
  id: 'local-quiz-1',
  title: 'Übersichts-Quiz (immer)',
  questionCount: 5,
  rating: 4,
  creator: 'StudIQ'
}

const quickQuizzes = ref([defaultQuickQuiz])
const quizzes = ref([defaultQuiz])

const loading = ref(false)
const error = ref(null)

async function fetchLernsetDetails(id) {
  if (!id) return
  try {
    const data = await getLernset(id) //LernsetService-Abfrage
    lernset.value = data
    lernsetName.value = data.title || data.name || lernsetName.value
    lernsetBeschreibung.value = data.description || lernsetBeschreibung.value
    // try to set modul name if API provides nested modul
    modulName.value = data.modul?.name || data.modul_name || modulName.value
  } catch (err) {
    console.warn('fetchLernsetDetails:', err)
    error.value = 'Fehler beim Laden des Lernset-Details.'
  }
}

async function fetchQuizzesForLernset(id) {
  if (!id) return
  loading.value = true
  error.value = null
  try {
    const data = await getLernsetQuizzes(id) // expect array
    const all = Array.isArray(data) ? data : []

    // API-Antwort auf die richtigen Attribute mappen
    const mapped = all.map(q => ({
      id: q.id,
      title: q.title || q.name || q.heading || 'Untitled',
      description: q.description || q.summary || '',
      questionCount: q.question_count ?? (q.questions ? q.questions.length : 0) ?? 0,
      rating: Number(q.rating ?? 0),
      creator: q.created_by_username || q.creator || q.creator_name || q.owner || '' ,
      isQuick: Boolean(q.is_quick || q.quick || q.type === 'quick')
    }))

  //Quick- von normalen Quizzes trennen
  const serverQuick = mapped.filter(m => m.isQuick)
  const serverNormal = mapped.filter(m => !m.isQuick)

  //gehardcodetes Quiz immer oben angezeigt, danach Quizzes vom Server
  //Filter sorgt dafür, dass ID vom gehardcodeten Quiz nicht einer ID vom Serverquiz in die Quere kommt
  quickQuizzes.value = [defaultQuickQuiz, ...serverQuick.filter(s => String(s.id) !== String(defaultQuickQuiz.id))]
  quizzes.value = [defaultQuiz, ...serverNormal.filter(s => String(s.id) !== String(defaultQuiz.id))]
  } catch (err) {
    console.error('Fehler beim Laden der Quizzes:', err)
    error.value = 'Fehler beim Laden der Quizze.'
  } finally {
    loading.value = false
  }
}

const goToQuizOverview = (quizId) => {
  router.push({ name: 'quiz-overview', params: { quizId } })
}

const goToEditQuiz = () => {
  router.push({ name: 'edit-quiz', params: { quizId } })
}

// Hilfsfunktion für Sterne
const getStars = (rating) => {
  const fullStars = Math.floor(rating)
  const hasHalfStar = rating - fullStars >= 0.5
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0)
  return {
    full: fullStars,
    half: hasHalfStar,
    empty: emptyStars
  }
}

onMounted(() => {
  if (lernsetId) {
    fetchLernsetDetails(lernsetId)
    fetchQuizzesForLernset(lernsetId)
  }
})
</script>

<template>
  <div class="lernset-view">
    <!-- Titelzeile -->
    <div class="header-row">
      <h1 class="lernset-title">{{ lernsetName }}</h1>
      <span class="modul-label">{{ modulName }}</span>
    </div>

    <!-- Beschreibung -->
    <div class="lernset-description">
      {{ lernsetBeschreibung }}
    </div>

    <!-- Quick-Quiz -->
    <section class="quick-quiz-section">
      <h2 class="section-title">Quick-Quiz</h2>
      <div class="quick-quiz-list">
        <button
          v-for="quiz in quickQuizzes"
          :key="quiz.id"
          class="quick-quiz-btn"
          @click="goToQuizOverview(quiz.id)"
        >
          <span class="quick-quiz-title">{{ quiz.title }}</span>
          <span class="quick-quiz-desc">{{ quiz.description }}</span>
        </button>
      </div>
    </section>

    <!-- Normale Quizze -->
    <section class="quizzes-section">
      <div class="quizze-title-row">
        <h2 class="section-title">Quizze</h2>
        <button
          class="plus-btn"
          @click="goToEditQuiz"
          aria-label="Quiz hinzufügen"
        >
          <IconPlus />
        </button>
      </div>
      <div class="quizzes-list">
        <button
          v-for="quiz in quizzes"
          :key="quiz.id"
          class="quiz-btn"
          @click="goToQuizOverview(quiz.id)"
        >
          <div class="quiz-btn-header">
            <span class="quiz-title">{{ quiz.title }}</span>
            <span class="quiz-question-count">{{ quiz.questionCount }} Fragen</span>
          </div>
          <div class="quiz-rating-row">
            <span class="quiz-stars">
              <template v-for="n in getStars(quiz.rating).full" :key="'full' +quiz.id+'-'+n">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="#FFC107" style="vertical-align:middle">
                  <polygon points="10,1.5 12.7,7.6 19.2,8.1 14,12.7 15.6,19.1 10,15.7 4.4,19.1 6,12.7 0.8,8.1 7.3,7.6"/>
                </svg>
              </template>
              <template v-if="getStars(quiz.rating).half">
                <svg width="20" height="20" viewBox="0 0 20 20" style="vertical-align:middle" key="half">
                  <defs>
                    <linearGradient id="halfstar" x1="0" y1="0" x2="100%" y2="0">
                      <stop offset="50%" stop-color="#FFC107"/>
                      <stop offset="50%" stop-color="#E0E0E0"/>
                    </linearGradient>
                  </defs>
                  <polygon points="10,1.5 12.7,7.6 19.2,8.1 14,12.7 15.6,19.1 10,15.7 4.4,19.1 6,12.7 0.8,8.1 7.3,7.6" fill="url(#halfstar)" />
                </svg>
              </template>
              <template v-for="n in getStars(quiz.rating).empty" :key="'empty' +quiz.id+'-'+n">
                <svg 
                    width="20" height="20" viewBox="0 0 20 20" fill="#E0E0E0" style="vertical-align:middle" 
                    >
                  <polygon points="10,1.5 12.7,7.6 19.2,8.1 14,12.7 15.6,19.1 10,15.7 4.4,19.1 6,12.7 0.8,8.1 7.3,7.6"/>
                </svg>
              </template>
            </span>
            <span class="quiz-creator">Erstellt von: <b>{{ quiz.creator }}</b></span>
          </div>
        </button>
      </div>
    </section>
  </div>
</template>

<style scoped>
.lernset-view {
  max-width: 700px;
  margin: 0 auto;
  padding: 30px 18px 0 18px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 8px;
}

.lernset-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-primary, #1976d2);
  word-break: break-word;
  margin: 0;
}

.modul-label {
  font-size: 1.1rem;
  color: #666;
  background: #e3f2fd;
  border-radius: 8px;
  padding: 7px 17px;
  font-weight: 500;
  margin-left: 12px;
}

.lernset-description {
  font-size: 1.08rem;
  color: #222;
  margin-bottom: 16px;
}

.section-title {
  font-size: 1.18rem;
  font-weight: 600;
  color: var(--color-accent, #1565c0);
  margin-bottom: 14px;
}

.quizze-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 10px;
}
.plus-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: var(--color-primary, #1976d2);
  display: flex;
  align-items: center;
  transition: color 0.18s;
}
.plus-btn:hover,
.plus-btn:focus {
  color: #1565c0;
}
.plus-btn svg {
  width: 2.1rem;
  height: 2.1rem;
}

.quick-quiz-list {
  display: flex;
  flex-direction: row;
  gap: 18px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.quick-quiz-btn {
  background: #f2f8fd;
  border: 1.5px solid #e3f2fd;
  border-radius: 10px;
  padding: 18px 16px;
  min-width: 190px;
  flex: 1 1 0;
  text-align: left;
  cursor: pointer;
  transition: border 0.15s, box-shadow 0.15s;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 1rem;
}
.quick-quiz-btn:hover, .quick-quiz-btn:focus {
  border: 1.5px solid #1976d2;
  box-shadow: 0 2px 10px 2px rgba(25, 118, 210, 0.08);
  background: #e3f2fd;
}
.quick-quiz-title {
  font-weight: 600;
  color: #1976d2;
  font-size: 1.07rem;
}
.quick-quiz-desc {
  color: #444;
  font-size: 0.97rem;
}

.quizzes-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.quiz-btn {
  background: #fff;
  border: 1.5px solid #e3f2fd;
  border-radius: 10px;
  padding: 18px 16px;
  text-align: left;
  cursor: pointer;
  transition: border 0.15s, box-shadow 0.15s;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.quiz-btn:hover, .quiz-btn:focus {
  border: 1.5px solid #1976d2;
  box-shadow: 0 2px 10px 2px rgba(25, 118, 210, 0.08);
  background: #f2f8fd;
}

.quiz-btn-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 4px;
}
.quiz-title {
  font-weight: 600;
  font-size: 1.06rem;
  color: #1976d2;
  word-break: break-word;
}
.quiz-question-count {
  font-size: 0.98rem;
  color: #1976d2;
  background: #e3f2fd;
  border-radius: 8px;
  padding: 2px 13px;
  font-weight: 500;
  margin-left: 10px;
}

.quiz-rating-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}
.quiz-stars {
  display: flex;
  align-items: center;
  gap: 2px;
}
.quiz-creator {
  font-size: 0.94rem;
  color: #888;
  margin-left: 16px;
  white-space: nowrap;
}
</style>