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


router.beforeEach((to, from, next) => {
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
    const store = useQuizEditStore()
    // Check if a quizId or lernsetId was provided OR if the store already has a lernsetId
    const hasQuiz = !!(to.params && to.params.quizId !== undefined && to.params.quizId !== '')
    const hasLernset = !!((to.params && to.params.lernsetId !== undefined && to.params.lernsetId !== '') || store.lernsetId)
    if (!hasQuiz && !hasLernset) {
      if (from && from.name) {
        next(false)
      } else {
        next({ name: 'home' })
      }
      return
    }
  }

  next()
})

export default router
