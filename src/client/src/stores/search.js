import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSearchStore = defineStore('search', () => {
  const searchQuery = ref('')
  const activeFilter = ref('alle')
  const results = ref({})
  const searchCache = ref(new Map())

  function saveToCache(cacheKey, data) {
    searchCache.value.set(cacheKey, data)
  }

  function getCachedResults(cacheKey) {
    return searchCache.value.get(cacheKey)
  }

  function hasCache(cacheKey) {
    return searchCache.value.has(cacheKey)
  }

  return {
    searchQuery,
    activeFilter,
    results,
    searchCache,
    saveToCache,
    getCachedResults,
    hasCache
  }
})
