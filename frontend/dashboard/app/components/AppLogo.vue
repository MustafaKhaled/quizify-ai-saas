<script setup lang="ts">
defineProps<{
  collapsed?: boolean
}>()
</script>

<template>
  <img
    v-if="collapsed"
    :src="'/quizify_icon.png'"
    alt="Quizify AI"
    class="h-24 w-24 object-contain"
  />
  <img
    v-else
    :src="'/quizify_ai_logo.png'"
    alt="Quizify AI"
    class="h-24 w-auto object-contain"
  />
</template>
