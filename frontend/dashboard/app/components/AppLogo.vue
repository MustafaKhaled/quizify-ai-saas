<script setup lang="ts">
defineProps<{
  collapsed?: boolean
}>()
</script>

<template>
  <img
    v-if="collapsed"
    :src="'/logo-icon.png'"
    alt="Quizify AI"
    class="h-8 w-8 object-contain"
  />
  <img
    v-else
    :src="'/logo-full.png'"
    alt="Quizify AI"
    class="h-8 w-auto object-contain"
  />
</template>
