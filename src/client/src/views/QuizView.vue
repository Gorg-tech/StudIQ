<template>
  <div class="quiz-overview-container">
    <div class="card quiz-card">
      <div class="quiz-header">
        <div>
          <h2>
            {{ quizTitle }}
            <span class="quiz-progress">
              (Frage {{ currentIndex + 1 }} von {{ totalQuestions }})
            </span>
          </h2>
          <p class="quiz-description">{{ quizDescription }}</p>
        </div>
        <div class="quiz-card-penguin">
          <Penguin style="width: 80px; height: 80px;" />
        </div>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progress + '%' }"></div>
      </div>
      <div class="quiz-content">
        <div v-if="loading" class="loading-state">
          Quiz wird geladen...
        </div>
        <div v-else-if="!currentQuestion">
          <div class="error-message">
            Keine Fragen im Quiz vorhanden.
          </div>
        </div>
        <div v-else class="question-block">
          <h3>{{ currentQuestion.text }}</h3>
          <p class="question-type" v-if="currentQuestion.type === 'SINGLE_CHOICE'">Wähle eine Antwort aus.</p>
          <p class="question-type" v-else>Wähle eine oder mehrere Antworten aus.</p>
          <div
            v-for="option in currentQuestion.answer_options"
            :key="option.id"
            class="answer-row"
            :class="{
              selected: selectedAnswerIds.includes(option.id),
              correct: answered && lastCorrectAnswerIds.includes(option.id),
              incorrect: answered && selectedAnswerIds.includes(option.id) && !lastCorrectAnswerIds.includes(option.id),
              hoverable: !answered && !selectedAnswerIds.includes(option.id)
            }"
            :role="currentQuestion.type === 'SINGLE_CHOICE' ? 'radio' : 'checkbox'"
            :aria-checked="selectedAnswerIds.includes(option.id).toString()"
            tabindex="0"
            @click="selectAnswer(option.id)"
            @keydown.enter="selectAnswer(option.id)"
          >
            <span class="answer-text">{{ option.text }}</span>
            <div class="checkmark" v-if="selectedAnswerIds.includes(option.id)">✓</div>
          </div>
          <div class="button-row">
            <button class="btn btn-primary" v-if="!answered" @click="checkAnswer" :disabled="selectedAnswerIds.length === 0 || submitting">
              {{ submitting ? 'Wird verarbeitet...' : 'Antwort abgeben' }}
            </button>
            <button class="btn btn-secondary" v-if="answered" @click="nextQuestion" :disabled="submitting">
              {{ isLastQuestion ? 'Beenden' : 'Weiter' }}
            </button>
          </div>
          <div v-if="answered" class="result-message">
            <span v-if="lastIsCorrect" class="user-answer correct">Richtig!</span>
            <span v-else-if="selectedAnswerIds.some(id => lastCorrectAnswerIds.includes(id))" class="user-answer partial">
              Fast richtig! Die richtigen Antworten sind: {{ getCorrectAnswerTexts() }}
            </span>
            <span v-else class="user-answer incorrect">
              Leider falsch. Die richtigen Antworten sind: {{ getCorrectAnswerTexts() }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { startQuiz, submitAnswer } from '@/services/quizzes'
import Penguin from '@/components/Penguin.vue'

const router = useRouter()
const route = useRoute()
const quizId = ref(route.params.quizId)

const loading = ref(true)
const submitting = ref(false)
const currentIndex = ref(0)
const sessionId = ref(null)
const currentQuestion = ref(null)
const selectedAnswerIds = ref([])
const answered = ref(false)
const lastIsCorrect = ref(null)
const lastCorrectAnswerIds = ref([])
const quizTitle = ref('')
const quizDescription = ref('')
const totalQuestions = ref(0)

const progress = computed(() => {
  if (!totalQuestions.value) return 0
  return ((currentIndex.value + 1) / totalQuestions.value) * 100
})

const isLastQuestion = computed(() => {
  return currentIndex.value === totalQuestions.value - 1
})

onMounted(async () => {
  try {
    const data = await startQuiz(quizId.value)
    
    sessionId.value = data.session_id
    quizTitle.value = data.title || ''
    quizDescription.value = data.description || ''
    totalQuestions.value = data.total_questions
    currentQuestion.value = data.first_question
  } catch (err) {
    console.error('Error loading quiz:', err)
    router.push('/')
  } finally {
    loading.value = false
  }
})

function getCorrectAnswerTexts() {
  if (!currentQuestion.value) return ''
  return currentQuestion.value.answer_options
    .filter(opt => lastCorrectAnswerIds.value.includes(opt.id))
    .map(opt => opt.text)
    .join(', ')
}

async function checkAnswer() {
  if (!currentQuestion.value || submitting.value) return
  
  submitting.value = true
  try {
    const response = await submitAnswer(quizId.value, {
      question_id: currentQuestion.value.id,
      selected_option_ids: selectedAnswerIds.value
    })

    lastIsCorrect.value = response.is_correct
    lastCorrectAnswerIds.value = response.correct_answers
    answered.value = true
  } catch (err) {
    console.error('Error submitting answer:', err)
    alert('Fehler beim Absenden der Antwort')
  } finally {
    submitting.value = false
  }
}

async function nextQuestion() {
  if (isLastQuestion.value) {
    // Quiz beenden
    submitting.value = true
    try {
      router.push({
        name: 'quiz-result',
        query: {
          quizId: quizId.value
        }
      })
    } catch (err) {
      console.error('Error completing quiz:', err)
      alert('Fehler beim Beenden des Quiz')
    } finally {
      submitting.value = false
    }
  } else {
    // Nächste Frage laden
    currentIndex.value++
    selectedAnswerIds.value = []
    answered.value = false
    lastIsCorrect.value = null
    lastCorrectAnswerIds.value = []
  }
}

function selectAnswer(answerId) {
  if (!answered.value) {
    if (currentQuestion.value.type === 'SINGLE_CHOICE') {
      selectedAnswerIds.value = [answerId]
    } else {
      const index = selectedAnswerIds.value.indexOf(answerId)
      if (index > -1) {
        selectedAnswerIds.value.splice(index, 1)
      } else {
        selectedAnswerIds.value.push(answerId)
      }
    }
  }
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
  background-color: var(--card-bg);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px var(--card-shadow);
  width: 100%;
}

.quiz-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.quiz-header h2 {
  color: var(--color-accent);
  margin: 0;
  font-size: 1.8rem;
  display: flex;
  align-items: center;
  gap: 16px;
}

.quiz-description {
  font-size: 1rem;
  color: var(--color-text);
  margin-top: 4px;
}

.quiz-progress {
  font-size: 1rem;
  color: var(--color-muted);
  margin-left: 16px;
}

.quiz-card-penguin {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  min-width: 100px;
  height: 100%;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: var(--color-border);
  border-radius: 4px;
  margin-bottom: 16px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--color-primary);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.quiz-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.question-block {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.question-type {
  font-size: 0.9rem;
  color: var(--color-muted);
  margin-bottom: 16px;
  font-style: italic;
}

.answer-row {
  width: 100%;
  margin-bottom: 12px;
  padding: 12px 16px;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--card-bg);
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.answer-text {
  flex: 1;
  cursor: pointer;
}

.checkmark {
  color: var(--color-primary);
  font-weight: bold;
  font-size: 1.2rem;
}

.button-row {
  display: flex;
  gap: 12px;
  margin-top: 18px;
}

.result-message {
  margin-top: 18px;
  font-size: 1.1rem;
}

.user-answer.correct {
  color: #4caf50;
  font-weight: 600;
}

.user-answer.incorrect {
  color: #f44336;
  font-weight: 600;
}

.user-answer.partial {
  color: #ff9800;
  font-weight: 600;
}

.answer-row.selected {
  background: var(--color-selected);
  border-color: var(--color-primary);
}
.answer-row.correct {
  background: var(--color-correct);
  border-color: #4caf50;
}
.answer-row.incorrect {
  background: var(--color-incorrect);
  border-color: #f44336;
}

.answer-row.hoverable:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-primary);
  cursor: pointer;
}

.loading-state {
  font-size: 1.2rem;
  color: var(--color-muted);
  text-align: center;
  padding: 24px 0;
}

.error-message {
  font-size: 1.2rem;
  color: #f44336;
  text-align: center;
  padding: 24px 0;
}

.hoverable {
  cursor: pointer;
  transition: background 0.3s;
}

.hoverable:hover {
  background: rgba(255, 255, 255, 0.1);
}
</style>
