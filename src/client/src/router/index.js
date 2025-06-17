import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import EditQuizView from '@/views/EditQuizView.vue'
import EditQuestionView from '@/views/EditQuestionView.vue'
import QuizOverview from '@/views/QuizOverview.vue'
import QuizresultatView from '@/views/QuizresultatView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
      path: '/edit-quiz',
      name: 'edit-quiz',
      component: EditQuizView,
    },
    {
      path: '/edit-question',
      name: 'edit-question',
      component: EditQuestionView,
    },
    {
      path: '/quiz-overview',
      name: 'quiz-overview',
      component: QuizOverview,
    },
    {
      path: '/quiz-result',
      name: 'quiz-result',
      component: QuizresultatView,
    }
  ],
})

export default router
