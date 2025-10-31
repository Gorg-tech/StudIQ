<template>
  <div class="edit-question">
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <h1 class="page-title">Frage Bearbeiten</h1>
    <div class="edit-question-card">
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
          <button class="btn-icon" @click="showTypeDropdown = !showTypeDropdown">
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
        <button class="btn-icon" @click="addOption" aria-label="Antwort hinzufügen">
          <IconPlus />
        </button>
      </div>

      <div class="options-list">
        <div v-for="(option, idx) in options" :key="option.id" class="option-item" @click="toggleCorrect(idx)" :class="{ selected: option.correct }">
          <div class="option-title">
            <span v-if="option.correct" class="checkmark">✓</span>
            <span 
              class="option-text" 
              contenteditable 
              @click.stop
              @input="option.text = $event.target.innerText" 
              @blur="finishEdit(idx)"
              :title="option.text"
              :data-placeholder="option.text ? '' : 'Antwort eingeben...'"
            >
              {{ option.text }}
            </span>
          </div>
          <div class="option-actions">
            <button class="btn-icon delete-option" @click.stop="deleteOption(idx)" aria-label="Antwort löschen">
              <IconTrash />
            </button>
          </div>
        </div>
      </div>

      <div class="footer-buttons">
        <button class="cancel-btn" @click="cancelEdit">
          Abbrechen
        </button>
        <button class="save-btn" @click="saveQuestion">
          <!-- Save Icon SVG, white -->
          <IconSave style="color: white"/>
          Speichern
        </button>
      </div>
    </div>

    <!-- Delete Confirmation Popup -->
    <Teleport to="body">
      <div v-if="deletePopup.open" class="edit-popup-overlay">
        <div class="edit-popup">
          <h3>Möchtest du wirklich folgende Antwortmöglichkeit löschen?</h3>
          <p class="popup-answer-text">{{ deletePopup.text }}</p>
          <div class="edit-popup-actions">
            <button class="cancel-btn" @click="closeDeletePopup">Abbrechen</button>
            <button class="delete-btn" @click="confirmDelete">Löschen</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Cancel Confirmation Popup -->
    <Teleport to="body">
      <div v-if="cancelPopup.open" class="edit-popup-overlay">
        <div class="edit-popup">
          <h3>Alle Änderungen werden gelöscht</h3>
          <div class="edit-popup-actions">
            <button class="cancel-btn" @click="closeCancelPopup">Abbrechen</button>
            <button class="delete-btn" @click="confirmCancel">OK</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useQuizEditStore, QUESTION_TYPES, getLabelFromApi } from '@/stores/editQuiz'
import { getAnswers } from '@/services/questions'
import { getAnswer } from '@/services/answer_options'
import IconPlus from '@/components/icons/IconPlus.vue'
import IconSave from '@/components/icons/IconSave.vue'
import IconTrash from '@/components/icons/IconTrashcan.vue'

const router = useRouter()
const route = useRoute()

const quizEdit = useQuizEditStore()

const questionId = Number(route.params.questionId)
const question = ref(null)

const questionText = ref('')
const questionTypes = QUESTION_TYPES.map(q => q.label)
const selectedType = ref(QUESTION_TYPES[0].label)
const showTypeDropdown = ref(false)
const options = ref([])

const errorMessage = ref('')

const selectedTypeApi = computed(() =>
  QUESTION_TYPES.find(q => q.label === selectedType.value)?.api || QUESTION_TYPES[0].api
)

onMounted(async () => {

  // Frage laden
  question.value = quizEdit.getQuestion(questionId)
  if(!question.value) {
    console.error('Frage nicht gefunden:', questionId)
    if (quizEdit.quizId) {
      router.push({ name: 'edit-quiz', params: { quizId: quizEdit.quizId, lernsetId: quizEdit.lernsetId } })
    } else {
      router.push({ name: 'lernset', params: { lernsetId: quizEdit.lernsetId } })
    }
    return
  }

  questionText.value = question.value.text || ''
  selectedType.value = getLabelFromApi(question.value.type) || QUESTION_TYPES[0].label

  if(question.value._status === 'unchanged') {
    // Wenn die Frage noch nicht geändert wurde, Antworten aus der Datenbank laden
    const loadedAnswers = await getAnswers(questionId)
    if (!loadedAnswers) {
      console.error('Frage konnte nicht geladen werden:', questionId)
      if (quizEdit.quizId) {
        router.push({ name: 'edit-quiz', params: { quizId: quizEdit.quizId, lernsetId: quizEdit.lernsetId } })
      } else {
        router.push({ name: 'lernset', params: { lernsetId: quizEdit.lernsetId } })
      }
      return
    }
    // Für jede Antwortmöglichkeit ein neues Objekt erstellen und mit getAnswer correct Variable laden und in options speichern
    for (const answer of loadedAnswers) {
      const answerDetails = await getAnswer(answer.id)
      options.value.push({
        id: answer.id,
        text: answer.text,
        correct: answerDetails.correct,
        _status: 'unchanged' 
      })
    }
    
  } else {
    options.value = question.value.options.map(opt => ({
      id: opt.id,
      text: opt.text,
      correct: opt.correct,
      _status: opt._status
    }))
  }
})

function selectType(type) {
  selectedType.value = type
  showTypeDropdown.value = false
}

function addOption() {
  options.value.push({
    id: Date.now(),
    text: '',
    correct: false,
    _status: 'new'
  })
}

function finishEdit(idx) {
  const opt = options.value[idx]
  opt.text = opt.text.trim()
  if (opt.text === '') {
    opt.text = ''
  }
  if (opt._status !== 'new') {
    opt._status = 'edited'
  }
}

const deletePopup = ref({
  open: false,
  idx: null,
  text: '',
})

function openDeletePopup(idx) {
  deletePopup.value.open = true
  deletePopup.value.idx = idx
  deletePopup.value.text = options.value[idx].text
}
function closeDeletePopup() {
  deletePopup.value.open = false
  deletePopup.value.idx = null
  deletePopup.value.text = ''
}
function confirmDelete() {
  if (deletePopup.value.idx !== null) {
    const opt = options.value[deletePopup.value.idx]
    if (opt._status === 'new') {
      options.value.splice(deletePopup.value.idx, 1)
    } else {
      opt._status = 'deleted'
    }
  }
  closeDeletePopup()
}

const cancelPopup = ref({
  open: false,
})
function openCancelPopup() {
  cancelPopup.value.open = true
}
function closeCancelPopup() {
  cancelPopup.value.open = false
}
function confirmCancel() {
  cancelPopup.value.open = false
  if (quizEdit.quizId) {
    router.push({ name: 'edit-quiz', params: { quizId: quizEdit.quizId, lernsetId: quizEdit.lernsetId } })
  } else {
    router.push({ name: 'lernset', params: { lernsetId: quizEdit.lernsetId } })
  }
}

// Update delete button in option-actions:
function deleteOption(idx, event) {
  event.stopPropagation()
  openDeletePopup(idx)
}

// Update cancelEdit to open popup:
function cancelEdit() {
  openCancelPopup()
}

// Update saveQuestion to redirect:
async function saveQuestion() {
  errorMessage.value = ''

  if (!questionText.value.trim()) {
    errorMessage.value = 'Fragetext ist erforderlich.'
    return
  }

  if (options.value.length < 2) {
    errorMessage.value = 'Mindestens zwei Antwortoptionen sind erforderlich.'
    return
  }

  for (const opt of options.value) {
    if (!opt.text || opt.text.trim() === '') {
      errorMessage.value = 'Alle Antwortoptionen müssen einen Text haben.'
      return
    }
  }

  const hasCorrect = options.value.some(opt => opt.correct)
  if (!hasCorrect) {
    errorMessage.value = 'Mindestens eine Antwortoption muss als korrekt markiert sein.'
    return
  }

  const correctCount = options.value.filter(opt => opt.correct).length
  const autoType = correctCount === 1 ? 'SINGLE_CHOICE' : 'MULTIPLE_CHOICE'
  selectedType.value = QUESTION_TYPES.find(q => q.api === autoType)?.label || selectedType.value

  quizEdit.updateQuestion(question.value.id, {
    text: questionText.value,
    type: autoType,
    options: options.value.map(opt => ({ ...opt })),
    _status: question.value._status === 'new' ? 'new' : 'edited'
  })
  router.push({ name: 'edit-quiz', params: { quizId: quizEdit.quizId, lernsetId: quizEdit.lernsetId } })
}

function toggleCorrect(idx) {
  if (selectedTypeApi.value === 'SINGLE_CHOICE') {
    options.value.forEach((opt, i) => (opt.correct = i === idx))
  } else {
    options.value[idx].correct = !options.value[idx].correct
  }
}
</script>

<style scoped>
.edit-question {
  max-width: 600px;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-accent);
  text-align: center;
  margin: 0;
  padding: 24px 0;
}

.error-message {
  color: var(--color-red);
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid var(--color-red);
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  font-weight: 500;
}

.edit-question-card {
  background: var(--card-bg); 
  border-radius: 16px;
  box-shadow: var(--color-shadow);
  padding: 32px 16px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section h3 {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 6px;
  color: var(--color-muted);
}

.question-input {
  width: 100%;
  border-radius: 8px;
  border: 1px solid var(--color-border-dark);
  padding: 12px;
  font-size: 1rem;
  margin-top: 8px;
  resize: vertical;
  background: var(--card-bg); 
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

.options-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.option-item {
  background: var(--card-bg); 
  border-radius: 10px;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  min-height: 48px;
  border: 1px solid var(--color-border);
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08); 
  cursor: pointer;
  transition: background-color 0.2s;
}
.option-item:hover {
  background: var(--color-bg-hover);
}
.option-item.selected {
  background: var(--color-selected);
  border-color: var(--color-primary);
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
  cursor: text;
  outline: none;
  border: 1px solid transparent;
  border-radius: 4px;
  padding: 4px 6px;
  transition: border-color 0.2s, background-color 0.2s;
  min-height: 1.2em;
  display: inline-block;
}

.option-text:focus {
  border-color: var(--color-primary);
  background: var(--color-bg-light);
}

.option-text:empty:before {
  content: attr(data-placeholder);
  color: var(--color-muted);
  pointer-events: none;
}

.checkmark {
  color: var(--color-green);
  font-weight: bold;
  font-size: 1.2rem;
  margin-right: 8px;
}

.option-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  position: static;
}

.footer-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  gap: 18px;
}

.cancel-btn {
  background: transparent;
  color: var(--color-secondary);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.cancel-btn:hover {
  background-color: var(--color-question-border);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.save-btn {
  background: var(--color-secondary);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  filter: brightness(0.93);
}

.delete-btn {
  background-color: var(--color-red);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.delete-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  filter: brightness(0.93);
}

/* Popup styles */
.edit-popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.edit-popup {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 24px;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  text-align: center;
}

.edit-popup h3 {
  margin: 0 0 16px 0;
  color: var(--color-accent);
}

.popup-answer-text {
  background: var(--color-bg-light);
  padding: 12px;
  border-radius: 8px;
  margin: 16px 0;
  color: var(--color-text);
  word-break: break-word;
}

.edit-popup-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}
</style>
