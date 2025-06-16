<!-- src/views/SearchView.vue -->
<template>
  <div class="search-view">
    <h2>Quiz suchen</h2>
    <input v-model="searchQuery" placeholder="Titel eingeben..." class="search-input" />
    
    <div v-if="filteredQuizzes.length">
      <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="quiz-item">
        <h3>{{ quiz.title }}</h3>
        <p>{{ quiz.questions }} Fragen, {{ quiz.duration }} Minuten</p>
      </div>
    </div>
    <p v-else>Keine Quizze gefunden.</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')

// Testdaten – später durch echte Daten ersetzen oder per Prop übergeben
const quizzes = ref([
  { id: 1, title: 'Laufzeitberechnung', questions: 10, duration: 5 },
  { id: 2, title: 'Analysis', questions: 15, duration: 7 },
  { id: 3, title: 'C - Programmierung', questions: 33, duration: 13 },
])

const filteredQuizzes = computed(() =>
  quizzes.value.filter(q =>
    q.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)
</script>

<style scoped>
.search-view {
  padding: 20px;
}

.search-input {
  border: 2px solid var(--color-primary);
  border-radius: 4px;
  padding: 10px;
  font-size: 1rem;
  outline: none;
  width: 100%;
  background-color: white;
  color: var(--color-text);
}

.search-input:focus {
  box-shadow: 0 0 5px var(--color-primary);
  border-color: var(--color-primary);
}


.quiz-item {
  padding: 12px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.quiz-item:focus {
  box-shadow: 0 0 5px var(--color-primary);
  border-color: var(--color-primary);
}
</style>

