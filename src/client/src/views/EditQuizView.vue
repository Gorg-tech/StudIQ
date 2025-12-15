<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { onMounted } from 'vue'
import { getQuiz, createQuiz, updateQuiz } from '@/services/quizzes'
import { useQuizEditStore, QUESTION_TYPES, getLabelFromApi } from '@/stores/editQuiz'
import IconTrashcan from '@/components/icons/IconTrashcan.vue'
import IconSave from '@/components/icons/IconSave.vue'


const router = useRouter()
const route = useRoute()
const quizId = ref(route.params.quizId || null)

const quizEdit = useQuizEditStore()

const showDeleteModal = ref(false)
const questionToDelete = ref(null)
const questionToDeleteText = ref('')

const showBackModal = ref(false)
const isNewQuiz = ref(!route.params.quizId)

const errorMessage = ref('')

/**
 * Loads Quiz-Data from Server
 * Writes Data to quizEdit
 * 
 * @param {String} quizId Quiz-Id
 */
async function fetch_quiz(quizId){
    const quiz = await getQuiz(quizId)
    quizEdit.setQuiz({
      id: quiz.id,
      title: quiz.title,
      lernset: quiz.lernset,
      questions: quiz.questions.map(q => ({
        id: q.id,
        text: q.text,
        type: q.type,
        options: q.answer_options.map(opt => ({
          id: opt.id,
          text: opt.text,
          correct: opt.is_correct,
          _status: 'unchanged'
        })),
        _status: 'unchanged'
      }))
    })
}

/**
 * Initializes the quiz on component mount.
 *  - If the store already has a loaded quiz:
 *      → Reuse it unless the route quizId differs, then re-fetch.
 *  - If creating a new quiz:
 *      → Ensure a Lernset is available and prepare an empty quiz state.
 *  - If editing an existing quiz:
 *      → Fetch the quiz data from the server.
 * 
 * Handles navigation when no Lernset is available for new quizzes.
 */
async function initializeQuiz() {
  // Case 1: Quiz already loaded in store
  if (quizEdit.quizLoaded) {
    if (quizId.value && quizEdit.quizId !== quizId.value) {
      await fetch_quiz(quizId.value)
    }
    return
  }

  // Case 2: New quiz creation
  if (isNewQuiz.value) {
    const lernsetId =
      route.params.lernsetId ||
      quizEdit.lernsetId ||
      null

    if (!lernsetId) {
      alert('Kein Lernset ausgewählt. Bitte erstelle ein Quiz über die Lernset-Seite.')
      router.push('/')
      return
    }

    quizEdit.setLernset(lernsetId)
    quizEdit.quizLoaded = true

    // Ensure questions array exists
    if (!quizEdit.questions.length) {
      quizEdit.questions = []
    }

    return
  }

  // Case 3: Editing existing quiz
  await fetch_quiz(quizId.value)
}

/**
 * Handler for "Back"-Button clicked
 * - resets Quiz
 * - sends User to QuizOverview or LernsetOverview
 */
function handle_backrouting(){
  const existingQuizId = quizEdit.quizId
  const targetLernset = quizEdit.lernsetId
  quizEdit.resetQuiz(true)
  showBackModal.value = false
  if (existingQuizId) {
    //Mode: EditQuiz
    router.push({ name: 'quiz-overview', params: { quizId: existingQuizId } })
  } else {
    //Mode: CreateQuiz
    router.push({ name: 'lernset', params: { lernsetId: targetLernset } })
  }
}

const goBack = () => {
  showBackModal.value = true
}
const confirmBack = () => {
  handle_backrouting()
}
const cancelBack = () => {
  showBackModal.value = false
}

/**
 * Checks Quiz-Data on correct Values and correct related Question-Data to achieve a correct Save
 * 
 * @returns {bool} If Quiz has correct Values
 */
function quiz_has_correct_values(){
  errorMessage.value = ''
  if (!quizEdit.quizTitle.trim()) {
    errorMessage.value = 'Quiz-Titel ist erforderlich.'
    return false
  }

  // Require at least 3 questions
  if (quizEdit.questions.length < 3) {
    errorMessage.value = 'Bitte füge mindestens 3 Fragen hinzu, bevor du das Quiz speicherst.'
    return false
  }

  for (const q of quizEdit.questions) {
    if (q._status === 'deleted') continue
    if (!q.options || q.options.length < 2) {
      errorMessage.value = 'Jede Frage muss mindestens zwei Antwortoptionen haben.'
      return false
    }
    for (const opt of q.options) {
      if (!opt.text || opt.text.trim() === '') {
        errorMessage.value = 'Alle Antwortoptionen müssen einen Text haben.'
        return false
      }
    }
  }
  return true
}

/**
 * Gives API-Call for Request to Edit(Create/Update) the Quiz
 * Maps current given quiz-Data for Edit-Request and sends it to the API-Service
 */
async function send_edit_request() {
  // Bereite die Quiz-Daten vor
  const quizData = {
    title: quizEdit.quizTitle,
    description: '',
    is_public: true,
    lernset: quizEdit.lernsetId,
    questions: quizEdit.questions
      .filter(q => q._status !== 'deleted')
      .map(q => ({
        ...(q._status !== 'new' ? { id: q.id } : {}),
        text: q.text,
        type: q.type,
        _status: q._status,
        answer_options: (q.options || [])
          .filter(opt => opt._status !== 'deleted')
          .map(opt => ({
            ...(opt._status !== 'new' ? { id: opt.id } : {}),
            text: opt.text,
            is_correct: opt.correct,
            _status: opt._status
          }))
      }))
      .filter(q => {
        // Keep all new/edited/deleted questions; for unchanged only keep if answers changed
        if (q._status !== 'unchanged') return true
        if (q.answer_options && q.answer_options.some(opt => opt._status !== 'unchanged')) {
          q._status = 'edited'
          return true
        }
        return false
      })
  }

  console.log('saveQuiz -> quizData being sent:', JSON.stringify(quizData, null, 2))

  try {
    let newQuizId = quizId.value
    if (isNewQuiz.value) {
      const createdQuiz = await createQuiz(quizData)
      newQuizId = createdQuiz.id
    } else {
      await updateQuiz(quizId.value, quizData)
    }

    quizEdit.resetQuiz() // no need to preserve lernset for quiz overview
    router.push({ name: 'quiz-overview', params: { quizId: newQuizId } })
  } catch (error) {
    errorMessage.value = 'Fehler beim Speichern des Quiz. Bitte versuche es später erneut.'
    console.error('Error saving quiz:', error)
  }
}

/**
 * Saves Quiz into Server
 * 
 * Checks for correct Values, 
 * Maps new Data for Server-Compatibility, Sends Create/Update-Request
 */
async function saveQuiz(){
  if(!quiz_has_correct_values()){
    return
  }
  send_edit_request()
}

/**
 * Adds Question to View, initializes Answer-Values
 */
async function addQuestion()
{
  const newQuestion = {
    id: Date.now().toString(), // temporäre ID
    text: '',
    type: QUESTION_TYPES[0].api,
    options: [
      { id: Date.now().toString() + '1', text: '', correct: false, _status: 'new' },
      { id: Date.now().toString() + '2', text: '', correct: false, _status: 'new' }
    ],
    _status: 'new'
  }
  quizEdit.addQuestion(newQuestion)
  router.push({ name: 'edit-question', params: { questionId: newQuestion.id } })
}

/**
 * Deletes a Question of the Quiz
 * @param id Id from the Question to be deleted
 */
function deleteLocalQuestion(id){

  const q = quizEdit.getQuestion(id)
  if (q._status === 'new') {
    quizEdit.removeQuestion(id)
  } else {
    q._status = 'deleted'
  }
}

/**
 * Sends User to the EditQuestionView
 * @param questionId ID of the Question to be edites
 */
function goToQuestion(questionId){
  // Always search for local Question, then send Id to EditQuestionView
  router.push({ name: 'edit-question', params: { questionId } })
}

/**
 * Öffnet den Löschdialog für eine bestimmte Frage.
 * @param {Event} event - Das Click-Event, dessen Propagation gestoppt wird.
 * @param {number|string} questionId - Die ID der zu löschenden Frage.
 */
function confirmDelete(event, questionId)
{
  event.stopPropagation()
  questionToDelete.value = questionId
  questionToDeleteText.value = quizEdit.getQuestion(questionToDelete.value).text
  showDeleteModal.value = true
}

/**
 * Löscht die aktuell ausgewählte Frage endgültig und schließt den Dialog.
 * @returns {Promise<void>} Wird aufgelöst, sobald der Löschvorgang abgeschlossen ist.
 */
async function deleteQuestionDialog()
{
  deleteLocalQuestion(questionToDelete.value)
  showDeleteModal.value = false
  questionToDelete.value = null
  questionToDeleteText.value = ''
}

/**
 * Bricht den Löschvorgang ab und setzt den Dialog zurück.
 */
function cancelDelete()
{
  showDeleteModal.value = false
  questionToDelete.value = null
  questionToDeleteText.value = ''
}

onMounted(async () => {
  initializeQuiz()
})

</script>

<template>
  <div class="edit-quiz-view">
    <header class="edit-header">
      <h1>{{ isNewQuiz ? 'Quiz erstellen' : 'Quiz bearbeiten' }}</h1>
    </header>
    <main class="edit-main">
      <section class="quiz-title-section card">
        <label class="block-label" for="quizTitle">Dein Quiz-Titel</label>
        <input
          id="quizTitle"
          v-model="quizEdit.quizTitle"
          class="input-title"
          placeholder="Quiz-Titel hier eingeben"
        />
      </section>

      <section class="quiz-questions-section card">
        <div class="questions-header">
          <h2 class="questions-section-title">Deine Quiz-Fragen</h2>
          <button class="btn-icon" type="button" @click="addQuestion" aria-label="Frage hinzufügen">
            <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" stroke="#2196f3"/>
              <path d="M12 8v8M8 12h8" stroke="#2196f3" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
        <div
          v-for="(question, idx) in quizEdit.questions"
          :key="question.id"
          class="question-field question-interactive"
          @click="goToQuestion(question.id)"
          tabindex="0"
          @keydown.enter="goToQuestion(question.id)"
          @keydown.space="goToQuestion(question.id)"
        >
          <div class="question-header">
            <span class="question-index">{{ idx + 1 }}. Frage</span>
            <span class="question-type">{{ getLabelFromApi(question.type) }}</span>
          </div>
          <div class="question-preview">
            <span class="question-text">{{ question.text || `Fragetext für Frage ${idx + 1}` }}</span>
            <button
              class="btn-icon question-delete"
              @click.stop="confirmDelete($event, question.id, question.text)"
              aria-label="Frage löschen"
            >
              <IconTrashcan />
            </button>
          </div>
        </div>
      </section>

      <div class="edit-actions">
        <button class="btn btn-secondary" @click="goBack">
          Zurück
        </button>
        <button class="btn btn-primary" @click="saveQuiz">
          <IconSave style="color: white"/>
          Speichern
        </button>
      </div>

      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </main>

    <!-- Delete confirmation modal -->
    <Teleport to="body">
      <div v-if="showDeleteModal" class="modal-backdrop">
        <div class="modal">
          <h3>Frage löschen?</h3>
          <p>Möchtest du diese Frage wirklich löschen?</p>
          <p class="modal-question-text">
            <b>{{ questionToDeleteText }}</b>
          </p>
          <div class="modal-actions">
            <button class="btn btn-secondary" @click="cancelDelete">Abbrechen</button>
            <button class="btn btn-danger" @click="deleteQuestionDialog">Löschen</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Back confirmation modal -->
    <Teleport to="body">
      <div v-if="showBackModal" class="modal-backdrop">
        <div class="modal">
          <h3>Zurück ohne Speichern?</h3>
          <p>Ungespeicherte Änderungen gehen verloren. Möchtest du wirklich zurückgehen?</p>
          <div class="modal-actions">
            <button class="btn btn-secondary" @click="cancelBack">Abbrechen</button>
            <button class="btn btn-danger" @click="confirmBack">Zurück</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.edit-quiz-view {
  max-width: 600px;
  margin: 0 auto;
  padding: 24px 12px 0 12px;
  display: flex;
  flex-direction: column;
}
.edit-header {
  margin-bottom: 20px;
  text-align: center;
}
.edit-header h1 {
  font-size: 2rem;
  font-weight: 700;
}
.edit-header .edit-subtitle {
  font-size: 1.1rem;
  color: var(--color-muted, #888);
  margin-top: 4px;
}
.edit-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.card {
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 2px 8px var(--card-shadow);
  padding: 20px;
}
.block-label {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 6px;
  display: block;
  color: var(--color-muted, #888);
}
.input-title {
  width: 100%;
  font-size: 1.1rem;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  margin-top: 8px;
  margin-bottom: 4px;
  background: var(--card-bg);
  color: var(--color-text);
}

.error-input {
  border-color: var(--color-red) !important;
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

.questions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quiz-questions-section {
  margin-top: 10px;
}

.questions-section-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-accent);
  margin: 0;
}

.question-field {
  margin-bottom: 22px;
  border: 1.5px solid var(--color-question-border);
  border-radius: 9px;
  padding: 14px 12px;
  transition: box-shadow 0.15s, border 0.15s;
  background: var(--color-question-bg);
}
.question-field:last-child {
  margin-bottom: 0;
}
.question-interactive {
  cursor: pointer;
  user-select: none;
}
.question-interactive:hover, .question-interactive:focus {
  border: 1.5px solid var(--color-secondary);
  box-shadow: 0 2px 10px 2px rgba(25, 118, 210, 0.08);
  background: var(--color-question-hover);
  outline: none;
}
.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  margin-bottom: 6px;
}
.question-index {
  color: var(--color-primary);
  font-size: 1.05rem;
}
.question-type {
  font-size: 0.97rem;
  background: var(--color-question-border);
  color: var(--color-secondary);
  border-radius: 6px;
  padding: 2px 10px;
}
.question-preview {
  font-size: 1.04rem;
  color: var(--color-text);
  padding: 6px 0 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.question-delete {
  margin-left: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.edit-actions {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  margin-top: 10px;
}

.btn-primary {
  background: var(--color-secondary);
  color: #fff;
}

.btn-danger {
  background-color: var(--color-red);
  color: #fff;
  border: none;
}

/* Modal styles */
.modal-backdrop {
  position: fixed;
  z-index: 1000;
  left: 0; top: 0; right: 0; bottom: 0;
  background: var(--color-modal-backdrop);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 32px 28px 24px 28px;
  box-shadow: 0 4px 32px 4px rgba(25,118,210,0.14);
  max-width: 340px;
  width: 100%;
  text-align: center;
}
.modal h3 {
  margin-top: 0;
  margin-bottom: 14px;
  font-size: 1.15rem;
}
.modal-actions {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  margin-top: 28px;
}
.modal-question-text {
  margin: 20px 0 0 0;
  color: var(--color-text);
  font-size: 1.04rem;
  word-break: break-word;
  background: var(--color-question-border);
  padding: 8px 10px;
  border-radius: 7px;
}
</style>
