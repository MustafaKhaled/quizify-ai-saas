<script setup lang="ts">
const props = defineProps<{
  error: {
    statusCode: number
    statusMessage: string
    message: string
  }
}>()

const handleError = () => clearError({ redirect: '/' })
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 p-4">
    <UCard class="max-w-md w-full">
      <div class="text-center">
        <h1 class="text-6xl font-bold mb-4">{{ props.error.statusCode }}</h1>
        <h2 class="text-2xl font-semibold mb-2">{{ props.error.statusMessage }}</h2>
        <p class="text-gray-500 mb-6">{{ props.error.message }}</p>
        <UButton @click="handleError">Go Home</UButton>
      </div>
    </UCard>
  </div>
</template>
