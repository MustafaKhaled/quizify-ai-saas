<script setup lang="ts">
defineProps<{
  collapsed?: boolean
}>()
</script>

<template>
  <NuxtLink to="/dashboard" class="flex items-center px-2 py-1.5 min-w-0">
    <AppLogo :collapsed="collapsed" />
  </NuxtLink>
</template>
