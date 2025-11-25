import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getSelfUser } from '@/services/user'
import apiClient from '@/services/api/client'

export const useUserStore = defineStore('user', () => {
  const id = ref(null)
  const username = ref(null)
  const email = ref(null)
  const role = ref(null)
  const iq_level = ref(0)
  const streak = ref(0)
  const correct_answers = ref(0)
  const wrong_answers = ref(0)
  const solved_quizzes = ref(0)
  const studiengang = ref(null)
  const studiengang_name = ref(null)
  const loaded = ref(false)
  const loading = ref(false)
  const error = ref(null)

  async function loadCurrentUser(force = false) {
    if (loaded.value && !force) return
    loading.value = true
    error.value = null
    try {
      const data = await getSelfUser()
      id.value = data.id || null
      username.value = data.username || null
      email.value = data.email || null
      role.value = data.role || null
      iq_level.value = data.iq_level || 0
      streak.value = data.streak || 0
      correct_answers.value = data.correct_answers || 0
      wrong_answers.value = data.wrong_answers || 0
      solved_quizzes.value = data.solved_quizzes || 0
      studiengang.value = data.studiengang || null
      studiengang_name.value = data.studiengang_name || null
      loaded.value = true
    } catch (e) {
      console.error('Failed to load current user', e)
      error.value = 'Benutzer konnte nicht geladen werden'
      reset()
    } finally {
      loading.value = false
    }
  }

  function reset() {
    id.value = null
    username.value = null
    email.value = null
    role.value = null
    iq_level.value = 0
    streak.value = 0
    correct_answers.value = 0
    wrong_answers.value = 0
    solved_quizzes.value = 0
    studiengang.value = null
    studiengang_name.value = null
    loaded.value = false
    error.value = null
  }

  async function logout() {
    try {
      await apiClient.post('api/accounts/logout/')
    } catch (e) {
      console.error('Logout failed', e)
    }
    reset()
  }

  function isModerator() {
    return role.value === 'MODERATOR'
  }

  function isOwner(name) {
    return !!username.value && username.value === name
  }

  return {
    id, username, email, role, iq_level, streak, correct_answers, wrong_answers, solved_quizzes, studiengang, studiengang_name,
    loaded, loading, error,
    loadCurrentUser, reset, logout, isModerator, isOwner
  }
})
