import { reactive } from 'vue'

export const store = reactive({
  user: null,
  quizStats: {
    completed: 0,
    correctAnswers: 0,
    totalQuestions: 0
  },
  
  // Methods
  setUser(userData) {
    this.user = userData
  },
  
  updateStats(completed, correct, total) {
    this.quizStats.completed += completed
    this.quizStats.correctAnswers += correct
    this.quizStats.totalQuestions += total
  }
})