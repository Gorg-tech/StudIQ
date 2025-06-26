<template>
  <div class="search-view">
    <h2 class="search-heading">Suche</h2>

    <!-- Search bar -->
    <input
      v-model="searchQuery"
      placeholder="Suche nach Studiengang, Lernset, Modul oder Quiz ..."
      class="search-input"
    />

    <!-- Filter buttons -->
    <div class="filter-buttons">
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'Alle' }"
        @click="activeFilter = 'Alle'; fetchFilteredQuizzes()"
      >
        Alle
      </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'Studiengang' }"
        @click="activeFilter = 'Studiengang'; fetchFilteredQuizzes()"
      >
        Studiengang
      </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'Modul' }"
        @click="activeFilter = 'Modul'; fetchFilteredQuizzes()"
      >
        Modul
      </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'Lernset' }"
        @click="activeFilter = 'Lernset'; fetchFilteredQuizzes()"
      >
        Lernset
      </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'Quiz' }"
        @click="activeFilter = 'Quiz'; fetchFilteredQuizzes()"
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
        @click="$router.push({ name: 'quiz-overview', params: { quizId: quiz.id } })"
        style="cursor: pointer;"
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
import { ref, computed } from 'vue';
import { getSearch } from '@/services/quizzes';

const searchQuery = ref('');
const activeFilter = ref('Alle');
const quizzes = ref([]);
const loading = ref(false);
const error = ref(null);

// Fetch quizzes based on active filter and search query
async function fetchFilteredQuizzes() {
  loading.value = true;
  error.value = null;

  try {
    const params = { searchTerm: searchQuery.value };

    // Dynamically add filter parameters based on activeFilter
    if (activeFilter.value === 'Studiengang') {
      params.studiengangID = 1; // Replace with actual Studiengang ID logic
    } else if (activeFilter.value === 'Modul') {
      params.modulID = 1; // Replace with actual Modul ID logic
    } else if (activeFilter.value === 'Lernset') {
      params.lernsetID = 1; // Replace with actual Lernset ID logic
    } else if (activeFilter.value === 'Quiz') {
      params.quizID = 1; // Replace with actual Quiz ID logic
    }

    // Fetch filtered quizzes
    quizzes.value = await getSearch(params);
  } catch (err) {
    error.value = 'Fehler beim Abrufen der Quiz-Daten.';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

// Filtered quizzes based on search query
const filteredQuizzes = computed(() =>
  quizzes.value.filter((quiz) =>
    quiz.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);
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
