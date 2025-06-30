import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useQuizEditStore = defineStore('quizEdit', () => {
  const quizLoaded = ref(false)
  const quizId = ref(null)
  const quizTitle = ref('Mein Quiz')
  const questions = ref([])

  function setQuiz({ id, title, questions: qs }) {
    quizLoaded.value = true
    quizId.value = id || null
    quizTitle.value = title || 'Mein Quiz'
    questions.value = qs ? [...qs] : []
  }

  function resetQuiz() {
    quizLoaded.value = false
    quizId.value = null
    quizTitle.value = ''
    questions.value = []
  }

  function updateQuestion(id, data) {
    const q = questions.value.find(q => q.id === id)
    if (q) Object.assign(q, data)
  }

  function addQuestion(question) {
    questions.value.push(question)
  }

  function removeQuestion(id) {
    questions.value = questions.value.filter(q => q.id !== id)
  }

  function getQuestion(id) {
    return questions.value.find(q => q.id === id)
  }

  return {
    quizId, quizTitle, questions, quizLoaded,
    setQuiz, resetQuiz, updateQuestion, addQuestion, removeQuestion, getQuestion
  }
})