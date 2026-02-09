<template>
  <UDashboardPanel grow>
    <UDashboardPanelContent class="p-6 overflow-y-auto">
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

      <!-- Weak Topics Widget -->
      <div v-if="topicInsights.length > 0" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Your Weak Areas</h2>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          Topics where you scored below 70% •
          <span class="text-green-600 font-bold">🟢 Good</span> •
          <span class="text-yellow-600 font-bold">🟡 Needs Improvement</span> •
          <span class="text-red-600 font-bold">🔴 Failed</span>
        </p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="topic in topicInsights" :key="topic.topic"
               class="border-2 rounded-lg p-4 transition-all hover:shadow-md"
               :class="getBorderColor(topic.accuracy)">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-semibold text-gray-900 dark:text-white">{{ topic.topic }}</h3>
              <span
                class="text-xs font-bold px-3 py-1 rounded-md"
                :class="getPerformanceColor(topic.accuracy)"
              >
                {{ getPerformanceLabel(topic.accuracy) }}
              </span>
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              {{ topic.correct }}/{{ topic.total }} correct • {{ Math.round(topic.accuracy) }}%
            </p>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-lg h-8 overflow-hidden">
              <div
                class="h-8 flex items-center justify-center text-white text-xs font-bold transition-all duration-500"
                :class="getBarColor(topic.accuracy)"
                :style="{ width: `${topic.accuracy}%` }"
              >
                <span v-if="topic.accuracy > 20">{{ Math.round(topic.accuracy) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
          <p class="text-gray-600 dark:text-gray-400 text-sm mb-2">Total Quizzes</p>
          <p class="text-4xl font-bold text-gray-900 dark:text-white">{{ stats.totalQuizzes }}</p>
        </div>
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
          <p class="text-gray-600 dark:text-gray-400 text-sm mb-2">Average Score</p>
          <p class="text-4xl font-bold text-gray-900 dark:text-white">{{ stats.averageScore }}%</p>
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
    </UDashboardPanelContent>
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const config = useRuntimeConfig()

const recentQuizzes = ref<any[]>([])
const stats = ref({ totalQuizzes: 0, averageScore: 0 })
const topicInsights = ref<any[]>([])

const getToken = () => typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null

const getBarColor = (accuracy: number) => {
  if (accuracy >= 70) return 'bg-green-500'
  if (accuracy >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
}

const getPerformanceColor = (accuracy: number) => {
  if (accuracy >= 70) return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
  if (accuracy >= 50) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
  return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
}

const getBorderColor = (accuracy: number) => {
  if (accuracy >= 70) return 'border-green-300 dark:border-green-700 bg-green-50 dark:bg-green-900/20'
  if (accuracy >= 50) return 'border-yellow-300 dark:border-yellow-700 bg-yellow-50 dark:bg-yellow-900/20'
  return 'border-red-300 dark:border-red-700 bg-red-50 dark:bg-red-900/20'
}

const getPerformanceLabel = (accuracy: number) => {
  if (accuracy >= 70) return 'Good'
  if (accuracy >= 50) return 'Needs Improvement'
  return 'Failed'
}

onMounted(async () => {
  try {
    const token = getToken()

    // Fetch quizzes
    const quizzesResponse = await fetch(`${config.public.apiBase}/quizzes/my_quizzes`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      }
    })

    if (quizzesResponse.ok) {
      const quizzes = await quizzesResponse.json()
      recentQuizzes.value = quizzes.slice(0, 5)
      stats.value.totalQuizzes = quizzes.length
    }

    // Fetch all quiz results
    const resultsResponse = await fetch(`${config.public.apiBase}/quizzes/my_results`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      }
    })

    if (resultsResponse.ok) {
      const results = await resultsResponse.json()

      // Calculate average score
      if (results.length > 0) {
        const totalScore = results.reduce((sum: number, result: any) => sum + result.score_percentage, 0)
        stats.value.averageScore = Math.round(totalScore / results.length)
      }
    }

    // Fetch weak topics
    const topicResponse = await fetch(`${config.public.apiBase}/quizzes/performance/by-topic`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      }
    })

    if (topicResponse.ok) {
      const data = await topicResponse.json()
      topicInsights.value = data.weak_topics.slice(0, 4) // Show top 4 weak areas
    }
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  }
})
</script>
