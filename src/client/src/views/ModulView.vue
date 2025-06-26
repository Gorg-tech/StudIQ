<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import IconLink from '@/components/icons/IconLink.vue'

const router = useRouter()

// Beispiel-Daten für das Modul und Lernsets
const moduleName = ref('Diskrete Mathematik')
const moduleDescription = ref('Dieses Modul behandelt grundlegende Themen der diskreten Mathematik wie Mengen, Relationen, Graphen, Kombinatorik und mehr.')
const moduleLink = ref('https://beispiel-universitaet.de/module/diskrete-mathematik')

const lernsets = ref([
  { id: 1, title: 'Definitionen', quizCount: 5 },
  { id: 2, title: 'Beweisaufgaben', quizCount: 3 },
  { id: 3, title: 'Kombinatorik', quizCount: 4 },
  { id: 4, title: 'Graphentheorie', quizCount: 2 },
])

const goToLernset = (lernsetId) => {
  // Du kannst auch lernsetId im Pfad übergeben, z.B. `/lernset-view/${lernsetId}`
  router.push('/lernset-overview/')
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
      </div>
    </header>

    <main>
      <section class="lernsets-section card">
        <h2 class="lernsets-title">Lernsets</h2>
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

.lernsets-title {
  font-size: 1.13rem;
  font-weight: 600;
  color: var(--color-accent, #1976d2);
  margin-bottom: 16px;
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
</style>