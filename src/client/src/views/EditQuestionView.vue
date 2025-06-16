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
        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" stroke="#2196f3"/>
          <path d="M12 8v8M8 12h8" stroke="#2196f3" stroke-linecap="round"/>
        </svg>
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
          <button class="edit-btn" @click="editOption(idx)" aria-label="Antwort bearbeiten">
            <!-- Pen Icon SVG -->
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M2 14l4 0 8-8-4-4-8 8z" stroke="#4caf50"/>
              <path d="M14 6l2 2" stroke="#4caf50"/>
            </svg>
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
            <!-- Trash Icon SVG -->
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="6" width="12" height="9" rx="2" stroke="#f44336"/>
              <path d="M8 9v3M10 9v3M5 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2" stroke="#f44336"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div class="footer-buttons">
      <button class="cancel-btn" @click="cancelEdit">
        Abbrechen
      </button>
      <button class="save-btn" @click="saveQuestion">
        <!-- Save Icon SVG -->
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="14" height="14" rx="2" stroke="#2196f3"/>
          <path d="M7 3v4h6V3" stroke="#2196f3"/>
          <path d="M7 13h6" stroke="#2196f3"/>
        </svg>
        Speichern
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

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
  // Optionally reset options for Freitext
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

function editOption(idx) {
  const newText = prompt('Antwort bearbeiten:', options.value[idx].text)
  if (newText !== null && newText.trim() !== '') {
    options.value[idx].text = newText
  }
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
.edit-question {
  max-width: 600px;
  margin: 0 auto;
  padding: 32px 16px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(34,34,34,0.08);
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
  border: 1px solid #ddd;
  padding: 12px;
  font-size: 1rem;
  margin-top: 8px;
  resize: vertical;
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
}
.selected-type {
  margin-left: 12px;
  font-weight: 500;
  color: #2196f3;
}
.dropdown {
  position: absolute;
  top: 2.5em;
  left: 0;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(34,34,34,0.08);
  z-index: 10;
  min-width: 140px;
}
.dropdown-item {
  padding: 8px 16px;
  cursor: pointer;
  color: #222;
}
.dropdown-item:hover {
  background: #f5f5f5;
}
.add-option-btn {
  background: #2196f3;
  border: none;
  border-radius: 50%;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s;
}
.add-option-btn:hover {
  background: #1976d2;
}
.options-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.option-item {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 12px 12px 28px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  min-height: 48px;
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
  color: #222;
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
  color: #4caf50;
  padding: 2px;
}
.option-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
input[type="checkbox"] {
  width: 20px;
  height: 20px;
  accent-color: #2196f3;
}
.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  position: absolute;
  bottom: 6px;
  right: 8px;
  color: #f44336;
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
  background: #eee;
  color: #222;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.cancel-btn:hover {
  background: #ddd;
}
.save-btn {
  background: #2196f3;
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
  background: #1976d2;
}
</style>
