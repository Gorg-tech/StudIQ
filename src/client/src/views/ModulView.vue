```vue name=ModuleOverview.vue
Beschreibung: View der Modulübersicht mit Details und Lernsets
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
const moduleDozent = ref('')
const moduleExams = ref('')

/**
 * Parses a raw exam description string into a structured list of exam entries. 
 * Spliting by Exam-Labels
 * 
 * @param {string} rawValue
 *        The raw exam description text
 *
 * @returns {string[]}
 *          A cleaned list of exam descriptions with Exam Type and Description
 */
function parseExamList(rawValue) {

  const labelRe = /(Schriftliche Prüfungsleistung|Alternative Prüfungsleistung|Mü?ndliche Prüfungsleistung)/i

  if (labelRe.test(rawValue)) {
    const reGlobal = /(Schriftliche Prüfungsleistung|Alternative Prüfungsleistung|Mü?ndliche Prüfungsleistung)[\s:\-]*/ig
    const matches = [...rawValue.matchAll(reGlobal)]

    if (matches.length) {
      const parts = []
      for (let i = 0; i < matches.length; i++) {
        const start = matches[i].index
        const end = (i + 1 < matches.length) ? matches[i + 1].index : rawValue.length
        const slice = rawValue.slice(start, end).trim()
        if (slice) parts.push(slice)
      }
      return parts
    }
  }
  // fallback: split by newlines/commas
  return rawValue
    .split(/\r?\n|,\s*/)
    .map(s => s.trim())
    .filter(Boolean)
}

// convenience computed lists split by newlines or commas
const moduleDozentList = computed(() => {
  return (moduleDozent.value || '')
    .split(/\r?\n|,\s*/)
    .map(s => s.trim())
    .filter(Boolean)
})

const moduleExamsList = computed(() => {
  console.info("Exams: " + moduleExams.value)
  const raw = (moduleExams.value || '').trim()
  if (!raw) 
    return []
  return parseExamList(moduleExams.value)
})

const EXAM_TYPES = {
  schriftliche: /schriftliche\s*prüfungsleistung/i,
  alternative: /alternative\s*prüfungsleistung/i,
  mündliche: /mü?ndliche\s*prüfungsleistung/i
}

/**
 * Checks if a given exam type is present in the moduleExamsList.
 *
 * @param {RegExp} regex - Case-insensitive regex matching "Schriftliche Prüfungsleistung" etc.
 * @returns {boolean} IsPresent?
 */
function hasExamType(regex) {
  return moduleExamsList.value.some(e => regex.test(e))
}
 
const hasSchriftliche = computed(() => hasExamType(EXAM_TYPES.schriftliche))
const hasAlternative  = computed(() => hasExamType(EXAM_TYPES.alternative))
const hasMuendliche   = computed(() => hasExamType(EXAM_TYPES.mündliche))

//Falls keine der Labels passt, Zusammenfassen in otherExams
const otherExams = computed(() => {
  const reS = /schriftliche\s*prüfungsleistung/i
  const reA = /alternative\s*prüfungsleistung/i
  const reM = /mü?ndliche\s*prüfungsleistung/i
  return moduleExamsList.value.filter(e => !reS.test(e) && !reA.test(e) && !reM.test(e))
})

/**
 * Extracts details after a given exam type label.
 * Example: "Schriftliche Prüfungsleistung: Klausur"
 *
 * @param {RegExp} regex - Regex matching the exam label including optional suffixes.
 * @returns {string[]} ExamDetails
 */
function extractExamDetails(regex) {
  const detailRegex = new RegExp(regex.source + "\\s*[:\\-]?\\s*", "i")

  return moduleExamsList.value
    .filter(e => detailRegex.test(e))
    .map(e => e.replace(detailRegex, '').trim())
    .filter(Boolean)
}

const schriftlicheDetails = computed(() => extractExamDetails(EXAM_TYPES.schriftliche))
const alternativeDetails  = computed(() => extractExamDetails(EXAM_TYPES.alternative))
const muendlicheDetails   = computed(() => extractExamDetails(EXAM_TYPES.mündliche))

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

/**
 * 
 * @param {string} title Lernset-Title 
 * @param {string} description Lernset-Description
 */
async function handleCreateLernset(title, description) {

  //Contente of API-Call
  const payload = {
    title,
    description,
    modul: route.params.modulId
  }

  const onSuccess = (data) => {
    lernsets.value.push({
      id: data.id,
      title: data.title,
      quizCount: 0
    })
    handleCloseConfirmModal()
  }

  try {
    const response = await createLernset(payload)
    onSuccess(response)
  } 
  catch (err) {
    console.error("Fehler beim Erstellen des Lernsets:", err)
  }
}

/**
 * Loads module data, populates UI state handles Lernset extraction.
 *  - Handles API errors by applying fallback values
 *
 * @async
 * @function loadModuleData
 *
 * @returns {Promise<void>}
 *          Resolves once all module data has been loaded and mapped into
 *          reactive UI state variables.
 */
async function loadModuleData() {
  const modulId = route.params.modulId
  
  try {
    const modulData = await getModul(modulId)

    moduleName.value = modulData.name + ' (' + modulId + ')'
    moduleDozent.value = modulData.dozent_name || 'Unbekannter Dozent'
    moduleExams.value = modulData.examinations || 'Keine Prüfungen erkannt'
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
  }
  catch(error){
    console.error('Fehler beim Laden des Moduls:', error)
    // Fall back to placeholder data if API call fails
    moduleName.value = `Modul ${modulId}`
    moduleDescription.value = `Dieses Modul behandelt grundlegende Themen für ${modulId}.`
    moduleDozent.value = ''
    moduleExams.value = ''
    moduleLink.value = 'https://www.htw-dresden.de/'
  }

}

onMounted(() => {
  loadModuleData()
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

        <div v-if="moduleDozentList.length" class="module-subsection">
          <h3 class="sub-title">Verantwortlich</h3>
          <ul class="sub-list">
            <li v-for="(person, idx) in moduleDozentList" :key="'resp-'+idx">{{ person }}</li>
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
  color: var(--color-text);
  margin-top: 0;
}

.module-subsection {
  margin-top: 12px;
  padding: 12px;
  background: var(--color-bg-light);
  border: 1px solid var(--color-border);
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
  color: var(--color-text);
}
.sub-list li {
  margin: 4px 0;
}

.card {
  background: var(--card-bg);
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
  background: var(--color-bg-light);
  border-radius: 8px;
  padding: 13px 16px;
  font-size: 1.08rem;
  box-shadow: 0 1px 3px rgba(25,118,210,0.03);
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: border 0.15s, box-shadow 0.15s;
}
.lernset-item:hover, .lernset-item:focus {
  border: 1.5px solid var(--color-secondary);
  box-shadow: 0 2px 10px 2px rgba(25, 118, 210, 0.08);
  background: var(--color-bg-hover);
}

.lernset-title {
  font-weight: 500;
  color: var(--color-secondary);
}
.lernset-quiz-count {
  font-size: 0.97rem;
  color: var(--color-muted);
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
  background: var(--card-bg);
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
  border: 1.2px solid var(--color-border);
  font-size: 1.06rem;
  margin-top: 6px;
  margin-bottom: 8px;
  outline: none;
  transition: border 0.15s;
  background: var(--card-bg);
  color: var(--color-text);
}
.lernset-input:focus {
  border: 1.5px solid var(--color-secondary);
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
