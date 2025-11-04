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

onMounted(async () => {

    try {
        const user_data = await store.getUser()
        selfUser.value = user_data
        const data = await fetchLeaderboard(TOP_COUNT, AROUND_COUNT)
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
})
</script>

<template>
  <div class="leaderboard-view">
    <header class="leaderboard-header">
      <h1>Leaderboard</h1>
      <p class="subtitle">Top Streaks der StudIQ Community</p>
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
        :class="{'top-three': index < TOP_COUNT, 'current-user': selfUser.id == user.id}">
            <div class="rank">#{{ user.rank }}</div>
            <div class="user-info">
                <div class="username">{{ user.username }}</div>
                <div class="stats">
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
  gap: 16px;
}

.leaderboard-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.rank {
  font-size: 1.5rem;
  font-weight: bold;
  min-width: 48px;
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
  background: linear-gradient(135deg, var(--color-primary-light) 0%, var(--card-bg) 100%);
  border: 2px solid var(--color-primary-light);
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
    padding: 16px;
  }
  
  .stats {
    flex-direction: column;
    gap: 4px;
  }
  
  .leaderboard-item {
    padding: 12px;
  }
}
</style>