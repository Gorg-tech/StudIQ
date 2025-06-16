<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import IconSettings from '@/components/icons/IconSettings.vue'
import LogoStudIQ from '@/components/LogoStudIQ.vue'
import Penguin from '@/components/Penguin.vue' 
import IconFlame from '@/components/icons/IconFlame.vue'
import IconLeaderboard from '@/components/icons/IconLeaderboard.vue'
import IconSearch from '@/components/icons/IconSearch.vue'
import IconTimer from '@/components/icons/IconTimer.vue'
import IconCode from '@/components/icons/IconCode.vue'
import IconChart from '@/components/icons/IconChart.vue'
const router = useRouter()
</script>
<template>
  <div class="editQuiz">
    <header class="app-header">
      <div class="logo-container">
        <h1>
          <LogoStudIQ />
        </h1>
        <p class="tagline">Dein Begleiter für die Prüfungsvorbereitung</p>
      </div>
      <button class="btn editQuest" @click="router.push('/editQuestion')">
          <span class="btn-icon"><IconSearch /></span>
          <span>Quiz suchen</span>
      </button>
    </header>
    <h1>Hier kommt das Quiz bearbeiten hin :P</h1>
  </div>
</template>

<style>
  
</style>

