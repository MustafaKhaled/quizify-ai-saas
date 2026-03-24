<script setup lang="ts">
defineProps<{
  collapsed?: boolean
}>()
</script>

<template>
  <NuxtLink to="/dashboard" class="flex items-center gap-2 px-2 py-1.5 min-w-0">
    <AppLogo class="h-6 w-auto shrink-0" :class="collapsed ? 'mx-auto' : ''" />
  </NuxtLink>
</template>
