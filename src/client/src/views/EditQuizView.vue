<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import LogoStudIQ from '@/components/LogoStudIQ.vue'
//import Penguin from '@/components/Penguin.vue' 
import IconFlame from '@/components/icons/IconFlame.vue'
import IconSearch from '@/components/icons/IconSearch.vue'
import IconTimer from '@/components/icons/IconTimer.vue'
import IconCode from '@/components/icons/IconCode.vue'
import IconChart from '@/components/icons/IconChart.vue'
const router = useRouter()
</script>
<template>
  <div class="editQuiz">
    <header class="editQuiz-header">
      <div class="logo-container">
        <h2>
          <LogoStudIQ />
        </h2>
      </div>
      <button class="btn editQuest" @click="router.push('/editQuestion')">
          <span class="btn-icon"><IconSearch /></span>
          <span>Quiz suchen</span>
      </button>
      <h1>Quiz bearbeiten</h1>
      Hier kannst du ein neues Quiz erstellen oder Bearbeiten
    </header>
    
    <body>
      <h1>Dein Quiz-Titel</h1>
      <div class="questions">
        <input id="quizTitle" type="" value="Dynamisches Label">
      </div>
    </body>
  </div>
</template>

<style>
  
</style>

