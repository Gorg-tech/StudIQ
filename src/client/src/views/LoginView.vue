<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const login = () => {
  router.push('/')
}
</script>

<template>
  <div class="login">
    <h1>Hier kommt das Login hin :P</h1>
    <button class="btn btn-primary" @click="login">
          <span>Zum Home</span>
    </button>
    <br>
    <button class="btn btn-secondary" @click="router.push('/register')">
          <span>Zur Registrierung</span>
    </button>
  </div>
</template>

<style>

</style>