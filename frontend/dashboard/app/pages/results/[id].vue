<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="max-w-4xl mx-auto px-4 py-12">
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <div v-else-if="result" class="space-y-6">
        <!-- Score Summary -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-8 text-center">
          <div class="mb-6">
            <div class="text-6xl font-bold mb-4" :class="result.is_passed ? 'text-green-600' : 'text-red-600'">
              {{ Math.round(result.score_percentage) }}%
            </div>
            <h2 class="text-2xl font-bold" :class="result.is_passed ? 'text-green-600' : 'text-red-600'">
              {{ result.is_passed ? 'Great Job!' : 'Try Again' }}
            </h2>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-6 text-left">
            <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded">
              <p class="text-sm text-gray-600 dark:text-gray-400">Score Percentage</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ Math.round(result.score_percentage) }}%</p>
            </div>
            <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded">
              <p class="text-sm text-gray-600 dark:text-gray-400">Time Taken</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ formatTime(result.time_taken_seconds) }}</p>
            </div>
          </div>

          <div class="flex gap-4 justify-center">
            <NuxtLink to="/quizzes">
              <button class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Back to Quizzes
              </button>
            </NuxtLink>
            <NuxtLink :to="`/quiz/${result.quiz_id}`">
              <button class="px-6 py-2 bg-gray-300 dark:bg-gray-600 text-gray-900 dark:text-white rounded-lg hover:bg-gray-400 transition-colors">
                Retake Quiz
              </button>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const route = useRoute()
const config = useRuntimeConfig()
const { $fetch } = useNuxtApp()

const result = ref<any>(null)
const isLoading = ref(true)

const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}m ${secs}s`
}

onMounted(async () => {
  try {
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
    // Parse the result ID from the route
    const resultId = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id
    
    result.value = await $fetch(`${config.public.apiBase}/results/${resultId}`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
  } catch (error) {
    console.error('Failed to load result:', error)
  } finally {
    isLoading.value = false
  }
})
</script>
