<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import LogoStudIQ from '@/components/LogoStudIQ.vue'

// API
import { getStudiengangById } from '@/services/studiengaenge'

const route = useRoute()
const router = useRouter()

const studiengang = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const studiengangId = route.params.studiengangId
    const sg = await getStudiengangById(studiengangId)
    console.log('Studiengang data:', sg)
    // Beschreibung parsen
    if (sg.description) {
      const degreeMatch = sg.description.match(/Abschluss:\s*([^,]+)/)
      const durationMatch = sg.description.match(/Regelstudienzeit:\s*(\d+)\s*Semester/)

      sg.degree = degreeMatch ? degreeMatch[1].trim() : ''
      sg.duration = durationMatch ? Number(durationMatch[1]) : null
    } else console.error('Description error')

    studiengang.value = sg
  } catch (err) {
    console.error('Error loading Studiengang:', err)
    error.value = 'Fehler beim Laden des Studiengangs'
  } finally {
    loading.value = false
  }
})

const goToModul = (modulId) => {
  router.push({ name: 'modul', params: { modulId } })
}
</script>

<template>
  <div class="studiengang-view">
    <div v-if="loading" class="loading">Laden...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="studiengang-content">
      <header class="studiengang-header">
        <LogoStudIQ class="logo" />

        <div class="studiengang-title">
          <h1>{{ studiengang?.name }}</h1>
          <span class="studiengang-number">Studiengang-Nr: {{ studiengang?.id }}</span>
        </div>

        <!-- Beschreibung -->
        <p class="studiengang-description" v-if="studiengang?.description">
          {{ studiengang.description }}
        </p>

        <!-- Modulux-Link -->
        <a
          v-if="studiengang?.modulux_url"
          :href="studiengang.modulux_url"
          target="_blank"
          class="modulux-link"
        >
          Modulux öffnen
        </a>

        <div class="studiengang-info">
          <p class="semester" v-if="studiengang?.semester">{{ studiengang.semester }}. Semester</p>
          <p class="department" v-if="studiengang?.department">
            Fachbereich: {{ studiengang.department }}
          </p>
        </div>
      </header>

      <section class="studiengang-details">
        <h2>Studiengangdetails</h2>
        <div class="info-grid">
          <div class="info-item" v-if="studiengang?.degree">
            <strong>Abschluss:</strong>
            <span>{{ studiengang.degree }}</span>
          </div>

          <div class="info-item" v-if="studiengang?.duration">
            <strong>Regelstudienzeit:</strong>
            <span>{{ studiengang.duration }} Semester</span>
          </div>

          <div class="info-item" v-if="studiengang?.credits">
            <strong>ECTS:</strong>
            <span>{{ studiengang.credits }} Credits</span>
          </div>
        </div>
      </section>

      <section class="module-list" v-if="studiengang?.module?.length">
        <h2>Module</h2>
        <div class="modules-grid">
          <div
            v-for="modul in studiengang.module"
            :key="modul.modulId"
            class="module-card"
            @click="goToModul(modul.modulId)"
          >
            <h3>{{ modul.name }}</h3>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.studiengang-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.logo {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

.studiengang-header {
  margin-bottom: 2rem;
  border-bottom: 2px solid var(--color-primary);
  padding-bottom: 1rem;
  background: var(--card-bg);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.1);
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
  background: var(--color-bg-light);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  box-shadow: 0 1px 3px rgba(25, 118, 210, 0.05);
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
  background: var(--card-bg);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.module-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.15);
  border-color: var(--color-primary, #1976d2);
}

.module-card h3 {
  color: var(--color-primary, #1976d2);
  margin-bottom: 0.5rem;
}

.studiengang-number {
  color: var(--color-muted);
  font-size: 1rem;
  padding: 0.4rem 0.8rem;
  background: var(--color-bg-light);
  border-radius: 8px;
  font-weight: 500;
}

.studiengang-description {
  margin: 1rem 0;
  color: var(--color-muted);
}

.modulux-link {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: var(--color-primary);
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
}

section h2 {
  color: var(--color-accent, #1565c0);
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.studiengang-details,
.module-list {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.1);
}
</style>
