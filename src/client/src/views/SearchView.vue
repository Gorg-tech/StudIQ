<template>
  <div class="search-view">
    <h2 class="search-heading">Quiz suchen</h2>

    <!-- Search bar -->
    <input
      v-model="searchQuery"
      placeholder="Gib einen Titel ein..."
      class="search-input"
    />

    <!-- Filter buttons -->
    <div class="filter-buttons">
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'Alle' }"
        @click="activeFilter = 'Alle'"
      >
        Alle
      </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'Quiz' }"
        @click="activeFilter = 'Quiz'"
      >
        Quiz
      </button>
    </div>

    <!-- Fetch quizzes button -->
    <button class="btn btn-primary" @click="fetchQuizzes">Quiz abrufen</button>

    <!-- Display quizzes -->
    <div v-if="loading">Lade Quiz-Daten...</div>
    <div v-if="error">{{ error }}</div>
    <div v-if="filteredQuizzes.length">
      <div
        v-for="quiz in filteredQuizzes"
        :key="quiz.id"
        class="quiz-item"
      >
        <h3>{{ quiz.title }}</h3>
        <p>{{ quiz.questions }} Fragen – {{ quiz.duration }} Min</p>
      </div>
    </div>
    <p v-else>Keine passenden Einträge gefunden.</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import apiClient from '@/services/api/client'

const searchQuery = ref('')
const activeFilter = ref('Alle')
const quizzes = ref([]) // Store quizzes fetched from the server
const loading = ref(false)
const error = ref(null)

// Fetch quizzes from the server
async function fetchQuizzes() {
  loading.value = true
  error.value = null
  try {
    const response = await apiClient.get('/api/quizzes/')
    console.log('API resoponse', response)
    quizzes.value = response // Update the quizzes list
  } catch (err) {
    error.value = 'Fehler beim Abrufen der Quiz-Daten.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Filter quizzes based on search query and active filter
const filteredQuizzes = computed(() =>
  quizzes.value.filter(q =>
    q.title.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
    (activeFilter.value === 'Alle' || q.type === activeFilter.value)
  )
)
</script>

<style scoped>
.search-view {
  padding: 20px;
}

.search-heading {
  color: var(--color-accent);
  margin-bottom: 12px;
}

.search-input {
  width: 100%;
  padding: 10px;
  border: 2px solid var(--color-primary);
  border-radius: 6px;
  font-size: 1rem;
  margin-bottom: 16px;
  background-color: white;
  color: var(--color-text);
}

.search-input:focus {
  box-shadow: 0 0 5px var(--color-primary);
  border-color: var(--color-primary);
}

.filter-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.quiz-item {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-bottom: 12px;
  background-color: white;
}
</style>
