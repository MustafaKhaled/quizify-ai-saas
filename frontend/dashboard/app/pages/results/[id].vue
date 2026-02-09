<template>
  <UDashboardPanel grow>
    <UDashboardPanelContent class="p-6 max-w-4xl mx-auto overflow-y-auto">
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

        <!-- Performance by Topic Chart -->
        <div v-if="Object.keys(topicPerformance).length > 0" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
          <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Performance by Topic</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
            <span class="text-green-600 font-bold">🟢 Good (≥70%)</span> •
            <span class="text-yellow-600 font-bold">🟡 Needs Improvement (50-69%)</span> •
            <span class="text-red-600 font-bold">🔴 Failed (<50%)</span>
          </p>

          <div class="space-y-4">
            <div v-for="(stats, topic) in topicPerformance" :key="topic" class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-semibold text-gray-900 dark:text-white">{{ topic }}</span>
                <div class="flex items-center gap-3">
                  <span class="text-sm text-gray-600 dark:text-gray-400">
                    {{ stats.correct }}/{{ stats.total }} correct
                  </span>
                  <span
                    class="text-sm font-bold px-3 py-1 rounded-md"
                    :class="getPerformanceColor(stats.accuracy)"
                  >
                    {{ getPerformanceLabel(stats.accuracy) }}
                  </span>
                </div>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-lg h-10 overflow-hidden">
                <div
                  class="h-10 flex items-center justify-center text-white text-sm font-bold transition-all duration-500"
                  :class="getBarColor(stats.accuracy)"
                  :style="{ width: `${stats.accuracy}%` }"
                >
                  <span v-if="stats.accuracy > 20">{{ Math.round(stats.accuracy) }}%</span>
                </div>
              </div>
            </div>
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
        <div class="mt-8 flex gap-4 flex-wrap">
          <NuxtLink to="/quizzes">
            <button class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors">
              ← Back to Quizzes
            </button>
          </NuxtLink>

          <button
            @click="retakeQuiz"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            🔄 Retake This Quiz
          </button>

          <button
            v-if="hasWeakTopics"
            @click="createFocusedQuiz"
            class="px-6 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
          >
            🎯 Practice Weak Areas
          </button>

          <button
            @click="retakeFullQuiz"
            class="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            ✨ Generate New Quiz
          </button>
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
    </UDashboardPanelContent>
  </UDashboardPanel>
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

const getPerformanceLabel = (accuracy: number) => {
  if (accuracy >= 70) return 'Good'
  if (accuracy >= 50) return 'Needs Improvement'
  return 'Failed'
}

const topicPerformance = computed(() => {
  if (!result.value?.breakdown) return {}

  const stats: Record<string, { total: number, correct: number, accuracy: number }> = {}

  result.value.breakdown.forEach((item: any) => {
    const topic = item.topic || 'Unknown'

    if (!stats[topic]) {
      stats[topic] = { total: 0, correct: 0, accuracy: 0 }
    }

    stats[topic].total++
    if (item.is_correct) {
      stats[topic].correct++
    }
  })

  // Calculate accuracy
  Object.values(stats).forEach(s => {
    s.accuracy = s.total > 0 ? (s.correct / s.total) * 100 : 0
  })

  return stats
})

const hasWeakTopics = computed(() => {
  return Object.values(topicPerformance.value).some(s => s.accuracy < 70 && s.total >= 2)
})

const createFocusedQuiz = async () => {
  const weakTopics = Object.entries(topicPerformance.value)
    .filter(([_, stats]) => stats.accuracy < 70 && stats.total >= 2)
    .map(([topic, _]) => topic)

  // Navigate to quiz creation with focus topics
  await navigateTo({
    path: '/quiz-new',
    query: {
      source_id: result.value.quiz?.source_id,
      focus_topics: weakTopics.join(','),
      mode: 'focused'
    }
  })
}

const retakeQuiz = async () => {
  if (result.value?.quiz?.id) {
    await navigateTo(`/quiz/${result.value.quiz.id}`)
  }
}

const retakeFullQuiz = async () => {
  await navigateTo({
    path: '/quiz-new',
    query: {
      source_id: result.value.quiz?.source_id,
      mode: 'full'
    }
  })
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
