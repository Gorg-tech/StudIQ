<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import LogoStudIQ from '@/components/LogoStudIQ.vue'

const router = useRouter()
const studiengang = ref(null)
const loading = ref(true)
const error = ref(null)

// Dummy Daten
const dummyStudiengang = {
  id: 'I41',  
  name: "Bachelor Informatik",
  semester: 6,
  department: "Informatik und Mathematik",
  degree: "Bachelor of Science",
  duration: 6,
  credits: 180,
  modules: [
    { id: "I128", name: "Programmierung 1", credits: 6 },
    { id: "I128", name: "Algorithmen und Datenstrukturen", credits: 6 },
    { id: "I128", name: "Mathematik für Informatiker", credits: 8 }
  ]
}

onMounted(async () => {
  try {
    // TODO: Scraper hier einbetten
    studiengang.value = dummyStudiengang
    loading.value = false
  } catch (err) {
    error.value = 'Fehler beim Laden des Studiengangs'
    console.error('Error loading Studiengang:', err)
  }
})

const goToModul = (modulId) => {
  router.push({ name: 'modul', params: { modulId: modulId }})  // Zeigt auf einzigstes Modul 
}
</script>

<template>
  <div class="studiengang-view">
    <div v-if="loading" class="loading">
      Laden...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="studiengang-content">
      <header class="studiengang-header">
        <LogoStudIQ class="logo" />
        <div class="studiengang-title">
          <h1>{{ studiengang.name }}</h1>
          <span class="studiengang-number">Studiengang-Nr: {{ studiengang.id }}</span>
        </div>
        <div class="studiengang-info">
          <p class="semester">{{ studiengang.semester }}. Semester</p>
          <p class="department">Fachbereich: {{ studiengang.department }}</p>
        </div>
      </header>

      <section class="studiengang-details">
        <h2>Studiengangdetails</h2>
        <div class="info-grid">
          <div class="info-item">
            <strong>Abschluss:</strong>
            <span>{{ studiengang.degree }}</span>
          </div>
          <div class="info-item">
            <strong>Regelstudienzeit:</strong>
            <span>{{ studiengang.duration }} Semester</span>
          </div>
          <div class="info-item">
            <strong>ECTS:</strong>
            <span>{{ studiengang.credits }} Credits</span>
          </div>
        </div>
      </section>

      <section class="module-list">
        <h2>Module</h2>
        <div v-if="studiengang.modules?.length" class="modules-grid">
          <div 
            v-for="modul in studiengang.modules" 
            :key="modul.id"
            class="module-card"
            @click="goToModul(modul.id)"
          >
            <h3>{{ modul.name }}</h3>
            <p>{{ modul.credits }} ECTS</p>
          </div>
        </div>
        <p v-else>Keine Module verfügbar</p>
      </section>
    </div>
  </div>
</template>

<style scoped>
.studiengang-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background: #fafafa;
}

.logo {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

.studiengang-header {
  margin-bottom: 2rem;
  border-bottom: 2px solid var(--color-primary, #1976d2);
  padding-bottom: 1rem;
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(25,118,210,0.1);
}

.studiengang-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: var(--color-primary, #1976d2);
}

.studiengang-info {
  display: flex;
  gap: 17rem;
  color: var(--color-muted, #666);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 1rem 0;
}

.info-item {
  background: #f7fbff;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e3f2fd;
  box-shadow: 0 1px 3px rgba(25,118,210,0.05);
}

.info-item strong {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--color-accent, #1565c0);
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.module-card {
  background: white;
  border: 1px solid #e3f2fd;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.module-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(25,118,210,0.15);
  border-color: var(--color-primary, #1976d2);
}

.module-card h3 {
  color: var(--color-primary, #1976d2);
  margin-bottom: 0.5rem;
}

.studiengang-number {
  color: var(--color-muted, #666);
  font-size: 1rem;
  padding: 0.4rem 0.8rem;
  background: #e3f2fd;
  border-radius: 8px;
  font-weight: 500;
}

section h2 {
  color: var(--color-accent, #1565c0);
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.studiengang-details, .module-list {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(25,118,210,0.1);
}
</style>