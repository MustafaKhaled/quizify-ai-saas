<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})
</script>

<template>
  <NuxtLayoutGroup>
    <NuxtPage />
  </NuxtLayoutGroup>
</template>
