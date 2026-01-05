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
      <button class="btn btn-create" @click="openDialog">
        Quiz erstellen
      </button>
    </div>

    <!-- Help Text -->
    <div v-if="activeFilter === 'quiz'" class="help-text">
      <p>Du möchtest ein eigenes Quiz erstellen? Navigiere zu einem Lernset und klicke dort auf das Plus-Symbol (+).</p>
    </div>
    <div v-if="activeFilter === 'lernset'" class="help-text">
      <p>Du möchtest ein neues Lernset anlegen? Navigiere zu einem Modul und wähle dort "Lernset erstellen".</p>
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

          <div v-if="item.type === 'Quiz'" class="quiz-details">
            <div class="stats-row">
              <span title="Fragen">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                {{ item.questions?.length || 0 }} Fragen
              </span>
              <span title="Dauer">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                {{ item.avg_time_spent || 0 }} Min
              </span>
            </div>
          </div>

          <div v-else-if="item.type === 'Lernset'" class="quiz-details">
            <div class="stats-row">
              <span title="Quizze">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                {{ item.quiz_count || 0 }} Quizze
              </span>
            </div>
          </div>

          <div v-else-if="item.type === 'Modul'" class="quiz-details modul-details">
            <div class="stats-row" v-if="item.dozent_name">
              <span class="dozent-wrapper" :title="item.dozent_name">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                <span class="text-truncate">{{ item.dozent_name }}</span>
              </span>
            </div>
            <div class="stats-row">
              <span title="Credits">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline></svg>
                {{ item.credits }} CP
              </span>
              <span :title="item.turnus" v-if="item.turnus">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                {{ formatTurnus(item.turnus) }}
              </span>
              <span title="Lernsets">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                {{ item.lernset_count || 0 }} Sets
              </span>
            </div>
          </div>

          <div v-else-if="item.type === 'Studiengang'" class="quiz-details">
            <div class="stats-row">
              <span title="Module" v-if="item.module">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                {{ item.module.length }} Module
              </span>
            </div>
          </div>

          <p v-if="item.description" class="quiz-description">
            {{ item.description }}
          </p>

          <div class="card-footer">
            <div v-if="item.type === 'Quiz'" class="hierarchy-info">
              <span v-if="item.modul_name" class="hierarchy-item" title="Modul">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                {{ item.modul_name }}
              </span>
              <span v-if="item.modul_name && item.lernset_title" class="hierarchy-separator">›</span>
              <span v-if="item.lernset_title" class="hierarchy-item" title="Lernset">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                {{ item.lernset_title }}
              </span>
            </div>
            
            <div v-else-if="item.type === 'Lernset' && item.modul" class="hierarchy-info">
              <span class="hierarchy-item" title="Modul">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                {{ item.modul.name }}
              </span>
            </div>

            <div v-else-if="item.type === 'Modul' || item.type === 'Studiengang'">
              <span class="id-badge" :title="item.type + '-ID'">#{{ item.modulId || item.id }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- No results message -->
      <p v-else class="no-results">Keine passenden Einträge gefunden.</p>
    </template>

    <!-- Create Quiz Dialog -->
    <div v-if="showDialog" class="dialog-overlay" @click.self="closeDialog">
      <div class="dialog-content">
        <button class="close-btn" @click="closeDialog">×</button>
        
        <div v-if="dialogStep === 1">
          <h3>Wähle ein Modul</h3>
          <p class="dialog-desc">Zu welchem Modul gehört dein Quiz? Wähle unten das passende Modul aus.</p>
          <input 
            v-model="dialogSearchQuery" 
            @input="searchModulesForDialog" 
            placeholder="Modul suchen..." 
            class="dialog-input"
            aria-label="Modul suchen"
          />

          <div class="dialog-list">
            <div v-if="dialogModulesLoading" class="dialog-loading">
              <div class="dialog-spinner" aria-hidden="true"></div>
            </div>

            <div v-else>
              <div v-if="!dialogModules || dialogModules.length === 0" class="dialog-empty">
                Keine Module gefunden.
              </div>
              <div 
                v-for="mod in dialogModules" 
                :key="mod.id" 
                class="dialog-item" 
                @click="selectModule(mod)"
              >
                {{ mod.name }}
              </div>
            </div>
          </div>
        </div>

        <div v-if="dialogStep === 2">
          <h3>Wähle ein Lernset</h3>
          <p class="dialog-desc">Zu welchem Lernset soll dein Quiz gehören? Wähle ein Lernset aus oder erstelle zuerst eines im Modul.</p>
          <button class="back-btn" @click="dialogStep = 1">Zurück</button>

          <div class="dialog-list">
            <div v-if="dialogLoading" class="dialog-loading">
              <div class="dialog-spinner" aria-hidden="true"></div>
            </div>

            <div v-else>
              <div v-if="!dialogLernsets || dialogLernsets.length === 0" class="dialog-empty">
                <p>Keine Lernsets gefunden.</p>
                <router-link 
                  :to="`/modul/${selectedModule.modulId}`" 
                  class="dialog-link"
                  @click="closeDialog"
                >
                  Zum Modul gehen und Lernset erstellen
                </router-link>
              </div>

              <div v-else>
                <div 
                  v-for="ls in dialogLernsets" 
                  :key="ls.id" 
                  class="dialog-item" 
                  @click="selectLernset(ls)"
                >
                  {{ ls.title }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { getSearch } from '@/services/quizzes';
import { getModul } from '@/services/modules';
import { useSearchStore } from '@/stores/search';
import { storeToRefs } from 'pinia';

const router = useRouter();
const searchStore = useSearchStore();
const { searchQuery, activeFilter, results } = storeToRefs(searchStore);

const loading = ref(false);
const error = ref(null);

// Dialog State
const showDialog = ref(false);
const dialogStep = ref(1);
const dialogSearchQuery = ref('');
const dialogModules = ref([]);
const dialogModulesLoading = ref(false);
const selectedModule = ref(null);
const dialogLernsets = ref([]);
const dialogLoading = ref(false);

// Mapping von Button-Label zu Server-Filter
const filterMap = {
  alle: null,
  studiengang: 'studiengaenge',
  modul: 'modules',
  lernset: 'lernsets',
  quiz: 'quizzes',
};

// Simple debounce utility
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// Fetch search results with caching
async function fetchFilteredQuizzes() {
  const currentFilter = activeFilter.value;
  const currentQuery = searchQuery.value.trim();
  const cacheKey = `${currentFilter}:${currentQuery}`;

  const hasCache = searchStore.hasCache(cacheKey);
  if (hasCache) {
    results.value = searchStore.getCachedResults(cacheKey);
  } else {
    loading.value = true;
  }

  error.value = null;
  
  try {
    const filter = filterMap[currentFilter.toLowerCase()];
    const data = await getSearch({
      searchQuery: currentQuery,
      filter
    });
    
    // Update cache in store
    searchStore.saveToCache(cacheKey, data);
    
    // Only update results if this is still the current search
    if (cacheKey === `${activeFilter.value}:${searchQuery.value.trim()}`) {
      results.value = data;
    }
  } catch (err) {
    if (!hasCache) {
      error.value = 'Fehler beim Abrufen der Suchergebnisse.';
    }
    console.error(err);
  } finally {
    loading.value = false;
  }
}

// Debounced version of fetch for search input
const debouncedFetch = debounce(fetchFilteredQuizzes, 250);

// Dialog Functions
function openDialog() {
  showDialog.value = true;
  dialogStep.value = 1;
  dialogSearchQuery.value = '';
  dialogModules.value = [];
  selectedModule.value = null;
  dialogLernsets.value = [];
  searchModulesForDialog();
}

function closeDialog() {
  showDialog.value = false;
}

// Debounced search for dialog
const searchModulesForDialog = debounce(async () => {
  dialogModulesLoading.value = true;
  try {
    const res = await getSearch({
      searchQuery: dialogSearchQuery.value,
      filter: 'modules'
    });
    dialogModules.value = res.modules || [];
  } catch (err) {
    console.error(err);
    dialogModules.value = [];
  } finally {
    dialogModulesLoading.value = false;
  }
}, 300);

async function selectModule(mod) {
  selectedModule.value = mod;
  dialogStep.value = 2;
  dialogLoading.value = true;
  try {
    const modulData = await getModul(mod.modulId);
    dialogLernsets.value = modulData.lernsets || [];
  } catch (err) {
    console.error(err);
    dialogLernsets.value = [];
  } finally {
    dialogLoading.value = false;
  }
}

function selectLernset(ls) {
  closeDialog();
  router.push({ name: 'edit-quiz', params: { lernsetId: ls.id } });
}

// Helper to normalize result items
function normalizeItem(item, type) {
  const base = { ...item, type };
  if (type === 'Modul') {
    base.title = item.name;
    base.description = item.description;
  } else if (type === 'Studiengang') {
    base.title = item.name;
  }
  return base;
}

function formatTurnus(turnus) {
  if (!turnus) return '';
  return turnus
    .replace(/Sommersemester/gi, 'SS')
    .replace(/Wintersemester/gi, 'WS');
}

// Return all filtered results based on the active filter type
const filteredResults = computed(() => {
  const filter = activeFilter.value.toLowerCase();
  const res = results.value;

  if (filter === 'alle') {
    return [
      ...(res.quizzes || []).map(i => normalizeItem(i, 'Quiz')),
      ...(res.lernsets || []).map(i => normalizeItem(i, 'Lernset')),
      ...(res.modules || []).map(i => normalizeItem(i, 'Modul')),
      ...(res.studiengaenge || []).map(i => normalizeItem(i, 'Studiengang')),
    ];
  }

  const filterKey = filterMap[filter];
  if (!filterKey || !res[filterKey]) return [];

  // Map the specific type
  const typeMap = {
    'studiengaenge': 'Studiengang',
    'modules': 'Modul',
    'lernsets': 'Lernset',
    'quizzes': 'Quiz'
  };
  
  return res[filterKey].map(item => normalizeItem(item, typeMap[filterKey]));
});

// Navigation function for quiz items
function navigateToItem(item) {
  const routes = {
    'Quiz': { name: 'quiz-overview', params: { quizId: item.id } },
    'Lernset': { name: 'lernset', params: { lernsetId: item.id } },
    'Modul': { path: `/modul/${item.modulId}` },
    'Studiengang': { name: 'studiengang-overview', params: { studiengangId: item.id } }
  };
  
  const route = routes[item.type];
  if (route) router.push(route);
}

// Watch for changes in searchQuery
watch(searchQuery, () => {
  debouncedFetch();
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

.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
  display: inline-block;
  vertical-align: bottom;
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
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  width: 100%;
}

.quiz-item {
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  margin-bottom: 12px;
  background-color: var(--card-bg);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.item-type {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
  background-color: var(--type-bg);
  color: var(--type-color);
  border: 1px solid var(--type-border);
}

.type-quiz {
  --type-bg: rgba(33, 150, 243, 0.2);
  --type-color: #1565c0;
  --type-border: rgba(33, 150, 243, 0.3);
}
.type-lernset {
  --type-bg: rgba(156, 39, 176, 0.2);
  --type-color: #6a1b9a;
  --type-border: rgba(156, 39, 176, 0.3);
}
.type-modul {
  --type-bg: rgba(76, 175, 80, 0.2);
  --type-color: #1b5e20;
  --type-border: rgba(76, 175, 80, 0.3);
}
.type-studiengang {
  --type-bg: rgba(255, 152, 0, 0.2);
  --type-color: #e65100;
  --type-border: rgba(255, 152, 0, 0.3);
}

.dark .type-quiz { --type-color: #64b5f6; }
.dark .type-lernset { --type-color: #ba68c8; }
.dark .type-modul { --type-color: #81c784; }
.dark .type-studiengang { --type-color: #ffb74d; }

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

.quiz-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 12px;
}

.card-footer {
  margin-top: auto;
  display: flex;
  justify-content: flex-end;
  padding-top: 8px;
}

.hierarchy-info {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  font-size: 0.85rem;
  color: var(--color-muted);
  justify-content: flex-end;
}

.hierarchy-item {
  display: flex;
  align-items: center;
  gap: 4px;
  background-color: var(--color-bg-light);
  padding: 2px 8px;
  border-radius: 4px;
}

.hierarchy-separator {
  color: var(--color-muted);
  font-weight: bold;
}

.stats-row {
  display: flex;
  gap: 12px;
  font-size: 0.85rem;
  color: var(--color-text);
  align-items: center;
}

.stats-row > span {
  display: flex;
  align-items: center;
  gap: 4px;
  line-height: 1;
}

.id-badge {
  font-size: 0.75rem;
  color: var(--color-muted);
  background: var(--color-bg-light);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
}

.icon {
  opacity: 0.7;
}

.quiz-stats strong {
  font-weight: 700;
  color: var(--color-text); /* optional */
}

/* New Styles */
.btn-create {
  margin-left: auto;
  background-color: var(--color-accent);
  color: white;
  border-color: var(--color-accent);
}

.btn-create:hover {
  filter: brightness(0.95);
}

.help-text {
  background-color: var(--color-bg-light);
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid var(--color-info);
  color: var(--color-text);
}

/* Dialog Styles */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-content {
  background-color: var(--card-bg);
  padding: 24px;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  position: relative;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text);
}

.dialog-input {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  margin-bottom: 16px;
  background-color: var(--color-bg);
  color: var(--color-text);
}

.dialog-list {
  overflow-y: auto;
  max-height: 300px;
  height: 260px; /* fixed dialog list height to keep visual consistency */
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.dialog-spinner {
  width: 30px;
  height: 30px;
  border: 3px solid var(--color-primary);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 18px auto;
}

.dialog-item {
  padding: 12px;
  background-color: var(--color-bg-light);
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
  color: var(--color-text);
}

.dialog-item:hover {
  background-color: var(--color-bg-hover);
}

.back-btn {
  background: none;
  border: none;
  color: var(--color-primary);
  cursor: pointer;
  margin-bottom: 12px;
  padding: 0;
  text-align: left;
  font-size: 0.9rem;
}

.back-btn:hover {
  text-decoration: underline;
}

.dialog-loading {
  text-align: center;
  padding: 20px;
  color: var(--color-muted);
}

.dialog-desc {
  margin: 6px 0 12px 0;
  color: var(--color-muted);
  font-size: 0.95rem;
}

.dialog-empty {
  text-align: center;
  padding: 20px;
  color: var(--color-muted);
}

.dialog-link {
  color: var(--color-primary);
  text-decoration: none;
  display: block;
  margin-top: 8px;
}

.dialog-link:hover {
  text-decoration: underline;
}
</style>
