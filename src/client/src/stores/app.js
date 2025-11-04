import { reactive } from 'vue'
import { getSelfUser } from '@/services/user'

export const store = reactive({
  user: null,
  quizStats: {
    completed: 0,
    correctAnswers: 0,
    totalQuestions: 0
  },

  async getUser() {
    if (this.user) {
      return this.user
    } else {
      return await getSelfUser()
    }
  },
  
  updateStats(completed, correct, total) {
    this.quizStats.completed += completed
    this.quizStats.correctAnswers += correct
    this.quizStats.totalQuestions += total
  }
})