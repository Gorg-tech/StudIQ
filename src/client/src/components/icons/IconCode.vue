<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
  >
    <path 
      d="M16 18l6-6-6-6M8 6l-6 6 6 6" 
      :stroke="color" 
      stroke-width="2" 
      stroke-linecap="round" 
      stroke-linejoin="round" 
    />
  </svg>
</template>

<script>
export default {
  props: {
    color: {
      type: String,
      default: '#2196f3'
    }
  }
}
</script>