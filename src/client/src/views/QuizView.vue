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
          <div
            v-for="(answer, index) in currentQuestion.answers"
            :key="index"
            class="answer-row"
            :class="{
              selected: answered && selectedAnswer === answer,
              correct: answered && answer === currentQuestion.correctAnswer,
              incorrect: answered && selectedAnswer === answer && answer !== currentQuestion.correctAnswer
            }"
          >
            <label>
              <input
                type="radio"
                :value="answer"
                v-model="selectedAnswer"
                name="answer"
                :disabled="answered"
              >
              {{ answer }}
            </label>
          </div>
          <div class="button-row">
            <button class="btn btn-primary" v-if="!answered" @click="checkAnswer" :disabled="selectedAnswer === null">
              Antwort abgeben
            </button>
            <button class="btn btn-secondary" v-if="answered" @click="nextQuestion">
              Weiter
            </button>
          </div>
          <div v-if="answered" class="result-message">
            <span v-if="result" class="user-answer correct">Richtig!</span>
            <span v-else class="user-answer incorrect">
              Leider falsch. Die richtige Antwort ist: {{ currentQuestion.correctAnswer }}
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
const selectedAnswer = ref(null)
const answered = ref(false)
const result = ref(null)
const correctCount = ref(0)
const userAnswers = ref([])

const currentQuestion = computed(() => {
  if (!quiz.value.questions.length || currentIndex.value >= quiz.value.questions.length) return null
  const question = quiz.value.questions[currentIndex.value]
  return {
    question: question.text,
    answers: question.answer_options.map(opt => opt.text),
    correctAnswer: question.answer_options.find(opt => opt.is_correct)?.text
  }
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
  
  const isCorrect = selectedAnswer.value === currentQuestion.value.correctAnswer
  result.value = isCorrect
  if (isCorrect) correctCount.value++

  userAnswers.value[currentIndex.value] = {
    question: currentQuestion.value.question,
    selected: selectedAnswer.value,
    correct: currentQuestion.value.correctAnswer,
    isCorrect
  }
  answered.value = true
}

function nextQuestion() {
  currentIndex.value++
  selectedAnswer.value = null
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

.answer-row {
  width: 100%;
  margin-bottom: 12px;
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

.answer-row.selected {
  background: var(--color-selected);
}
.answer-row.correct {
  background: var(--color-correct);
}
.answer-row.incorrect {
  background: var(--color-incorrect);
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
</style>
