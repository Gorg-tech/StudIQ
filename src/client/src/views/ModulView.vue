```vue name=ModuleOverview.vue
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { createLernset } from '@/services/lernsets'
import { getModul } from '@/services/modules' 
import IconLink from '@/components/icons/IconLink.vue'
import IconPlus from '@/components/icons/IconPlus.vue'


const router = useRouter()
const route = useRoute()

const moduleName = ref('')
const moduleDescription = ref('')
const moduleLink = ref('')

const lernsets = ref([])

const showNewLernsetModal = ref(false)
const showConfirmModal = ref(false)
const newLernsetTitle = ref('')
const newLernsetDescription = ref('')
const pendingLernsetTitle = ref('')
const pendingLernsetDescription = ref('')

const goToLernset = (lernsetId) => {
  router.push({ name: 'lernset', params: { lernsetId } })
}

const handleOpenNewLernsetModal = () => {
  newLernsetTitle.value = ''
  newLernsetDescription.value = ''
  showNewLernsetModal.value = true
}

const handleCloseNewLernsetModal = () => {
  showNewLernsetModal.value = false
  newLernsetTitle.value = ''
  newLernsetDescription.value = ''
}

const handleShowConfirmModal = () => {
  pendingLernsetTitle.value = newLernsetTitle.value
  pendingLernsetDescription.value = newLernsetDescription.value
  showNewLernsetModal.value = false
  showConfirmModal.value = true
}

const handleCloseConfirmModal = () => {
  showConfirmModal.value = false
  pendingLernsetTitle.value = ''
  pendingLernsetDescription.value = ''
}

const handleCreateLernset = (title, description) => {
  // API-Call
  // id, title, description, modul
  const newSet = {
    title: title,
    description: description,
    modul: route.params.modulId // Use dynamic modulId
  }

  const newLernset = createLernset(newSet)
  newLernset
    .then(response => {
      // console.log('Lernset erstellt:', response)
      lernsets.value.push({
        id: response.id,
        title: response.title,
        quizCount: 0
      })
      handleCloseConfirmModal()
    })
    .catch(error => {
      console.error('Fehler beim Erstellen des Lernsets:', error)
    })

}

onMounted(() => {
  const modulId = route.params.modulId
  
  getModul(modulId)
    .then(modulData => {
      moduleName.value = modulData.name || `Modul ${modulId}`
      moduleDescription.value = modulData.description || `Dieses Modul behandelt grundlegende Themen für ${modulId}.`
      moduleLink.value = modulData.modulux_url || 'https://apps.htw-dresden.de/modulux/frontend/module/'
      
      // Check if lernsets data exists in the response
      if (modulData.lernsets && Array.isArray(modulData.lernsets)) {
        lernsets.value = modulData.lernsets.map(set => ({
          id: set.id,
          title: set.title,
          quizCount: set.quiz_count || 0
        }));
      } else {
        // If no lernsets in the response, initialize with an empty array
        lernsets.value = [];
        console.log('No lernsets data found in module response');
      }
    })
    .catch(error => {
      console.error('Fehler beim Laden des Moduls:', error)
      // Fall back to placeholder data if API call fails
      moduleName.value = `Modul ${modulId}`
      moduleDescription.value = `Dieses Modul behandelt grundlegende Themen für ${modulId}.`
      moduleLink.value = 'https://www.htw-dresden.de/'
    })
})

</script>

<template>
  <div class="module-overview">
    <header class="module-header">
      <div class="module-title-block">
        <h1 class="module-title">{{ moduleName }}</h1>
        <a
          class="link-btn"
          :href="moduleLink"
          target="_blank"
          rel="noopener"
          aria-label="Modul-Link öffnen"
        >
          <IconLink />
        </a>
      </div>
      <div class="module-desc-block">
        <h2 class="desc-title">Modulbeschreibung</h2>
        <p class="module-description">{{ moduleDescription }}</p>
      </div>
    </header>

    <main>
      <section class="lernsets-section card">
        <div class="lernsets-title-row">
          <h2 class="lernsets-title">Lernsets</h2>
          <button class="plus-btn" @click="handleOpenNewLernsetModal" aria-label="Neues Lernset erstellen">
            <IconPlus />
          </button>
        </div>
        <div class="lernsets-list">
          <div
            v-for="set in lernsets"
            :key="set.id"
            class="lernset-item"
            @click="goToLernset(set.id)"
            tabindex="0"
            @keydown.enter="goToLernset(set.id)"
            @keydown.space="goToLernset(set.id)"
          >
            <span class="lernset-title">{{ set.title }}</span>
            <span class="lernset-quiz-count">{{ set.quizCount }} Quizze</span>
          </div>
        </div>
      </section>
    </main>

    <!-- Modal: Neues Lernset erstellen -->
    <div v-if="showNewLernsetModal" class="modal-overlay">
      <div class="modal-content">
        <h3>Neues Lernset erstellen</h3>
        <input
          v-model="newLernsetTitle"
          class="lernset-input"
          placeholder="Lernset-Name"
          @keyup.enter="newLernsetTitle.trim() ? handleShowConfirmModal() : null"
        />
        <textarea
          v-model="newLernsetDescription"
          class="lernset-input"
          placeholder="Lernset-Beschreibung (optional)"
          rows="3"
        ></textarea>
        <div class="modal-actions">
          <button class="modal-btn" @click="handleShowConfirmModal" :disabled="!newLernsetTitle.trim()">Erstellen</button>
          <button class="modal-btn cancel" @click="handleCloseNewLernsetModal">Abbruch</button>
        </div>
      </div>
    </div>
    <!-- Modal: Bestätigung -->
    <div v-if="showConfirmModal" class="modal-overlay">
      <div class="modal-content">
        <h3>Lernset wirklich erstellen?</h3>
        <p>Möchtest du das Lernset <b>{{ pendingLernsetTitle }}</b> wirklich erstellen?</p>
        <div class="modal-actions">
          <button class="modal-btn" @click="handleCreateLernset(pendingLernsetTitle, pendingLernsetDescription)">Ja, erstellen</button>
          <button class="modal-btn cancel" @click="handleCloseConfirmModal">Abbruch</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.module-overview {
  max-width: 700px;
  margin: 0 auto;
  padding: 28px 16px 0 16px;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.module-header {
  margin-bottom: 16px;
}

.module-title-block {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.module-title {
  font-size: 2.15rem;
  font-weight: 700;
  color: var(--color-primary, #1976d2);
  margin: 0;
  line-height: 1.1;
}

.link-btn {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  padding: 0 0 0 12px;
  color: var(--color-accent, #1976d2);
  cursor: pointer;
  font-size: 1.5rem;
  transition: color 0.18s;
  text-decoration: none;
}
.link-btn:hover,
.link-btn:focus {
  color: #1565c0;
}

.module-desc-block {
  margin-top: 10px;
}
.desc-title {
  font-size: 1.17rem;
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--color-accent, #1976d2);
}
.module-description {
  font-size: 1.05rem;
  color: #222;
  margin-top: 0;
}

.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
  padding: 22px 20px;
}

.lernsets-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 8px;
}

.lernsets-title {
  font-size: 1.13rem;
  font-weight: 600;
  color: var(--color-accent, #1976d2);
  margin-bottom: 0;
}

.plus-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: var(--color-primary, #1976d2);
  display: flex;
  align-items: center;
  transition: color 0.18s;
}
.plus-btn:hover,
.plus-btn:focus {
  color: #1565c0;
}
.plus-btn svg {
  width: 2rem;
  height: 2rem;
}

.lernsets-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.lernset-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f7fbff;
  border-radius: 8px;
  padding: 13px 16px;
  font-size: 1.08rem;
  box-shadow: 0 1px 3px rgba(25,118,210,0.03);
  border: 1px solid #e3f2fd;
  cursor: pointer;
  transition: border 0.15s, box-shadow 0.15s;
}
.lernset-item:hover, .lernset-item:focus {
  border: 1.5px solid #1976d2;
  box-shadow: 0 2px 10px 2px rgba(25, 118, 210, 0.08);
  background: #f2f8fd;
}

.lernset-title {
  font-weight: 500;
  color: #1976d2;
}
.lernset-quiz-count {
  font-size: 0.97rem;
  color: #555;
  font-weight: 400;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  z-index: 1000;
  inset: 0;
  background: rgba(36, 44, 53, 0.23);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: #fff;
  border-radius: 12px;
  padding: 28px 24px 20px 24px;
  min-width: 300px;
  box-shadow: 0 4px 30px 0 rgba(25, 118, 210, 0.13);
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 18px;
}
.lernset-input {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1.2px solid #e3f2fd;
  font-size: 1.06rem;
  margin-top: 6px;
  margin-bottom: 8px;
  outline: none;
  transition: border 0.15s;
}
.lernset-input:focus {
  border: 1.5px solid #1976d2;
}
.modal-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}
.modal-btn {
  padding: 7px 18px;
  border-radius: 6px;
  border: none;
  background: #1976d2;
  color: #fff;
  font-weight: 500;
  font-size: 1.01rem;
  cursor: pointer;
  transition: background 0.17s;
}
.modal-btn:disabled {
  background: #b0c4d8;
  cursor: not-allowed;
}
.modal-btn.cancel {
  background: #e0e0e0;
  color: #555;
}
</style>
```
