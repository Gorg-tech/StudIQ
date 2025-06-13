<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
  >
    <rect x="3" y="12" width="4" height="8" :fill="color" />
    <rect x="10" y="8" width="4" height="12" :fill="color" />
    <rect x="17" y="4" width="4" height="16" :fill="color" />
  </svg>
</template>

<script>
export default {
  props: {
    color: {
      type: String,
      default: '#4caf50'
    }
  }
}
</script>