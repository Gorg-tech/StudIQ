<script setup>
import { ref, onMounted } from 'vue'
import { store } from '@/stores/app.js'
import { fetchLeaderboard } from '@/services/leaderboard'
import IconFlame from '@/components/icons/IconFlame.vue'

// Configuration: how many top users to show, and how many around the current user
const TOP_COUNT = 3
const AROUND_COUNT = 1

const leaderboard = ref([])
const isLoading = ref(true)
const error = ref(null)
const hasMoreAfter = ref(false)
const hasMoreBefore = ref(false)
const selfUser = ref(null)

const TAB_ALL = 'all'
const TAB_STUDIENGANG = 'studiengang'
const TAB_FRIENDS = 'friends'
const tabs = [
  { key: TAB_ALL, label: 'Alle' },
  { key: TAB_STUDIENGANG, label: 'Studiengang' },
  { key: TAB_FRIENDS, label: 'Freunde' }
]
const activeTab = ref(TAB_ALL)

function selectTab(tabKey) {
  if (activeTab.value === tabKey) return
  activeTab.value = tabKey
  if (tabKey === TAB_ALL) {
    loadLeaderboard('all')
  } else if (tabKey === TAB_STUDIENGANG) {
    loadLeaderboard('studiengang')
  } else if (tabKey === TAB_FRIENDS) {
    loadLeaderboard('friends')
  }
}

// When button pressed, call API for new leaderboard-list
async function loadLeaderboard(category) {
  isLoading.value = true;
  try {
      const user_data = await store.getUser()
      selfUser.value = user_data
      const data = await fetchLeaderboard(TOP_COUNT, AROUND_COUNT, category)
      if (!data) {
      throw new Error('Keine Daten vom Server erhalten')
      }
      leaderboard.value = data.users || []
      hasMoreAfter.value = data.has_more_after
      hasMoreBefore.value = data.has_more_before
  } catch (err) {
      console.error('Leaderboard Error:', err)
      error.value = `Fehler beim Laden des Leaderboards: ${err.message}`
  } finally {
      isLoading.value = false
  }
}

onMounted(async () => {
  loadLeaderboard('all');
})
</script>

<template>
  <div class="leaderboard-view">

    <header class="leaderboard-header">
      <h1>Leaderboard</h1>
      <p class="subtitle">Top Studenten der StudIQ Community</p>
      <div class="leaderboard-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          :class="['leaderboard-tab', { active: activeTab === tab.key }]"
          @click="selectTab(tab.key)"
        >
          {{ tab.label }}
        </button>
      </div>
    </header>

    <main class="leaderboard-content">
      <div v-if="isLoading" class="loading">
        Lade Leaderboard...
      </div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

     <div v-else class="leaderboard-list">
     <!-- Top N -->
     <div v-if="selfUser && leaderboard.length > 0">
        <div v-for="(user, index) in leaderboard.slice(0, TOP_COUNT)"
        :key="user.username + '-top-' + index"
        class="leaderboard-item"
        :class="{
          'top-three': index < TOP_COUNT,
          'first-place': index === 0,
          'second-place': index === 1,
          'third-place': index === 2,
          'current-user': selfUser.id == user.id
        }">
            <div class="rank">#{{ user.rank }}</div>
            <div class="user-info">
                <div class="username">{{ user.username }}</div>
                <div class="stats">
                  <span class="iq-score">
                      {{ user.iq_score }} IQ Punkte
                  </span>
                  <span class="streak">
                      <IconFlame class="streak-icon" />
                      {{ user.streak }} Tage Streak
                  </span>
                  <span class="total-quizzes">
                      {{ user.solved_quizzes }} Quizze abgeschlossen
                  </span>
                </div>
            </div>
            </div>
        </div>

        <!-- Ellipsis if there's a gap between top and around users -->
        <div v-if="hasMoreBefore" class="rank-separator">
          •••
        </div>

        <!-- Users around current user (appended after top) -->
    <div v-if="selfUser && leaderboard.length > 0">
     <div v-for="(user, idx) in leaderboard.slice(TOP_COUNT)"
       :key="user.username + '-around-' + idx"
       class="leaderboard-item"
       :class="{'current-user': selfUser.id == user.id}">
          <div class="rank">#{{ user.rank }}</div>
          <div class="user-info">
            <div class="username">{{ user.username }}</div>
            <div class="stats">
              <span class="iq-score">
                {{ user.iq_score }} IQ Punkte
              </span>
              <span class="streak">
                <IconFlame class="streak-icon" />
                {{ user.streak }} Tage Streak
              </span>
              <span class="total-quizzes">
                {{ user.solved_quizzes }} Quizze abgeschlossen
              </span>
            </div>
          </div>
        </div>
        </div>

        <!-- trailing ellipsis (only if there are more users after the displayed ones) -->
        <div v-if="hasMoreAfter" class="rank-separator">•••</div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.leaderboard-tabs {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 18px;
}
.leaderboard-tab {
  background: none;
  border: none;
  font-size: 1.08rem;
  font-weight: 600;
  color: var(--color-text);
  margin-top: 1em;
  padding: 8px 60px;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.leaderboard-tab.active {
  background: var(--color-primary);
  color: var(--color-bg);
}
.leaderboard-tab.active:hover {
  background: var(--color-primary);
  color: var(--color-bg);
}
.leaderboard-tab:hover {
  background: color-mix(in oklab, var(--color-bg) 90%, #888888 10%);
  color: var(--color-primary);
}
.leaderboard-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
}

.leaderboard-header {
  text-align: center;
  margin-bottom: 32px;
}

.leaderboard-header h1 {
  font-size: 2.5rem;
  color: var(--color-primary);
  margin-bottom: 8px;
}

.subtitle {
  color: var(--color-muted);
  font-size: 1.1rem;
}

.leaderboard-list {
  display: flex;
  flex-direction: column;
}

.leaderboard-item {
  display: flex;
  align-items: center;
  padding: 20px;
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 8px;
}

.rank {
  font-size: 1.5rem;
  font-weight: bold;
  min-width: 48px;
  margin-right: 1em;
  text-align: center;
  color: var(--color-primary);
}

.user-info {
  flex-grow: 1;
}

.username {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 4px;
}

.stats {
  display: flex;
  gap: 16px;
  color: var(--color-muted);
  font-size: 0.9rem;
}

.streak {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--color-accent);
}

.streak-icon {
  width: 16px;
  height: 16px;
}

.top-three {
  /* Same styling as regular items */
}

.first-place, .second-place, .third-place {
  /* No special styling */
}

.loading, .error {
  text-align: center;
  padding: 32px;
  color: var(--color-muted);
}

.error {
  color: var(--color-red);
}

.toggle-view {
  margin-top: 16px;
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background-color: var(--color-primary);
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.toggle-view:hover {
  background-color: var(--color-accent);
}

.rank-separator {
  text-align: center;
  color: var(--color-muted);
  padding: 8px 0;
  font-size: 1.2rem;
  letter-spacing: 2px;
}

.current-user {
  border: 2px solid var(--color-accent);
  background: var(--card-bg);
}

@media (max-width: 600px) {
  .leaderboard-view {
    padding: 12px;
  }

  .leaderboard-header h1 {
    font-size: 1.8rem;
  }

  .subtitle {
    font-size: 0.95rem;
  }

  .leaderboard-tabs {
    gap: 8px;
  }

  .leaderboard-tab {
    font-size: 0.9rem;
    padding: 8px 16px;
  }

  .leaderboard-item {
    padding: 12px;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .rank {
    font-size: 1.2rem;
    margin-right: 0;
    margin-bottom: 8px;
  }

  .username {
    font-size: 1.05rem;
  }

  .stats {
    flex-direction: column;
    gap: 6px;
    font-size: 0.85rem;
  }
}
</style>
