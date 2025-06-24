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
      path: '/quiz-overview',
      name: 'quiz-overview',
      component: QuizOverviewView,
    },
    {
      path: '/quiz-result',
      name: 'quiz-result',
      component: QuizResultView,
    }
  ],
})


const isAuthenticated = () => {
  // Hier kommt Authentifizierungslogik hin :)
  // z.B. Token aus localStorage/sessionStorage cookies... prüfen
  const token = localStorage.getItem('authToken')
  return !!token
}

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')

  // if route requires autorization, but token doesn't here - redirect to /login
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

/*

 Erstmal auskommentiert, da Authentifizierung noch nicht implementiert ist

// Router guard for authentication
router.beforeEach((to, from, next) => {
  // Login and Register routes are always accessible
  if (to.name === 'login' || to.name === 'register') {
    next()
    return
  }

  // For all other routes, check if authenticated
  if (!isAuthenticated()) {
    next({ name: 'login' })
    return
  }

  next()
})

*/

export default router
