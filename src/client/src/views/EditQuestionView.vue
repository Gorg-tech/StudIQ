<template>
  <div class="edit-question">
    <h1>Frage Bearbeiten</h1>
    <div class="section">
      <h3>Fragetext eingeben</h3>
      <textarea
        v-model="questionText"
        class="question-input"
        placeholder="z.B. Was ist das Ergebnis von 2 + 2?"
        rows="3"
      />
    </div>

    <div class="section type-row">
      <div class="type-label">
        <h3>Typ der Frage</h3>
        <button class="arrow-btn" @click="showTypeDropdown = !showTypeDropdown">
          <span>&#x25BC;</span>
        </button>
        <div v-if="showTypeDropdown" class="dropdown">
          <div
            v-for="type in questionTypes"
            :key="type"
            class="dropdown-item"
            @click="selectType(type)"
          >
            {{ type }}
          </div>
        </div>
        <span class="selected-type">{{ selectedType }}</span>
      </div>
      <button class="add-option-btn" @click="addOption" aria-label="Antwort hinzufügen">
        <!-- Plus Icon SVG -->
        <IconPlus />
      </button>
    </div>

    <div class="options-list">
      <div
        v-for="(option, idx) in options"
        :key="option.id"
        class="option-item"
      >
        <div class="option-title">
          <span class="option-text" :title="option.text">
            {{ truncate(option.text, 30) }}
          </span>
          <button class="edit-btn" @click="openEditPopup(idx)" aria-label="Antwort bearbeiten">
            <IconPen />
          </button>
        </div>
        <div class="option-actions">
          <input
            v-if="selectedType !== 'Freitext'"
            type="checkbox"
            :checked="option.correct"
            @change="toggleCorrect(idx)"
            :aria-label="option.correct ? 'Richtige Antwort' : 'Falsche Antwort'"
          />
          <button class="delete-btn" @click="deleteOption(idx)" aria-label="Antwort löschen">
            <!-- TODO: Implement Trash Icon from Georg -->
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Option Popup -->
    <div v-if="editPopup.open" class="edit-popup-overlay">
      <div class="edit-popup">
        <h3>Antwort bearbeiten</h3>
        <input
          v-model="editPopup.text"
          class="edit-popup-input"
          type="text"
          :maxlength="100"
        />
        <div class="edit-popup-actions">
          <button class="cancel-btn" @click="closeEditPopup">Abbrechen</button>
          <button class="save-btn" @click="applyEdit">Ändern</button>
        </div>
      </div>
    </div>

    <div class="footer-buttons">
      <button class="cancel-btn" @click="cancelEdit">
        Abbrechen
      </button>
      <button class="save-btn" @click="saveQuestion">
        <!-- Save Icon SVG, white -->
        <IconSave />
        Speichern
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import IconPen from '@/components/icons/IconPen.vue'
import IconPlus from '@/components/icons/IconPlus.vue'
import IconSave from '@/components/icons/IconSave.vue'
import IconTrash from '@/components/icons/IconTrashCan.vue' // Assuming you have a Trash icon component

const router = useRouter()

const questionText = ref('')
const questionTypes = ['Single Choice', 'Multiple Choice', 'Freitext']
const selectedType = ref('Single Choice')
const showTypeDropdown = ref(false)

const options = ref([
  { id: 1, text: 'Antwort A', correct: false },
  { id: 2, text: 'Antwort B', correct: false },
])

function selectType(type) {
  selectedType.value = type
  showTypeDropdown.value = false
  if (type === 'Freitext') {
    options.value = []
  }
}

function addOption() {
  options.value.push({
    id: Date.now(),
    text: 'Neue Antwort',
    correct: false,
  })
}

// Edit popup state
const editPopup = ref({
  open: false,
  idx: null,
  text: '',
})

function openEditPopup(idx) {
  editPopup.value.open = true
  editPopup.value.idx = idx
  editPopup.value.text = options.value[idx].text
}

function closeEditPopup() {
  editPopup.value.open = false
  editPopup.value.idx = null
  editPopup.value.text = ''
}

function applyEdit() {
  if (
    editPopup.value.idx !== null &&
    editPopup.value.text.trim() !== ''
  ) {
    options.value[editPopup.value.idx].text = editPopup.value.text.trim()
  }
  closeEditPopup()
}

function deleteOption(idx) {
  options.value.splice(idx, 1)
}

function toggleCorrect(idx) {
  if (selectedType.value === 'Single Choice') {
    options.value.forEach((opt, i) => (opt.correct = i === idx))
  } else {
    options.value[idx].correct = !options.value[idx].correct
  }
}

function cancelEdit() {
  router.push('/editQuiz')
}

function saveQuestion() {
  // TODO: Save logic
  alert('Frage gespeichert!')
}

function truncate(text, maxLength) {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength - 3) + '...'
}
</script>

<style scoped>
:root {
  --color-bg: #fff;
  --color-bg-light: #f9f9f9;
  --color-bg-hover: #f5f5f5;
  --color-border: #eee;
  --color-border-dark: #ddd;
  --color-blue: #2196f3;
  --color-blue-dark: #1976d2;
  --color-red: #f44336;
  --color-green: #4caf50;
  --color-text: #222;
  --color-muted: #888;
  --color-shadow: 0 2px 8px rgba(34,34,34,0.08);
}

.edit-question {
  max-width: 600px;
  margin: 0 auto;
  padding: 32px 16px;
  background: var(--color-bg);
  border-radius: 16px;
  box-shadow: var(--color-shadow);
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.section {
  margin-bottom: 12px;
}
.question-input {
  width: 100%;
  border-radius: 8px;
  border: 1px solid var(--color-border-dark);
  padding: 12px;
  font-size: 1rem;
  margin-top: 8px;
  resize: vertical;
  background: var(--color-bg);
  color: var(--color-text);
}
.type-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  position: relative;
}
.type-label {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}
.arrow-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  margin-left: 4px;
  color: var(--color-blue);
}
.selected-type {
  margin-left: 12px;
  font-weight: 500;
  color: var(--color-blue);
}
.dropdown {
  position: absolute;
  top: 2.5em;
  left: 0;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  box-shadow: var(--color-shadow);
  z-index: 10;
  min-width: 140px;
}
.dropdown-item {
  padding: 8px 16px;
  cursor: pointer;
  color: var(--color-text);
}
.dropdown-item:hover {
  background: var(--color-bg-hover);
}
.add-option-btn {
  background: none;
  border: none;
  border-radius: 50%;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-blue);
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: none;
}
.add-option-btn:hover {
  background: var(--color-bg-hover);
}
.options-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.option-item {
  background: var(--color-bg-light);
  border-radius: 10px;
  padding: 12px 12px 28px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  min-height: 48px;
  border: 1px solid var(--color-border);
}
.option-title {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}
.option-text {
  font-size: 1rem;
  color: var(--color-text);
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.edit-btn {
  background: none;
  border: none;
  cursor: pointer;
  margin-left: 4px;
  color: var(--color-blue);
  padding: 2px;
  display: flex;
  align-items: center;
}
.option-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  position: static;
}
input[type="checkbox"] {
  width: 20px;
  height: 20px;
  accent-color: var(--color-blue);
}
.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  position: static;
  color: var(--color-red);
  padding: 2px;
  display: flex;
  align-items: center;
  padding: 2px;
}
.footer-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  gap: 12px;
}
.cancel-btn {
  background: var(--color-border);
  color: var(--color-text);
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.cancel-btn:hover {
  background: var(--color-border-dark);
}
.save-btn {
  background: var(--color-blue);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 24px;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.save-btn:hover {
  background: var(--color-blue-dark);
}

/* Edit Option Popup */
.edit-popup-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.edit-popup {
  background: var(--color-bg);
  border-radius: 14px;
  box-shadow: var(--color-shadow);
  padding: 28px 24px 18px 24px;
  min-width: 320px;
  max-width: 90vw;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.edit-popup-input {
  width: 100%;
  border-radius: 8px;
  border: 1px solid var(--color-border-dark);
  padding: 10px;
  font-size: 1rem;
  color: var(--color-text);
  background: var(--color-bg);
}
.edit-popup-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.edit-popup .cancel-btn {
  background: var(--color-border);
  color: var(--color-text);
  padding: 8px 18px;
}
.edit-popup .save-btn {
  background: var(--color-blue);
  color: #fff;
  padding: 8px 18px;
}
.edit-popup .save-btn:hover {
  background: var(--color-blue-dark);
}
</style>