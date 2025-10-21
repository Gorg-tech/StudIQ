<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.push('/')
}
</script>

<template> 
  <div class="edit-quiz-view">
    <header class="edit-header">
      <h1>Einstellungen</h1>
    </header>

    <main class="edit-main">
      <section class="quiz-title-section card">
        <label class="block-label">Allgemein</label>
        <div style="margin-top: 10px;">
          <p>• Benutzername: <b>DemoUser</b></p>
          <p>• Sprache: <b>Deutsch</b></p>
        </div>
      </section>

      <section class="quiz-questions-section card">
        <h2 class="questions-section-title">Darstellung</h2>
        <div style="margin-top: 10px;">
          <p>• Dunkelmodus: <b>Deaktiviert</b></p>
          <p>• Große Schrift: <b>Aktiviert</b></p>
        </div>
      </section>

      <section class="quiz-questions-section card">
        <h2 class="questions-section-title">Benachrichtigungen</h2>
        <div style="margin-top: 10px;">
          <p>• E-Mail-Benachrichtigungen: <b>Aktiviert</b></p>
          <p>• Push-Benachrichtigungen: <b>Deaktiviert</b></p>
        </div>
      </section>

      <div class="edit-actions">
        <button class="btn btn-secondary" @click="goBack">
          Zurück
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
.questions-section-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-accent);
  margin: 0;
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
</style>
