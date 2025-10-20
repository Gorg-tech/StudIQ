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
import { isAuthenticated } from '@/services/auth.js'

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
      path: '/edit-quiz/:quizId?',
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
      path: '/quiz',
      name: 'quiz',
      component: QuizView,
    },
    { 
      path: '/modul/:moduleId?',
      name: 'modul',
      component: ModulView,
      props: true,  //nicht notwendig, ermöglicht Weitergabe von Parameter automatisch an neue Komonente(statt useRoute())
    },
    { 
      path: '/lernset/:lernsetId?',
      name: 'lernset',
      component: LernsetView,
    },
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

  next()
})

export default router
