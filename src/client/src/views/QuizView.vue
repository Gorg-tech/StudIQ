<template>
  <div class="quiz-overview-container">
    <div class="card quiz-card">
      <div class="quiz-header">
        <div>
          <h2>
            {{ quiz.title }}
            <span class="quiz-progress">
              (Frage {{ currentIndex + 1 }} von {{ quiz.questions.length }})
            </span>
          </h2>
          <p class="quiz-description">{{ quiz.description }}</p>
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
          <h3>{{ currentQuestion.question }}</h3>
          <p class="question-type" v-if="currentQuestion.type === 'SINGLE_CHOICE'">Wähle eine Antwort aus.</p>
          <p class="question-type" v-else>Wähle eine oder mehrere Antworten aus.</p>
          <div
            v-for="(answer, index) in currentQuestion.answers"
            :key="index"
            class="answer-row"
            :class="{
              selected: selectedAnswer.includes(answer),
              correct: answered && currentQuestion.correctAnswers.includes(answer),
              incorrect: answered && selectedAnswer.includes(answer) && !currentQuestion.correctAnswers.includes(answer),
              hoverable: !answered && !selectedAnswer.includes(answer)
            }"
            :role="currentQuestion.type === 'SINGLE_CHOICE' ? 'radio' : 'checkbox'"
            :aria-checked="currentQuestion.type === 'SINGLE_CHOICE' ? (selectedSingle === answer).toString() : selectedAnswer.includes(answer).toString()"
            tabindex="0"
            @click="selectAnswer(answer)"
            @keydown.enter="selectAnswer(answer)"
          >
            <span class="answer-text">{{ answer }}</span>
            <div class="checkmark" v-if="selectedAnswer.includes(answer)">✓</div>
          </div>
          <div class="button-row">
            <button class="btn btn-primary" v-if="!answered" @click="checkAnswer" :disabled="selectedAnswer.length === 0">
              Antwort abgeben
            </button>
            <button class="btn btn-secondary" v-if="answered" @click="nextQuestion">
              Weiter
            </button>
          </div>
          <div v-if="answered" class="result-message">
            <span v-if="result" class="user-answer correct">Richtig!</span>
            <span v-else-if="selectedAnswer.some(ans => currentQuestion.correctAnswers.includes(ans))" class="user-answer partial">
              Fast richtig! Die richtigen Antworten sind: {{ currentQuestion.correctAnswers.join(', ') }}
            </span>
            <span v-else class="user-answer incorrect">
              Leider falsch. Die richtigen Antworten sind: {{ currentQuestion.correctAnswers.join(', ') }}
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
import { getQuiz } from '@/services/quizzes'
import Penguin from '@/components/Penguin.vue'

const router = useRouter()
const route = useRoute()
const quizId = ref(route.params.quizId)

const quiz = ref({
  title: '',
  description: '',
  questions: []
})
const loading = ref(true)
const currentIndex = ref(0)
const selectedAnswer = ref([])
const selectedSingle = ref(null)
const answered = ref(false)
const result = ref(null)
const correctCount = ref(0)
const userAnswers = ref([])

const currentQuestion = computed(() => {
  if (!quiz.value.questions.length || currentIndex.value >= quiz.value.questions.length) return null
  const question = quiz.value.questions[currentIndex.value]
  return {
    question: question.text,
    type: question.type,
    answers: question.answer_options.map(opt => opt.text),
    correctAnswers: question.answer_options.filter(opt => opt.is_correct).map(opt => opt.text)
  }
})

const progress = computed(() => {
  if (!quiz.value.questions.length) return 0
  return ((currentIndex.value + 1) / quiz.value.questions.length) * 100
})

onMounted(async () => {
  try {
    const data = await getQuiz(quizId.value)
    quiz.value = data
  } catch (err) {
    console.error('Error loading quiz:', err)
    router.push('/')
  } finally {
    loading.value = false
  }
})

function checkAnswer() {
  if (!currentQuestion.value) return
  
  const selected = selectedAnswer.value
  const correct = currentQuestion.value.correctAnswers
  const isCorrect = selected.length === correct.length && selected.every(ans => correct.includes(ans))
  result.value = isCorrect
  if (isCorrect) correctCount.value++

  userAnswers.value[currentIndex.value] = {
    question: currentQuestion.value.question,
    selected: [...selected],
    correct: [...correct],
    isCorrect
  }
  answered.value = true
}

function nextQuestion() {
  currentIndex.value++
  selectedAnswer.value = []
  selectedSingle.value = null
  answered.value = false
  
  if (currentIndex.value >= quiz.value.questions.length) { // Use quiz.value.questions here too
    localStorage.setItem('quizResults', JSON.stringify(userAnswers.value))
    router.push({
      name: 'quiz-result',
      query: {
        quizId: quizId.value,
        correct: correctCount.value,
        total: quiz.value.questions.length
      }
    })
  }
}

function selectAnswer(answer) {
  if (!answered.value) {
    if (currentQuestion.value.type === 'SINGLE_CHOICE') {
      selectedSingle.value = answer
      selectedAnswer.value = [answer]
    } else {
      const index = selectedAnswer.value.indexOf(answer)
      if (index > -1) {
        selectedAnswer.value.splice(index, 1)
      } else {
        selectedAnswer.value.push(answer)
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
