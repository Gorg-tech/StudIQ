<script setup>
import { RouterView } from 'vue-router'
import BottomNavigation from './components/layout/BottomNavigation.vue'
import apiClient from '@/services/api/client'

apiClient.ensureCsrf()
</script>

<template>
  <div class="app-container">
    <main class="content">
      <RouterView />
    </main>
    <BottomNavigation />
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Ubuntu:wght@300;400;500;700&display=swap');

:root {
  --color-accent: #222;
  --color-bg: #f5f5f5;
  --color-bg-hover: #f5f5f5;
  --color-bg-light: #f9f9f9;
  --color-blue: #2196f3;
  --color-blue-dark: #1976d2;
  --color-border: #eee;
  --color-border-dark: #ddd;
  --color-green: #4caf50;
  --color-muted: #666;
  --color-primary: #fc7960;
  --color-red: #f44336;
  --color-secondary: #2196f3;
  --color-shadow: 0 2px 8px rgba(34,34,34,0.08);
  --color-text: #333;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Ubuntu', 'Roboto', 'Helvetica Neue', sans-serif;
  color: #333;
  background-color: #f5f5f5;
}

/* Override grid on #app */
#app {
  display: flex !important;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 1.5rem;
  padding-top: 0.8rem;
  font-family: 'Ubuntu', 'Roboto', 'Helvetica Neue', sans-serif;
}

.app-container {
  min-height: 100vh;
  position: relative;
  padding-bottom: 70px; /* Space for bottom navigation */
  width: 100%;
}

.content {
  max-width: 1200px;
  margin: 0 auto;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.btn-icon {
  display: flex;
  align-items: center;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-secondary {
  background-color: transparent;
  color: var(--color-secondary);
  border: 1px solid #bcdffb;
}

.btn-text {
  background-color: transparent;
  color: var(--color-primary);
}

/* Hover effects */
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  filter: brightness(0.93);
}

.btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn-secondary:hover {
  background-color: #e3f2fd;
}

.btn-text:hover {
  background-color: rgba(255, 75, 40, 0.1);
}

.btn:disabled {
  cursor: not-allowed;
}

.btn-primary:disabled {
  background-color: #b0bec5;
}


/* Icon Button */
.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  min-width: 32px;
  min-height: 32px;
}

.btn-icon:hover,
.btn-icon:focus {
  background-color: #e3f2fd;
  outline: none;
}

@media (min-width: 1024px) {
  .app-container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .content {
    width: 100%;
    padding: 24px;
  }
}
</style>