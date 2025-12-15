<template>
  <div class="profile">
    <!-- Header -->
    <header class="app-header">
      <div class="logo-container">
        <h1><LogoStudIQ /></h1>
        <p class="tagline">Dein Begleiter für die Prüfungsvorbereitung</p>
      </div>

      <button class="settings-btn" @click="router.push('/settings/')" aria-label="Einstellungen">
        <IconSettings />
      </button>
    </header>

    <!-- Friends Popup -->
    <div class="friends-popup-backdrop" v-if="showFriends" @click.self="showFriends = false">
      <div class="friends-popup">
        <div v-if="friendRequests.length" class="friend-requests-section">
          <h4>Freundschaftsanfragen</h4>
          <ul class="friend-requests-list">
            <li v-for="req in friendRequests" :key="req.from_user" class="friend-request-row">
              <span>{{ req.from_user }}</span>
              <button class="friend-accept-btn" @click="acceptFriendRequestAction(req.from_user)">✔️</button>
              <button class="friend-decline-btn" @click="declineFriendRequestAction(req.from_user)">❌</button>
            </li>
          </ul>
        </div>
        <div v-if="friends.length" class="friends-section">
          <h3>Freundesliste</h3>
          <div class="friends-table-wrapper">
            <table class="friends-table">
              <thead>
                <tr>
                  <th>Benutzername</th>
                  <th>Streak</th>
                  <th>IQ</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="friend in friends" :key="friend.username">
                  <td>{{ friend.username }}</td>
                  <td>{{ friend.streak ?? '-' }}</td>
                  <td>{{ friend.iq_score ?? '-' }}</td>
                  <td>
                    <button class="friend-delete-btn" @click="friendToDelete = friend">
                      <IconTrashcan />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <button class="add-friend-btn" @click="showAddFriend = true">Freund hinzufügen</button>
        <button class="close-btn" @click="showFriends = false">Schließen</button>
      </div>
    </div>

    <!-- Add Friend Popup -->
    <div class="friends-popup-backdrop" v-if="showAddFriend" @click.self="closeAddFriend">
      <div class="friends-popup">
        <h3>Freund hinzufügen</h3>
        <form @submit.prevent="submitAddFriend">
          <input
            v-model="addFriendUsername"
            class="add-friend-input"
            type="text"
            :disabled="addFriendLoading"
            placeholder="Benutzername eingeben"
            autocomplete="off"
            required
          />
          <div v-if="addFriendError" class="add-friend-error">{{ addFriendError }}</div>
          <div class="add-friend-btn-row">
            <button type="submit" class="add-friend-send-btn" :disabled="addFriendLoading">
              {{ addFriendLoading ? 'Senden...' : 'Schicken' }}
            </button>
            <button type="button" class="add-friend-cancel-btn" @click="closeAddFriend" :disabled="addFriendLoading">Abbrechen</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Friend Confirmation Popup -->
    <div class="friends-popup-backdrop" v-if="friendToDelete != null" @click.self="closeDeleteFriend">
      <div class="friends-popup">
        <h3>Freund entfernen</h3>
        <p>Möchtest du <strong>{{ friendToDelete?.username }}</strong> wirklich aus deiner Freundesliste entfernen?</p>
        <div class="add-friend-btn-row">
          <button class="add-friend-send-btn" @click="deleteFriend(friendToDelete)">Entfernen</button>
          <button class="add-friend-cancel-btn" @click="closeDeleteFriend">Abbrechen</button>
        </div>
      </div>
    </div>

    <!-- Profile etc. -->
    <div v-if="loading">Lädt...</div>
    <div v-else-if="error">Fehler: {{ error.message }}</div>
    <div v-if="!loading">

      <!-- Top Profile Section-->
      <div class="profile-top">
        <div class="profile-left">
          <div class="profile-info">
            <h2>{{ user.username }}</h2>
            <p>Platz #{{ leaderboardPosition }}</p>
          </div>

          <button class="friends-btn" @click="showFriends = true">
            👥
            <span v-if="friendRequests.length" class="friend-requests-badge">{{ friendRequests.length }}</span>
          </button>

          <!-- Level Bar -->
          <div class="level-bar-container">
            <div class="level-circle">{{ userLevel }}</div>
            <div class="level-bar-wrapper">
              <div class="level-bar">
                <div class="level-fill" :style="{ width: levelProgress + '%' }"></div>
              </div>
              <div class="level-percentage">{{ levelProgress }}%</div>
            </div>
          </div>
        </div>

        <div class="profile-right">
          <div class="penguin-bubble top-aligned">
            <div class="bubble">{{ penguinSpeech }}</div>
            <Penguin :clap="streakCount >= 3" />
          </div>
        </div>
      </div>

      <!-- Streak Calendar -->
      <div class="streak-card full-width">
        <div class="week-row">
          <div class="day-box" v-for="(day, index) in currentWeekStreak" :key="index">
            <IconFlame v-if="day.learned" />
            <IconFlame v-else class="inactive" />
            <div class="day-label">{{ day.label }}</div>
          </div>
        </div>
        <div class="streak-count">
          Aktuelle Serie: <strong>{{ streakCount }} Tage</strong><br />
          Beste Serie: <strong>{{ longestStreak }} Tage</strong>
        </div>
      </div>

      <!-- Recent Quizzes -->
      <div class="suggested-quizzes">
        <h3>Zuletzt bearbeitete Quizze</h3>
        <div class="quiz-suggestions-row">
          <div v-for="(quiz, index) in recentQuizzes" :key="index" class="quiz-suggestion-item">
            <div class="quiz-suggestion-icon" :style="{ backgroundColor: '#2196f3' + '1A' }">
              <IconCode />
            </div>
            <div class="quiz-suggestion-content">
              <h4>{{ quiz.title }}</h4>
              <p class="quiz-meta">{{ quiz.score }}/{{ quiz.total }} - {{ quiz.date }}</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSelfUserStreaks, getSelfUserStats } from '@/services/user.js'
import { getFriends, sendOrAcceptFriendRequest, declineFriendRequest, getFriendRequests} from '@/services/friends.js'
import { store } from '@/stores/app.js'

import LogoStudIQ from '@/components/LogoStudIQ.vue'
import Penguin from '@/components/Penguin.vue'
import IconFlame from '@/components/icons/IconFlame.vue'
import IconSettings from '@/components/icons/IconSettings.vue'
import IconCode from '@/components/icons/IconCode.vue'
import IconTrashcan from '@/components/icons/IconTrashcan.vue'

const router = useRouter()

const user = ref(null)
const loading = ref(true)
const error = ref(null)

const leaderboardPosition = ref(12)
const penguinSpeech = ref('Super gemacht! Weiter so 🐧')

const userLevel = ref(3)
const levelProgress = ref(60)

const currentWeekStreak = ref([])
const streakCount = ref(0)
const longestStreak = ref(0)


const showFriends = ref(false)
const showAddFriend = ref(false)
const addFriendUsername = ref('')
const addFriendError = ref('')
const addFriendLoading = ref(false)
const friends = ref([])
const friendRequests = ref([])
const friendToDelete = ref(null)

function loadFriends() {
  getFriends().then(fetchedFriends => {
    friends.value = fetchedFriends
  }).catch(err => {
    console.error('Error loading friends:', err)
  })
}

function loadFriendRequests() {
  getFriendRequests().then(requests => {
    friendRequests.value = requests
  }).catch(err => {
    console.error('Error loading friend requests:', err)
  })
}

function closeAddFriend() {
  showAddFriend.value = false
  addFriendUsername.value = ''
  addFriendError.value = ''
}

function closeDeleteFriend() {
  friendToDelete.value = null
}

function deleteFriend(friend) {
  alert(`Freund ${friend.username} entfernen (Backend noch nicht implementiert)`);
  closeDeleteFriend()
}

async function acceptFriendRequestAction(username) {
  try {
    await sendOrAcceptFriendRequest(username)
    loadFriends()
    loadFriendRequests()
  } catch (e) {
    alert(`Fehler beim Akzeptieren der Freundschaftsanfrage: ${e.message || 'Unbekannter Fehler.'}`)
  }
}

async function declineFriendRequestAction(username) {
  try {
    await declineFriendRequest(username)
    loadFriendRequests()
  } catch (e) {
    alert(`Fehler beim Ablehnen der Freundschaftsanfrage: ${e.message || 'Unbekannter Fehler.'}`)
  }
}

async function submitAddFriend() {
  addFriendError.value = ''
  addFriendLoading.value = true
  try {
    const username = addFriendUsername.value.trim()
    const res = await sendOrAcceptFriendRequest(username)
    closeAddFriend()
    showFriends.value = true
    if(res.status === 200) {
      // Accepted existing request
      alert(`Du bist jetzt mit ${username} befreundet!`)
      loadFriends()
    } else {
      // Sent new request
      alert(`Freundschaftsanfrage an ${username} gesendet!`)
    }
  } catch (e) {
    if (e && e.data && e.data.error) {
      addFriendError.value = e.data.error
    } else {
      addFriendError.value = 'Unbekannter Fehler.'
    }
  } finally {
    addFriendLoading.value = false
  }
}

const recentQuizzes = ref([
  { title: 'Analysis', date: '2025-02-20', score: 8, total: 10 },
  { title: 'Programmierung', date: '2025-02-18', score: 7, total: 10 },
  { title: 'BWL Grundlagen', date: '2025-02-16', score: 9, total: 10 },
])

onMounted(async () => {
  try {
    loadFriends()
    loadFriendRequests()
    user.value = await store.getUser()
    const [stats, streaks] = await Promise.all([getSelfUserStats(), getSelfUserStreaks()])

    leaderboardPosition.value = stats.rank
    streakCount.value = streaks.streak
    longestStreak.value = streaks.longest_streak

    const days = streaks.days || []
    const today = new Date()
    const weekDays = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa']

    const currentWeek = []
    for (let i = 0; i < 7; i++) {
      const day = new Date(today)
      day.setDate(today.getDate() - (6 - i))
      const iso = day.toISOString().split('T')[0]
      currentWeek.push({
        label: weekDays[day.getDay()],
        learned: days.includes(iso),
      })
    }
    currentWeekStreak.value = currentWeek
  } catch (err) {
    error.value = `Fehler beim Laden des Profils: ${err.message}`
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.profile { display: flex; flex-direction: column; gap: 24px; max-width: 800px; margin: 0 auto; }

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.friends-btn {
  margin-right: 12px;
  color: var(--color-text);
  background: color-mix(in oklab, var(--color-bg) 70%, #888888 30%);
  border: none;
  padding: 6px 10px;
  border-radius: 8px;
  cursor: pointer;
}

.friends-popup-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.friends-popup {
  background: var(--color-bg);
  padding: 20px;
  border-radius: 14px;
  width: 320px;
  max-width: 90%;
  box-shadow: 0 4px 14px rgba(0,0,0,0.45);
}


.add-friend-btn {
  width: 100%;
  background: var(--color-primary);
  color: var(--text-color);
  padding: 10px 0;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.2s;
}

.add-friend-btn:hover {
  opacity: 0.9;
}

.friend-requests-section h4,
.friends-section h3 {
  font-size: 1.05rem;
  font-weight: 700;
  text-decoration: underline;
  margin: 0 0 8px 0;
}

.friend-requests-list {
  padding-left: 12px;
  margin-bottom: 12px;
}

.friend-request-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
}

.friend-accept-btn, .friend-decline-btn {
  padding: 6px 8px;
  border-radius: 8px;
  min-width: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  color: var(--color-text);
}
.friend-accept-btn { background: var(--color-green); }
.friend-decline-btn { background: var(--color-red); }
.friend-accept-btn:hover, .friend-decline-btn:hover { opacity: 0.9; }

.friends-table-wrapper { display: flex; justify-content: center; margin-bottom: 8px; }
.friends-table { width: 100%; max-width: 460px; border-collapse: collapse; margin: 0 auto; }
.friends-table th, .friends-table td { padding: 10px 14px; text-align: center; }
.friends-table th { background: var(--color-primary); color: var(--color-on-primary, #fff); font-weight: 700; }
.friends-table td { vertical-align: middle; }
.friends-table tr:nth-child(even) { background: color-mix(in oklab, var(--color-bg) 92%, #888 8%); }

.add-friend-btn { margin-top: 10px; }

.friend-delete-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 6px;
  border-radius: 8px;
}
.friend-delete-btn svg { width: 1.1rem; height: 1.1rem; color: var(--color-red); }
.friend-delete-btn:hover { background: color-mix(in oklab, var(--color-red) 12%, transparent); }

.add-friend-input {
  width: 100%;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid var(--color-primary);
  margin-bottom: 8px;
  font-size: 1rem;
  background: var(--color-bg);
  color: var(--color-text);
  box-sizing: border-box;
}

.add-friend-error {
  color: var(--color-red);
  font-size: 0.95rem;
  margin-bottom: 8px;
  min-height: 1.2em;
}

.add-friend-btn-row {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.add-friend-send-btn {
  flex: 1;
  background: var(--color-primary);
  color: var(--color-text);
  border: none;
  border-radius: 8px;
  padding: 8px 0;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.add-friend-send-btn:hover {
  opacity: 0.9;
}

.add-friend-cancel-btn {
  flex: 1;
  background: var(--color-bg);
  color: var(--color-text);
  border: 1px solid var(--color-primary);
  border-radius: 8px;
  padding: 8px 0;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.add-friend-cancel-btn:hover {
  background: color-mix(in oklab, var(--color-primary) 10%, transparent);
  color: var(--color-text);
}


.friends-list {
  list-style: none;
  padding: 0;
  margin: 16px 0;
}

.friends-list li {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
}

.close-btn {
  width: 100%;
  margin-top: 12px;
  padding: 10px;
  background: var(--color-secondary);
  color: var(--color-text);
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 0.9;
}

.profile {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 800px;
  margin: 0 auto;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.settings-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  padding-top: 8px;
  margin-left: auto;
  display: flex;
  align-items: center;
  color: var(--color-primary);
  transition: color 0.2s;
}
.settings-btn:hover {
  color: var(--color-accent);
}

.settings-btn svg {
  width: 2.2rem;
  height: 2.2rem;
}

.profile-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}

/* Left Side */
.profile-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

/* Right Side */
.profile-right {
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
}

/* Profile Info */
.profile-info h2 {
  margin: 0;
  font-size: 1.5rem;
}

.profile-info p {
  margin: 0;
  color: color-mix(in oklab, var(--text-color) 50%, transparent);
  font-size: 0.9rem;
}

/* Level Bar Container */
.level-bar-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
  width: 200px;
}

/* Smaller Circle */
.level-circle {
  width: 40px;
  height: 40px;
  font-size: 1rem;
  border-radius: 50%;
  background-color: var(--color-primary);
  color: #fff;
  font-weight: 600;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  margin-bottom: 10px;
}

/* Smaller Bar */
.level-bar {
  flex: 1;
  height: 10px;
  background-color: color-mix(in oklab, var(--color-text) 20%, transparent);
  border-radius: 8px;
  overflow: hidden;
  min-width: 100px;
}

.level-fill {
  height: 100%;
  width: 60%;
  background-color: color-mix(in oklab, var(--color-text) 30%, transparent);
  border-radius: 8px 0 0 8px;
  transition: width 0.5s ease;
}

.level-percentage {
  font-size: 0.85rem;
  font-weight: 500;
  color: color-mix(in oklab, var(--text-color) 40%, transparent);
  white-space: nowrap;
}

.penguin-bubble {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.streak-card {
  background: var(--card-bg);
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.streak-card.full-width {
  width: 100%;
}

.week-row {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 8px;
  margin-bottom: 8px;
}

.day-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  z-index: 0;
}

.day-label {
  font-size: 0.75rem;
  color: #888;
}

.inactive {
  opacity: 0.25;
  filter: grayscale(1);
}

.streak-count {
  font-weight: 500;
  margin-top: 8px;
  text-align: center;
}

/* Suggested quizzes layout (bottom section) */
.suggested-quizzes {
  margin-top: 24px;
}

.suggested-quizzes h3 {
  margin-bottom: 16px;
  color: var(--color-accent);
}

.quiz-suggestions-row {
  display: flex;
  flex-direction: row;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.quiz-suggestion-item {
  background-color: var(--card-bg);
  border-radius: 10px;
  padding: 16px;
  min-width: 180px;
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quiz-suggestion-item:hover {
  background-color: color-mix(in oklab, var(--card-bg) 80%, #888 20%);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.quiz-suggestion-icon {
  color: var(--color-primary);
  background-color: rgba(33, 150, 243, 0.1);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
}

.quiz-suggestion-content h4 {
  margin: 0 0 4px 0;
  font-size: 1rem;
  color: var(--color-text);
}

.quiz-meta {
  margin: 0;
  font-size: 0.8rem;
  color: var(--color-muted);
}
</style>
