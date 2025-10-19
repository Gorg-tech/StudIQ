<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import IconPlus from '@/components/icons/IconPlus.vue'
import { getLernset, getLernsetQuizzes } from '@/services/lernsets'
import apiClient from '@/services/api/client'
import { API_ENDPOINTS } from '@/services/api/endpoints'

// Real data placeholders
const lernsetName = ref('')
const modul = ref({})
const lernsetBeschreibung = ref('')

// Quick quizzes (shorter quizzes)
const quickQuizzes = ref([])

// Regular quizzes
const quizzes = ref([])

// Loading and error states
const loading = ref(true)
const error = ref(null)

const router = useRouter()
const route = useRoute()

// Fetch lernset data from API
const fetchLernsetData = async () => {
  const lernsetId = route.params.lernsetId
  if (!lernsetId) {
    error.value = 'Keine Lernset-ID gefunden'
    loading.value = false
    return
  }
  
  try {
    loading.value = true
    
    // Get lernset details
    const lernsetData = await getLernset(lernsetId)
    
    console.log('Lernset data received:', lernsetData)
    
    // Modified check to properly handle the data structure
    if (!lernsetData || typeof lernsetData !== 'object') {
      throw new Error('Lernset-Daten nicht gefunden')
    }
    
    lernsetName.value = lernsetData.title || 'Unbenanntes Lernset'
    lernsetBeschreibung.value = lernsetData.description || ''
    modul.value = lernsetData.modul || {}
    
    // Get quizzes for this lernset
    const quizzesData = lernsetData.quizzes || []

    /*
        An dieser Stelle könnten wir später auch nach dem Quiz-Modus filtern,
        z.B. um nur den "Quick Quiz"-Modus anzuzeigen.
    */

    quizzes.value = quizzesData
      .map(quiz => ({
        id: quiz.id,
        title: quiz.title || 'Unbenanntes Quiz',
        questionCount: quiz.question_count || 0,
        rating: calculateRating(quiz.rating_score, quiz.rating_count),
        creator: quiz.creator_username || 'Unbekannt'
      }))
      
  } catch (err) {
    console.error('Error fetching lernset data:', err)
    error.value = 'Fehler beim Laden des Lernsets'
  } finally {
    loading.value = false
  }
}

// Calculate rating from score and count
const calculateRating = (score, count) => {
  return count > 0 ? score / count : 0
}

const goToQuizOverview = (quizId) => {
  router.push({ name: 'quiz-overview', params: { quizId } })
}

const goToEditQuiz = () => {
  router.push({ name: 'edit-quiz' })
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

// Fetch data when component is mounted
onMounted(fetchLernsetData)
</script>

<template>
  <div class="lernset-view">
    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Lernset wird geladen...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-message">
      {{ error }}
      <button @click="fetchLernsetData" class="retry-btn">Erneut versuchen</button>
    </div>

    <!-- Content when loaded -->
    <template v-else>
      <!-- Titelzeile -->
      <div class="header-row">
        <h1 class="lernset-title">{{ lernsetName }}</h1>
        <span v-if="modul.name" class="modul-label">
          <router-link :to="{ name: 'modul', params: { modulId: modul.modulId } }">
            {{ modul.name }} ({{ modul.modulId }})
          </router-link>
        </span>
      </div>

      <!-- Beschreibung -->
      <div class="lernset-description">
        {{ lernsetBeschreibung }}
      </div>

      <!-- Quick-Quiz -->
      <section class="quick-quiz-section" v-if="quickQuizzes.length > 0">
        <h2 class="section-title">Quick-Quiz</h2>
        <div class="quick-quiz-list">
          <button 
            v-for="quiz in quickQuizzes" 
            :key="quiz.id"
            class="quick-quiz-btn"
            @click="goToQuizOverview(quiz.id)"
          >
            <div class="quick-quiz-title">{{ quiz.title }}</div>
            <div class="quick-quiz-desc">{{ quiz.description }}</div>
          </button>
        </div>
      </section>

      <!-- Normale Quizze -->
      <section class="quizzes-section">
        <div class="quizze-title-row">
          <h2 class="section-title">Quizze</h2>
          <button class="plus-btn" @click="goToEditQuiz">
            <IconPlus />
          </button>
        </div>

        <div class="quizzes-list" v-if="quizzes.length > 0">
          <button 
            v-for="quiz in quizzes" 
            :key="quiz.id"
            class="quiz-btn"
            @click="goToQuizOverview(quiz.id)"
          >
            <div class="quiz-btn-header">
              <div class="quiz-title">{{ quiz.title }}</div>
              <div class="quiz-question-count">{{ quiz.questionCount }} Fragen</div>
            </div>
            
            <div class="quiz-rating-row">
              <div class="quiz-stars">
                <div v-for="n in getStars(quiz.rating).full" :key="'full-' + quiz.id + '-' + n">★</div>
                <div v-if="getStars(quiz.rating).half">★</div>
                <div v-for="n in getStars(quiz.rating).empty" :key="'empty-' + quiz.id + '-' + n">☆</div>
              </div>
              <div class="quiz-creator">von {{ quiz.creator }}</div>
            </div>
          </button>
        </div>
        
        <div v-else class="no-quizzes">
          <p>Keine Quizze für dieses Lernset gefunden.</p>
          <p>Erstelle das erste Quiz mit dem Plus-Button.</p>
        </div>
      </section>
    </template>
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

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: var(--color-primary, #1976d2);
}

.error-message {
  background-color: #fee;
  border: 1px solid #fcc;
  color: #d32f2f;
  padding: 16px;
  border-radius: 8px;
  margin: 16px 0;
  text-align: center;
}

.retry-btn {
  background-color: #d32f2f;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  margin-top: 8px;
  cursor: pointer;
}

.no-quizzes {
  background-color: #f5f5f5;
  padding: 24px;
  text-align: center;
  border-radius: 8px;
  color: #666;
}

.spinner {
  border: 4px solid rgba(25, 118, 210, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--color-primary, #1976d2);
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin-bottom: 12px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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