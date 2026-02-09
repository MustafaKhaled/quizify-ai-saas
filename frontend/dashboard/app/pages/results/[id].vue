<template>
  <div class="h-screen overflow-y-auto bg-gray-50 dark:bg-gray-900 px-6 py-12">
    <div class="max-w-4xl mx-auto">
      <!-- Loading State -->
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Results Display -->
      <div v-else-if="result" class="space-y-6">
        <!-- Header -->
        <div class="mb-4">
          <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-2">Quiz Results</h1>
          <p class="text-gray-600 dark:text-gray-400">
            Completed on {{ new Date(result.date).toLocaleDateString() }} at {{ new Date(result.date).toLocaleTimeString() }}
          </p>
        </div>

        <!-- Score Card -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-8 mb-6">
          <div class="text-center">
            <div class="text-6xl font-bold mb-4" :class="result.score >= 70 ? 'text-green-600' : 'text-red-600'">
              {{ Math.round(result.score) }}%
            </div>
            <div class="text-xl text-gray-900 dark:text-white mb-2">
              {{ result.score >= 70 ? '🎉 Passed!' : '😔 Failed' }}
            </div>
            <p class="text-gray-600 dark:text-gray-400">
              You answered {{ correctCount }} out of {{ result.breakdown.length }} questions correctly
            </p>
          </div>
        </div>

        <!-- Question Review -->
        <div class="space-y-4">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Question Review</h2>

          <div
            v-for="(item, index) in result.breakdown"
            :key="index"
            class="bg-white dark:bg-gray-800 rounded-lg shadow p-6"
            :class="item.is_correct ? 'border-l-4 border-green-500' : 'border-l-4 border-red-500'"
          >
            <div class="flex items-start justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex-1">
                Question {{ item.question_index + 1 }}
              </h3>
              <span
                class="px-3 py-1 rounded-full text-sm font-medium"
                :class="item.is_correct ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'"
              >
                {{ item.is_correct ? '✓ Correct' : '✗ Incorrect' }}
              </span>
            </div>

            <div class="space-y-3">
              <!-- User's Answer -->
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">Your Answer:</p>
                <p class="text-gray-900 dark:text-white">
                  {{ formatAnswer(item.user_choice) }}
                </p>
              </div>

              <!-- Correct Answer (if wrong) -->
              <div v-if="!item.is_correct">
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">Correct Answer:</p>
                <p class="text-green-700 dark:text-green-300 font-medium">
                  {{ formatAnswer(item.correct_answer) }}
                </p>
              </div>

              <!-- Explanation -->
              <div v-if="item.explanation" class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                <p class="text-sm font-medium text-blue-900 dark:text-blue-200 mb-1">Explanation:</p>
                <p class="text-blue-800 dark:text-blue-300">{{ item.explanation }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-8 flex gap-4">
          <NuxtLink to="/quizzes">
            <button class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors">
              ← Back to Quizzes
            </button>
          </NuxtLink>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="text-center py-12">
        <p class="text-red-600 dark:text-red-400 mb-4">Failed to load results</p>
        <NuxtLink to="/quizzes">
          <button class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            Back to Quizzes
          </button>
        </NuxtLink>
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

const result = ref<any>(null)
const isLoading = ref(true)

const getToken = () => typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null

const correctCount = computed(() => {
  if (!result.value?.breakdown) return 0
  return result.value.breakdown.filter((item: any) => item.is_correct).length
})

const formatAnswer = (answer: number | number[] | null | undefined) => {
  if (answer === null || answer === undefined) {
    return 'No answer provided'
  }
  if (Array.isArray(answer)) {
    return answer.length > 0 ? `Options: ${answer.map((a: number) => a + 1).join(', ')}` : 'No answer provided'
  }
  return `Option ${answer + 1}`
}

onMounted(async () => {
  try {
    const token = getToken()
    const resultId = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id

    const response = await fetch(`${config.public.apiBase}/quizzes/result/${resultId}/review`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      }
    })

    if (response.ok) {
      result.value = await response.json()
    } else {
      console.error('Failed to load results:', response.status)
    }
  } catch (error) {
    console.error('Failed to load result:', error)
  } finally {
    isLoading.value = false
  }
})
</script>
