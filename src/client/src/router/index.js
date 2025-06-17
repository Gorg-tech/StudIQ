import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import EditQuizView from '@/views/EditQuizView.vue'
import EditQuestionView from '@/views/EditQuestionView.vue'
import QuizOverviewView from '@/views/QuizOverviewView.vue'
import QuizResultView from '@/views/QuizResultView.vue'


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
      component: QuizOverviewView,
    },
    {
      path: '/quiz-result',
      name: 'quiz-result',
      component: QuizResultView,
    }
  ],
})

export default router
