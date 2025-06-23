<template>
  <div class="search-view p-4 md:p-6 lg:p-8">
    <!-- Suchfeld -->
    <input
      v-model="searchTerm"
      type="text"
      placeholder="Suche nach Quiz‑Titel …"
      class="border-2 border-orange-400 focus:border-orange-500 focus:ring-2 focus:ring-orange-500 rounded-lg p-3 w-full mb-6 text-base md:text-lg shadow-sm"
    />

    <!-- Lade‑ & Fehlermeldungen -->
    <div v-if="loading" class="text-center py-12 text-lg">Lade …</div>
    <div v-else-if="error" class="text-red-600 text-center text-lg">{{ error }}</div>

    <!-- Kein Ergebnis -->
    <div v-if="filteredQuizzes.length === 0 && !loading" class="text-center text-gray-500 text-base md:text-lg">
      Keine passenden Quizzes gefunden.
    </div>

    <!-- Ergebnisliste -->
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="quiz in filteredQuizzes"
        :key="quiz.id"
        class="border border-orange-200 rounded-xl p-6 shadow hover:shadow-lg hover:bg-orange-50 transition"
      >
        <h3 class="font-semibold text-xl mb-2 text-orange-700">{{ quiz.title }}</h3>
        <p class="text-base text-gray-600 mb-4 line-clamp-3">{{ quiz.description }}</p>

        <router-link
          :to="{ name: 'quiz-overview', query: { id: quiz.id } }"
          class="inline-block bg-orange-600 hover:bg-orange-700 text-white text-sm font-medium px-4 py-2 rounded-md transition"
        >
          Öffnen
        </router-link>
      </div>
    </div>
  </div>
</template>


<script>
import api from '@/services/api/client';

export default {
  name: 'SearchView',
  data() {
    return {
      searchTerm: '',
      quizzes: [],
      loading: false,
      error: null,
    };
  },
  computed: {
    filteredQuizzes() {
      if (!this.searchTerm.trim()) {
        return this.quizzes;
      }
      const term = this.searchTerm.toLowerCase();
      return this.quizzes.filter((q) =>
        q.title.toLowerCase().includes(term) ||
        (q.description && q.description.toLowerCase().includes(term))
      );
    },
  },
  methods: {
    async fetchQuizzes() {
      this.loading = true;
      this.error = null;
      try {
        // Endpoint wird vom DRF‑Router bereitgestellt → /quizzes/
        this.quizzes = await api.get('quizzes/');
      } catch (err) {
        this.error = 'Fehler beim Laden der Quizzes.';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.fetchQuizzes();
  },
};
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
