<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// Plus-Icon als Komponente
const PlusIcon = {
  name: 'PlusIcon',
  template: `<svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="11" stroke="#1976d2" fill="#e3f2fd"/>
    <path d="M12 8v8M8 12h8" stroke="#1976d2" stroke-width="2" stroke-linecap="round"/>
  </svg>`
}

const router = useRouter()

const quizTitle = ref('Mein erstes Quiz')
const questions = ref([
  {
    id: 1,
    text: 'Was ist die Hauptstadt von Deutschland?',
    type: 'Multiple Choice'
  }
])

const goBack = () => {
  router.push('/')
}
const saveQuiz = () => {
  router.push('/')
}
const addQuestion = () => {
  questions.value.push({
    id: questions.value.length + 1,
    text: '',
    type: 'Multiple Choice'
  })
}
// Navigiere auf Detailseite der Frage
const goToQuestion = (questionId) => {
  router.push(`/editQuestion`)
}
</script>

<template>
  <div class="edit-quiz-view">
    <header class="edit-header">
      <h1>Quiz bearbeiten</h1>
    </header>
    <main class="edit-main">
      <section class="quiz-title-section card">
        <label class="block-label" for="quizTitle">Dein Quiz-Titel</label>
        <input
          id="quizTitle"
          v-model="quizTitle"
          class="input-title"
          placeholder="Quiz-Titel hier eingeben"
        />
      </section>

      <section class="quiz-questions-section card">
        <div class="questions-section-title-row">
          <h2 class="questions-section-title">Deine Quiz-Fragen</h2>
          <button class="plus-btn" type="button" @click="addQuestion" aria-label="Frage hinzufügen">
            <PlusIcon />
          </button>
        </div>
        <div
          v-for="(question, idx) in questions"
          :key="question.id"
          class="question-field question-interactive"
          @click="goToQuestion(question.id)"
          tabindex="0"
          @keydown.enter="goToQuestion(question.id)"
          @keydown.space="goToQuestion(question.id)"
        >
          <div class="question-header">
            <span class="question-index">{{ idx + 1 }}. Frage</span>
            <span class="question-type">{{ question.type }}</span>
          </div>
          <div class="question-preview">
            {{ question.text || `Fragetext für Frage ${idx + 1}` }}
          </div>
        </div>
      </section>

      <div class="edit-actions">
        <button class="btn btn-secondary" @click="goBack">
          <IconArrowLeft style="vertical-align: middle; margin-right: 5px;" />
          Zurück
        </button>
        <button class="btn btn-primary" @click="saveQuiz">
          Speichern
        </button>
      </div>
    </main>
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
.quiz-questions-section {
  margin-top: 10px;
}
.questions-section-title-row {
  display: flex;
  align-items: center;
  margin-bottom: 18px;
  gap: 10px;
}
.questions-section-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-accent, #1976d2);
  margin: 0;
}
.plus-btn {
  background: none;
  border: none;
  margin-left: 12px;
  cursor: pointer;
  padding: 3px 6px;
  display: flex;
  align-items: center;
  transition: background 0.15s;
  border-radius: 50%;
  min-width: 32px;
  min-height: 32px;
}
.plus-btn svg {
  display: block;
  width: 28px;
  height: 28px;
}
.plus-btn:hover,
.plus-btn:focus {
  background: #e3f2fd;
  outline: none;
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
  border: 1.5px solid #1976d2;
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
  color: var(--color-primary, #1976d2);
  font-size: 1.05rem;
}
.question-type {
  font-size: 0.97rem;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 6px;
  padding: 2px 10px;
}
.question-preview {
  font-size: 1.04rem;
  color: #333;
  padding: 6px 0 0 0;
}
.edit-actions {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  margin-top: 10px;
}
.btn {
  padding: 12px 22px;
  border-radius: 9px;
  border: none;
  font-size: 1.03rem;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.18s;
}
.btn-secondary {
  background: #f3f3f3;
  color: #1976d2;
  border: 1px solid #bcdffb;
}
.btn-secondary:hover {
  background: #e3f2fd;
}
.btn-primary {
  background: #1976d2;
  color: #fff;
}
.btn-primary:hover {
  background: #1565c0;
}
</style>