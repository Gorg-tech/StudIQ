```vue name=ModuleOverview.vue
<script setup>
import { ref, onMounted, computed } from 'vue'
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
const moduleResponsible = ref('')
const moduleExams = ref('')

// convenience computed lists split by newlines or commas
const moduleResponsibleList = computed(() => {
  return (moduleResponsible.value || '')
    .split(/\r?\n|,\s*/)
    .map(s => s.trim())
    .filter(Boolean)
})

const moduleExamsList = computed(() => {
  const raw = (moduleExams.value || '').trim()
  if (!raw) return []

  // If the text contains explicit exam labels, split by these labels so
  // we keep the full description after each label intact.
  const labelRe = /(Schriftliche Prüfungsleistung|Alternative Prüfungsleistung|Mü?ndliche Prüfungsleistung)/i
  if (labelRe.test(raw)) {
    const reGlobal = /(Schriftliche Prüfungsleistung|Alternative Prüfungsleistung|Mü?ndliche Prüfungsleistung)[\s:\-]*/ig
    const matches = [...raw.matchAll(reGlobal)]
    if (matches.length) {
      const parts = []
      for (let i = 0; i < matches.length; i++) {
        const start = matches[i].index
        const end = (i + 1 < matches.length) ? matches[i + 1].index : raw.length
        const slice = raw.slice(start, end).trim()
        if (slice) parts.push(slice)
      }
      return parts
    }
  }

  // Fallback: split on newlines or commas
  return raw
    .split(/\r?\n|,\s*/)
    .map(s => s.trim())
    .filter(Boolean)
})

// Detect presence of the three exact exam type phrases (case-insensitive)
const hasSchriftliche = computed(() => {
  return moduleExamsList.value.some(e => /schriftliche\s*prüfungsleistung/i.test(e))
})

const hasAlternative = computed(() => {
  return moduleExamsList.value.some(e => /alternative\s*prüfungsleistung/i.test(e))
})

const hasMuendliche = computed(() => {
  return moduleExamsList.value.some(e => /mü?ndliche\s*prüfungsleistung/i.test(e))
})

const otherExams = computed(() => {
  const reS = /schriftliche\s*prüfungsleistung/i
  const reA = /alternative\s*prüfungsleistung/i
  const reM = /mü?ndliche\s*prüfungsleistung/i
  return moduleExamsList.value.filter(e => !reS.test(e) && !reA.test(e) && !reM.test(e))
})

// Extract trailing descriptions after the labels, e.g. "Schriftliche Prüfungsleistung: Klausur"
const schriftlicheDetails = computed(() => {
  const re = /schriftliche\s*prüfungsleistung\s*[:\-]?\s*/i
  return moduleExamsList.value
    .filter(e => re.test(e))
    .map(e => e.replace(re, '').trim())
    .filter(Boolean)
})

const alternativeDetails = computed(() => {
  const re = /alternative\s*prüfungsleistung\s*[:\-]?\s*/i
  return moduleExamsList.value
    .filter(e => re.test(e))
    .map(e => e.replace(re, '').trim())
    .filter(Boolean)
})

const muendlicheDetails = computed(() => {
  const re = /mü?ndliche\s*prüfungsleistung\s*[:\-]?\s*/i
  return moduleExamsList.value
    .filter(e => re.test(e))
    .map(e => e.replace(re, '').trim())
    .filter(Boolean)
})

// We keep a single exams list (`moduleExamsList`) and render it as bullets in one box.

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
  moduleName.value = modulData.name + ' (' + modulId + ')'
  // parse description to separate Verantwortlich and Prüfungen if present
  const rawDesc = modulData.description || `Dieses Modul behandelt grundlegende Themen für ${modulId}.`
  parseModuleDescription(rawDesc)
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
      moduleResponsible.value = ''
      moduleExams.value = ''
      moduleLink.value = 'https://www.htw-dresden.de/'
    })
})

// Helper: try to extract sections 'Verantwortlich:' and 'Prüfungen:' from a free-text description
// TODO: Backend sollte lieber Beschreibung in aufgeteilten Feldern schicken, dann ist es einfacher, evtl auch für zukünftige Filter
function parseModuleDescription(text) {
  const desc = text || ''
  // Look for the labels (case-insensitive)
  const idxResp = desc.search(/Verantwortlich:/i)
  const idxPruef = desc.search(/Prüfungen:|Prüfung:/i)

  if (idxResp === -1 && idxPruef === -1) {
    // nothing to split
    moduleDescription.value = desc
    moduleResponsible.value = ''
    moduleExams.value = ''
    return
  }

  // Determine order and slice accordingly
  let main = desc
  let resp = ''
  let pruef = ''

  if (idxResp !== -1 && idxPruef !== -1) {
    if (idxResp < idxPruef) {
      main = desc.slice(0, idxResp).trim()
      resp = desc.slice(idxResp + 'Verantwortlich:'.length, idxPruef).trim()
      pruef = desc.slice(idxPruef + (desc.slice(idxPruef).toLowerCase().startsWith('prüfungen:') ? 'Prüfungen:'.length : 'Prüfung:'.length)).trim()
    } else {
      main = desc.slice(0, idxPruef).trim()
      pruef = desc.slice(idxPruef + (desc.slice(idxPruef).toLowerCase().startsWith('prüfungen:') ? 'Prüfungen:'.length : 'Prüfung:'.length)).trim()
      resp = desc.slice(idxResp + 'Verantwortlich:'.length).trim()
    }
  } else if (idxResp !== -1) {
    main = desc.slice(0, idxResp).trim()
    resp = desc.slice(idxResp + 'Verantwortlich:'.length).trim()
  } else if (idxPruef !== -1) {
    main = desc.slice(0, idxPruef).trim()
    pruef = desc.slice(idxPruef + (desc.slice(idxPruef).toLowerCase().startsWith('prüfungen:') ? 'Prüfungen:'.length : 'Prüfung:'.length)).trim()
  }

  moduleDescription.value = main || ''
  moduleResponsible.value = resp || ''
  moduleExams.value = pruef || ''
}

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

        <div v-if="moduleResponsibleList.length" class="module-subsection">
          <h3 class="sub-title">Verantwortlich</h3>
          <ul class="sub-list">
            <li v-for="(person, idx) in moduleResponsibleList" :key="'resp-'+idx">{{ person }}</li>
          </ul>
        </div>

        <div v-if="moduleExamsList.length" class="module-subsection">
          <h3 class="sub-title">Prüfungen</h3>
          <ul class="sub-list">
            <li v-if="hasSchriftliche">
              Schriftliche Prüfungsleistung
              <span v-if="schriftlicheDetails.length">: {{ schriftlicheDetails.join(', ') }}</span>
            </li>
            <li v-if="hasAlternative">
              Alternative Prüfungsleistung
              <span v-if="alternativeDetails.length">: {{ alternativeDetails.join(', ') }}</span>
            </li>
            <li v-if="hasMuendliche">
              Mündliche Prüfungsleistung
              <span v-if="muendlicheDetails.length">: {{ muendlicheDetails.join(', ') }}</span>
            </li>
            <li v-if="otherExams.length">
              Weitere Prüfungen
              <ul>
                <li v-for="(exam, idx) in otherExams" :key="'other-'+idx">{{ exam }}</li>
              </ul>
            </li>
          </ul>
        </div>
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

.module-subsection {
  margin-top: 12px;
  padding: 12px;
  background: #fafcfe;
  border: 1px solid #eaf4ff;
  border-radius: 8px;
}
.sub-title {
  font-size: 0.98rem;
  font-weight: 700;
  color: var(--color-primary, #1976d2);
  margin: 0 0 8px 0;
}
.sub-list {
  margin: 0;
  padding-left: 1.05rem;
  color: #333;
}
.sub-list li {
  margin: 4px 0;
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
