<template>
  <div class="search-view">
    <h2 class="search-heading">Suche</h2>

    <!-- Search bar -->
    <input v-model="searchQuery" placeholder="Suche nach Studiengang, Lernset, Modul oder Quiz ..." class="search-input" />

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
      :class="{ 'btn-primary': activeFilter === 'Studiengang' }"
      @click="activeFilter = 'Studiengang'"
    >
      Studiengang
    </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'Modul' }"
        @click="activeFilter = 'Modul'"
      >
        Modul
      </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'Lernset' }"
        @click="activeFilter = 'Lernset'"
      >
        Lernset
      </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'Quiz' }"
        @click="activeFilter = 'Quiz'"
      >
        Quiz
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      Quizze werden geladen...
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Filtered list -->
    <div v-else-if="filteredQuizzes.length" class="quiz-list">
      <div 
        v-for="quiz in filteredQuizzes" 
        :key="quiz.id" 
        class="quiz-item"
      >
        <div class="quiz-header">
          <h3>{{ quiz.title }}</h3>
          <span class="quiz-type">{{ quiz.type || 'Quiz' }}</span>
        </div>
        <p class="quiz-stats">
          {{ quiz.questions?.length || 0 }} Fragen – {{ quiz.avg_time_spent || 0 }} Min
        </p>
        <p v-if="quiz.description" class="quiz-description">
          {{ quiz.description }}
        </p>
      </div>
    </div>
    <p v-else class="no-results">Keine passenden Einträge gefunden.</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getQuizzes } from '@/services/quizzes'

const searchQuery = ref('')
const activeFilter = ref('Alle')
const quizzes = ref([])
const loading = ref(true)
const error = ref(null)

// Load quizzes when component mounts
onMounted(async () => {
  try {
    loading.value = true
    quizzes.value = await getQuizzes('e3b639d8-b316-4282-a149-4744407d2d90')
    loading.value = false
  } catch (err) {
    console.error('Failed to load quizzes:', err)
    error.value = 'Fehler beim Laden der Quizze. Bitte versuche es später erneut.'
    loading.value = false
  }
})

const filteredQuizzes = computed(() =>
  quizzes.value.filter(
    (q) =>
      q.title.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
      (
        activeFilter.value === 'Alle' ||
        q.type === activeFilter.value ||
        (activeFilter.value === 'Studiengang' && q.study_program)
      )
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

.loading-container {
  text-align: center;
  color: var(--color-primary);
  margin: 20px 0;
}

.error-message {
  color: var(--color-danger);
  margin: 20px 0;
}

.quiz-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.quiz-item {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-bottom: 12px;
  background-color: white;
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.quiz-type {
  background-color: var(--color-light);
  color: var(--color-dark);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.875rem;
}

.quiz-stats {
  font-size: 0.875rem;
  color: var(--color-muted);
  margin-bottom: 8px;
}

.quiz-description {
  font-size: 0.875rem;
  color: var(--color-text);
}

.no-results {
  text-align: center;
  color: var(--color-muted);
  margin: 20px 0;
}
</style>
