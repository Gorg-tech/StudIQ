import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useQuizEditStore = defineStore('quizEdit', () => {
  const quizLoaded = ref(false)
  const quizId = ref(null)
  const quizTitle = ref('Mein Quiz')
  const lernsetId = ref(null)
  const questions = ref([])

  function setQuiz({ id, title, questions: qs, lernset }) {
    quizLoaded.value = true
    quizId.value = id || null
    quizTitle.value = title || 'Mein Quiz'
    lernsetId.value = lernset || lernsetId.value || null
    questions.value = qs ? [...qs] : []
  }

  function setLernset(id) {
    lernsetId.value = id
  }

  function resetQuiz() {
    quizLoaded.value = false
    quizId.value = null
    quizTitle.value = ''
    lernsetId.value = null
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
    quizId, quizTitle, questions, quizLoaded, lernsetId,
    setQuiz, resetQuiz, updateQuestion, addQuestion, setLernset, removeQuestion, getQuestion
  }
})

export const QUESTION_TYPES = [
  { api: 'SINGLE_CHOICE', label: 'Single Choice' },
  { api: 'MULTIPLE_CHOICE', label: 'Multiple Choice' }
]

export function getLabelFromApi(apiValue) {
  return QUESTION_TYPES.find(q => q.api === apiValue)?.label || apiValue
}