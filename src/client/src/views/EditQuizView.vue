<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { onMounted } from 'vue'
import { getQuiz, getQuizQuestions, createQuiz, updateQuiz } from '@/services/quizzes'
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

onMounted(async () => {

  if (isNewQuiz.value) {
    const lernset = route.params.lernsetId || quizEdit.lernsetId || null
    if (lernset)
      quizEdit.setLernset(lernset)
    else {
      alert('Kein Lernset ausgewählt. Bitte erstelle ein Quiz über die Lernset-Seite.')
      router.push('/')
      return
    }
    // Nur lokal initialisieren - Speicherung erst bei Click auf den Button "Speichern"
    if(!quizEdit.quizLoaded) {
      quizEdit.quizLoaded = true
      quizEdit.quizTitle = 'Mein Quiz'
      quizEdit.questions = [
        {
          id: Date.now(), // temporäre ID
          text: 'Frage 1',
          type: QUESTION_TYPES[0].api,
          options: [
            { id: Date.now() + 1, text: 'Antwort A', correct: false, _status: 'new' },
            { id: Date.now() + 2, text: 'Antwort B', correct: true, _status: 'new' },
            { id: Date.now() + 3, text: 'Antwort C', correct: false, _status: 'new' }
          ],
          _status: 'new'
        },
        {
          id: Date.now() + 1, // temporäre ID
          text: 'Frage 2',
          type: QUESTION_TYPES[0].api,
          options: [
            { id: Date.now() + 4, text: 'Antwort A', correct: true, _status: 'new' },
            { id: Date.now() + 5, text: 'Antwort B', correct: false, _status: 'new' },
            { id: Date.now() + 6, text: 'Antwort C', correct: false, _status: 'new' }
          ],
          _status: 'new'
        }
      ]
    }
    return
  } else {
    const quiz = await getQuiz(quizId.value)
    quizEdit.quizTitle = quiz.title
    quizEdit.setLernset(quiz.lernset)
    const serverQuestions = await getQuizQuestions(quizId.value)
    quizEdit.questions = serverQuestions.map(q => ({
      id: q.id,
      text: q.text,
      type: q.type,
      _status: 'unchanged'
    }))
  }
})

const goBack = () => {
  showBackModal.value = true
}
const confirmBack = () => {
  quizEdit.resetQuiz()
  quizEdit.quizLoaded = false
  showBackModal.value = falsen
  router.push({ 
    name: 'lernset', 
    params: { lernsetId: quizEdit.lernsetId } 
  })
}
const cancelBack = () => {
  showBackModal.value = false
}

const saveQuiz = async () => {
  // Bereite die Quiz-Daten vor
  const quizData = {
    title: quizEdit.quizTitle,
    description: '',
    is_public: true,
    lernset: quizEdit.lernsetId,
    questions: quizEdit.questions.map(q => ({
      id: q.id,
      text: q.text,
      type: q.type,
      _status: q._status,
      answer_options: q.options.map(opt => ({
        id: opt.id,
        text: opt.text,
        is_correct: opt.is_correct
      }))
    })).filter(q => q._status !== 'unchanged')
  }

  if (isNewQuiz.value) {
    await createQuiz(quizData)
  } else {
    await updateQuiz(quizId.value, quizData)
  }

  quizEdit.resetQuiz()
  router.push({ 
    name: 'lernset', 
    params: { lernsetId: quizEdit.lernsetId } 
  })
}

const addQuestion = async () => {
  quizEdit.addQuestion({
    id: Date.now(), // temporäre ID
    text: 'Neue Frage',
    type: QUESTION_TYPES[0].api, 
    options: [
            { id: Date.now() + 4, text: 'Antwort A', correct: true },
            { id: Date.now() + 5, text: 'Antwort B', correct: false },
            { id: Date.now() + 6, text: 'Antwort C', correct: false }
          ],
    _status: 'new'
  })
}

const deleteLocalQuestion = (id) => {

  const q = quizEdit.getQuestion(id)
  if (q._status === 'new') {
    quizEdit.removeQuestion(id)
  } else {
    q._status = 'deleted'
  }
}

const goToQuestion = (questionId) => {
  // Immer lokale Frage suchen und ID an EditQuestionView übergeben
  router.push({ name: 'edit-question', params: { questionId } })
}

const confirmDelete = (event, questionId) => {
  event.stopPropagation()
  questionToDelete.value = questionId
  questionToDeleteText.value = quizEdit.getQuestion(questionToDelete.value).text
  showDeleteModal.value = true
}
const deleteQuestionDialog = async () => {
  deleteLocalQuestion(questionToDelete.value)
  showDeleteModal.value = false
  questionToDelete.value = null
  questionToDeleteText.value = ''
}
const cancelDelete = () => {
  showDeleteModal.value = false
  questionToDelete.value = null
  questionToDeleteText.value = ''
}
</script>

<template>
  <div class="edit-quiz-view">
    <header class="edit-header">
      <h1>Quiz erstellen</h1>
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
.edit-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
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
  border: 1px solid #ddd;
  margin-top: 8px;
  margin-bottom: 4px;
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
  border: 1.5px solid #e3f2fd;
  border-radius: 9px;
  padding: 14px 12px;
  transition: box-shadow 0.15s, border 0.15s;
  background: #f9fbff;
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
  background: #f2f8fd;
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
  background: #e3f2fd;
  color: var(--color-secondary);
  border-radius: 6px;
  padding: 2px 10px;
}
.question-preview {
  font-size: 1.04rem;
  color: #333;
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
  background: rgba(0,0,0,0.18);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: #fff;
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
  color: #222;
  font-size: 1.04rem;
  word-break: break-word;
  background: #e3f2fd;
  padding: 8px 10px;
  border-radius: 7px;
}
</style>