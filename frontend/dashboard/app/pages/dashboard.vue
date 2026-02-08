<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
    <div class="w-full px-4 py-16">
      <!-- Hero Section -->
      <div class="text-center mb-16">
        <h1 class="text-5xl font-bold text-gray-900 dark:text-white mb-4">Welcome to Quizify</h1>
        <p class="text-xl text-gray-600 dark:text-gray-400 mb-8">AI-powered quiz generation from your PDFs</p>
        <NuxtLink to="/quiz-new">
          <button class="px-8 py-3 bg-blue-600 text-white text-lg rounded-lg hover:bg-blue-700 transition-colors font-semibold">
            Create Your First Quiz
          </button>
        </NuxtLink>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
          <p class="text-gray-600 dark:text-gray-400 text-sm mb-2">Total Quizzes</p>
          <p class="text-4xl font-bold text-gray-900 dark:text-white">{{ stats.totalQuizzes }}</p>
        </div>
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
          <p class="text-gray-600 dark:text-gray-400 text-sm mb-2">Average Score</p>
          <p class="text-4xl font-bold text-gray-900 dark:text-white">{{ stats.averageScore }}%</p>
        </div>
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
          <p class="text-gray-600 dark:text-gray-400 text-sm mb-2">Quizzes Taken</p>
          <p class="text-4xl font-bold text-gray-900 dark:text-white">{{ stats.totalResults }}</p>
        </div>
      </div>

      <!-- Recent Quizzes -->
      <div v-if="recentQuizzes.length > 0" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Recent Quizzes</h2>
        <div class="space-y-3">
          <div
            v-for="quiz of recentQuizzes"
            :key="quiz.id"
            class="p-4 border border-gray-200 dark:border-gray-700 rounded hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer transition-colors"
            @click="navigateTo(`/quiz/${quiz.id}`)"
          >
            <h3 class="font-semibold text-gray-900 dark:text-white">{{ quiz.title }}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">{{ quiz.num_questions }} questions • {{ quiz.quiz_type === 'single_choice' ? 'Multiple Choice' : 'Multiple Select' }}</p>
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

const config = useRuntimeConfig()
const { $fetch } = useNuxtApp()

const recentQuizzes = ref<any[]>([])
const stats = ref({ totalQuizzes: 0, averageScore: 0, totalResults: 0 })

onMounted(async () => {
  try {
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
    const quizzes = await $fetch(`${config.public.apiBase}/quizzes/my_quizzes`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })

    recentQuizzes.value = quizzes.slice(0, 5)
    stats.value.totalQuizzes = quizzes.length
    // Additional stats can be calculated here
  } catch (error) {
    console.error('Failed to load quizzes:', error)
  }
})
</script>
