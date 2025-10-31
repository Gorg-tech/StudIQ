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
        :class="{ 'btn-primary': activeFilter === 'alle' }"
        @click="activeFilter = 'alle'; fetchFilteredQuizzes()"
      >
        Alle
      </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'studiengang' }"
        @click="activeFilter = 'studiengang'; fetchFilteredQuizzes()"
      >
        Studiengang
      </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'modul' }"
        @click="activeFilter = 'modul'; fetchFilteredQuizzes()"
      >
        Modul
      </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'lernset' }"
        @click="activeFilter = 'lernset'; fetchFilteredQuizzes()"
      >
        Lernset
      </button>
      <button
        class="btn"
        :class="{ 'btn-primary': activeFilter === 'quiz' }"
        @click="activeFilter = 'quiz'; fetchFilteredQuizzes()"
      >
        Quiz
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      <span class="spinner"></span>
      Quizze werden geladen...
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Results state -->
    <template v-else>
      <!-- Filtered list when we have results -->
      <div v-if="filteredResults.length" class="quiz-list">
        <div
          v-for="item in filteredResults"
          :key="item.id"
          class="quiz-item"
          :class="`type-${item.type.toLowerCase()}`"
          @click="navigateToItem(item)"
          style="cursor: pointer;"
        >
          <div class="quiz-header">
            <h3>
              <!-- Emojis entfernt -->
              {{ item.title }}
            </h3>
            <span class="item-type">{{ item.type }}</span>
          </div>

          <div v-if="item.type === 'Quiz'" class="quiz-stats">
            {{ item.questions?.length || 0 }} Fragen – {{ item.avg_time_spent || 0 }} Min
          </div>
          <div v-else-if="item.type === 'Modul'" class="quiz-stats">
            Semester: {{ item.semester }} – Credits: {{ item.credits }} – Modul-ID: {{ item.modulId }}
          </div>
          <div v-else-if="item.type === 'Studiengang'" class="quiz-stats">
            ID: {{ item.id }}
          </div>

          <!-- Im Template, z.B. unter dem Titel -->
          <div v-if="item.type === 'Quiz' && item.lernset_title" class="quiz-lernset">
            Lernset: {{ item.lernset_title }}
          </div>

          <p v-if="item.description" class="quiz-description">
            {{ item.description }}
          </p>
        </div>
      </div>

      <!-- No results message -->
      <p v-else class="no-results">Keine passenden Einträge gefunden.</p>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { getSearch } from '@/services/quizzes';

const router = useRouter();
const searchQuery = ref('');
const activeFilter = ref('alle');
const results = ref({});
const loading = ref(false);
const error = ref(null);

// Mapping von Button-Label zu Server-Filter
const filterMap = {
  alle: null,
  studiengang: 'studiengaenge',
  modul: 'modules',
  lernset: 'lernsets',
  quiz: 'quizzes',
};

// Fetch search results
async function fetchFilteredQuizzes() {
  loading.value = true;
  error.value = null;
  try {
    const filter = filterMap[activeFilter.value.toLowerCase()];

    results.value = await getSearch({
      searchQuery: searchQuery.value,
      filter
    });
  } catch (err) {
    error.value = 'Fehler beim Abrufen der Suchergebnisse.';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

// Return all filtered results based on the active filter type
const filteredResults = computed(() => {
  const filter = activeFilter.value.toLowerCase();

  if (filter === 'alle') {
    // Flatten all result types into a single array
    const allResults = [
      ...(results.value.quizzes || []).map(item => ({ ...item, type: 'Quiz' })),
      ...(results.value.lernsets || []).map(item => ({ ...item, type: 'Lernset' })),
      ...(results.value.modules || []).map(item => ({ ...item, type: 'Modul', title: item.name, description: item.description })),
      ...(results.value.studiengaenge || []).map(item => ({ ...item, type: 'Studiengang', title: item.name })),
    ];

    return allResults;
  }

  // Otherwise, return just the requested type
  const filterKey = filterMap[filter];
  if (!filterKey || !results.value[filterKey]) {
    return [];
  }

  // Map fields to a consistent format
  if (filterKey === 'studiengaenge') {
    return results.value[filterKey].map(item => ({
      ...item,
      type: 'Studiengang',
      title: item.name
    }));
  } else if (filterKey === 'modules') {
    return results.value[filterKey].map(item => ({
      ...item,
      type: 'Modul',
      title: item.name
    }));
  } else if (filterKey === 'lernsets') {
    return results.value[filterKey].map(item => ({
      ...item,
      type: 'Lernset'
    }));
  } else {
    return results.value[filterKey].map(item => ({
      ...item,
      type: 'Quiz'
    }));
  }
});

// Navigation function for quiz items
// Api implementation with name instead of path
function navigateToItem(item) {
  if (item.type === 'Quiz') {
    router.push({ name: 'quiz-overview', params: { quizId: item.id } }); 
  } else if (item.type === 'Lernset') {
    router.push({ name: 'lernset', params: { lernsetId: item.id } });
  } else if (item.type === 'Modul') {
    router.push({ path: `/modul/${item.modulId}` }); 
  } else if (item.type === 'Studiengang') {
    router.push({ name: 'studiengang-overview', params: { studiengangId: item.id } }); //TODO
  }
}

// Watch for changes in searchQuery and fetch results for each typed letter
watch(searchQuery, () => {
  fetchFilteredQuizzes();
});

onMounted(() => {
  fetchFilteredQuizzes();
});
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
  background-color: var(--card-bg);
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
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  row-gap: 6px;

}

.quiz-item {
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  margin-bottom: 12px;
  background-color: var(--card-bg);
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.item-type {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.type-quiz .item-type {
  background-color: rgba(33, 150, 243, 0.2);
  color: #1565c0;
  border: 1px solid rgba(33, 150, 243, 0.3);
}
.type-lernset .item-type {
  background-color: rgba(156, 39, 176, 0.2);
  color: #6a1b9a;
  border: 1px solid rgba(156, 39, 176, 0.3);
}
.type-modul .item-type {
  background-color: rgba(76, 175, 80, 0.2);
  color: #1b5e20;
  border: 1px solid rgba(76, 175, 80, 0.3);
}
.type-studiengang .item-type {
  background-color: rgba(255, 152, 0, 0.2);
  color: #e65100;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

.dark .type-quiz .item-type {
  color: #64b5f6;
}
.dark .type-lernset .item-type {
  color: #ba68c8;
}
.dark .type-modul .item-type {
  color: #81c784;
}
.dark .type-studiengang .item-type {
  color: #ffb74d;
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

.spinner {
  display: inline-block;
  width: 22px;
  height: 22px;
  border: 3px solid var(--color-primary);
  border-top: 3px solid transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 10px;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 900px) {
  .quiz-list {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 600px) {
  .quiz-list {
    grid-template-columns: 1fr;
  }
}

.quiz-lernset {
  font-size: 0.85rem;
  color: var(--color-muted);
  margin-bottom: 6px;
}
</style>
