import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import EditQuizView from '@/views/EditQuizView.vue'
import EditQuestionView from '@/views/EditQuestionView.vue'
import QuizOverviewView from '@/views/QuizOverviewView.vue'
import QuizResultView from '@/views/QuizResultView.vue'
import LoginView from '@/views/LoginView.vue'
import RegistrationView from '@/views/RegistrationView.vue'
import QuizView from '@/views/QuizView.vue'
import ModulView from '@/views/ModulView.vue'
import LernsetView from '@/views/LernsetView.vue'
import HomeViewSettings from '@/views/HomeViewSettings.vue'
import { isAuthenticated } from '@/services/auth.js'
import { getQuiz } from '@/services/quizzes'
import { useUserStore } from '@/stores/user'
import { useQuizEditStore } from '@/stores/editQuiz'
import StudiengangView from '@/views/StudiengangView.vue'
import LeaderboardView from '@/views/LeaderboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegistrationView,
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/edit-quiz/:quizId?/:lernsetId?',
      name: 'edit-quiz',
      component: EditQuizView,
    },
    {
      path: '/edit-question/:questionId?',
      name: 'edit-question',
      component: EditQuestionView,
    },
    {
      path: '/quiz-overview/:quizId',
      name: 'quiz-overview',
      component: QuizOverviewView,
    },
    {
      path: '/quiz-result',
      name: 'quiz-result',
      component: QuizResultView,
    },
    { 
      path: '/quiz/:quizId',
      name: 'quiz',
      component: QuizView,
    },
    { 
      path: '/modul/:modulId',
      name: 'modul',
      component: ModulView,
    },
    { 
      path: '/lernset/:lernsetId',
      name: 'lernset',
      component: LernsetView,
    },
    {
      path: '/settings',
      name: 'settings',
      component: HomeViewSettings,
    },
    {
      path: '/studiengang/:studiengangId',
      name: 'studiengang-overview',
      component: StudiengangView,
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: LeaderboardView,
    }
  ],
})


router.beforeEach(async (to, from, next) => {
  // Login and Register routes are always accessible
  if (to.name === 'login' || to.name === 'register') {
    next()
    return
  }

  // For all other routes, check if authenticated
  if (!isAuthenticated.value) {
    next({ name: 'login' })
    return
  }

  // Prevent accessing edit-quiz without quizId OR lernsetId
  if (to.name === 'edit-quiz') {
    const quizEditStore = useQuizEditStore()
    const userStore = useUserStore()
    await userStore.loadCurrentUser()
    const hasQuizParam = !!(to.params && to.params.quizId)
    const hasLernsetParam = !!(to.params && to.params.lernsetId)
    const hasStoredLernset = !!quizEditStore.lernsetId
    if (!hasQuizParam && !hasLernsetParam && !hasStoredLernset) {
      // No context for creating/editing
      next(from && from.name ? false : { name: 'home' })
      return
    }
    // If editing existing quiz, verify permission
    if (hasQuizParam) {
      try {
        const quiz = await getQuiz(to.params.quizId)
        const creator = quiz.created_by || quiz.createdBy || quiz.creator_username || null
        const isOwner = creator && userStore.username && creator === userStore.username
        const isMod = userStore.isModerator()
        if (!isOwner && !isMod) {
          // Deny access; redirect to quiz overview (read-only)
          next({ name: 'quiz-overview', params: { quizId: to.params.quizId } })
          return
        }
        // Store creator for later UI checks if not already set
        if (!quizEditStore.quizCreator) quizEditStore.quizCreator = creator
      } catch (e) {
        // If quiz fetch fails, block navigation
        next(from && from.name ? false : { name: 'home' })
        return
      }
    }
  }

  next()
})

export default router
