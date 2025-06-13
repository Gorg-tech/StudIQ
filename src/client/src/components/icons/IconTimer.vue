<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke-linecap="round"
    stroke-linejoin="round"
    stroke-width="2"
  >
    <circle cx="12" cy="12" r="10" stroke="#ff9800" fill="#fff3e0" />
    <path
      d="M12 6v6l4 2"
      stroke="#ff9800"
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
      default: '#ff9800',
    },
  },
}
</script>