<template>
  <UDashboardPanel grow>
    <UDashboardPanelContent class="p-6 overflow-y-auto bg-mesh">
      <!-- Loading State -->
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Results Display -->
      <div v-else-if="result" class="space-y-6">
        <!-- Header -->
        <div class="mb-4">
          <h1 class="text-4xl font-bold gradient-text mb-2">Quiz Results</h1>
          <p class="text-slate-500 dark:text-slate-400">
            Completed on {{ new Date(result.date).toLocaleDateString() }} at {{ new Date(result.date).toLocaleTimeString() }}
          </p>
        </div>

        <!-- Score Card -->
        <div class="glass-card rounded-2xl p-8 mb-6">
          <div class="text-center">
            <div class="text-6xl font-bold mb-4 gradient-text">
              {{ Math.round(result.score) }}%
            </div>
            <div class="text-xl text-slate-900 dark:text-white mb-2 flex items-center justify-center gap-2">
              <template v-if="result.score >= 70">
                <UIcon name="i-lucide-trophy" class="text-yellow-500 text-2xl" /> Passed!
              </template>
              <template v-else>
                <UIcon name="i-lucide-target" class="text-red-500 text-2xl" /> Failed
              </template>
            </div>
            <p class="text-slate-500 dark:text-slate-400">
              You answered {{ correctCount }} out of {{ result.breakdown.length }} questions correctly
            </p>
          </div>
        </div>

        <!-- Performance by Topic Chart -->
        <div v-if="Object.keys(topicPerformance).length > 0" class="glass-card rounded-2xl p-6 mb-6">
          <h2 class="text-xl font-bold gradient-text mb-4">Performance by Topic</h2>
          <p class="text-sm text-slate-500 dark:text-slate-400 mb-6">
            <span class="text-green-600 font-bold flex-inline items-center gap-1"><span class="w-2.5 h-2.5 rounded-full inline-block bg-green-500" /> Good (&ge;70%)</span> &bull;
            <span class="text-yellow-600 font-bold flex-inline items-center gap-1"><span class="w-2.5 h-2.5 rounded-full inline-block bg-yellow-500" /> Needs Improvement (50-69%)</span> &bull;
            <span class="text-red-600 font-bold flex-inline items-center gap-1"><span class="w-2.5 h-2.5 rounded-full inline-block bg-red-500" /> Failed (&lt;50%)</span>
          </p>

          <div class="space-y-4">
            <div v-for="(stats, topic) in topicPerformance" :key="topic" class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-semibold text-slate-900 dark:text-white">{{ topic }}</span>
                <div class="flex items-center gap-3">
                  <span class="text-sm text-slate-500 dark:text-slate-400">
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
              <div class="w-full bg-white/20 dark:bg-white/10 backdrop-blur-sm rounded-lg h-10 overflow-hidden">
                <div
                  class="h-10 flex items-center justify-center text-white text-sm font-bold transition-all duration-500 rounded-lg"
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
          <h2 class="text-2xl font-bold gradient-text mb-4">Question Review</h2>

          <div
            v-for="(item, index) in result.breakdown"
            :key="index"
            class="glass-card rounded-2xl p-6"
            :class="item.is_correct ? 'border-l-4 border-green-500' : 'border-l-4 border-red-500'"
          >
            <div class="flex items-start justify-between mb-4">
              <h3 class="text-lg font-semibold text-slate-900 dark:text-white flex-1">
                Question {{ item.question_index + 1 }}
              </h3>
              <span
                class="px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1"
                :class="item.is_correct ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'"
              >
                <template v-if="item.is_correct">
                  <UIcon name="i-lucide-check" /> Correct
                </template>
                <template v-else>
                  ✗ Incorrect
                </template>
              </span>
            </div>

            <div class="space-y-3">
              <!-- Question text -->
              <p v-if="item.question" class="text-slate-900 dark:text-white font-medium">
                {{ item.question }}
              </p>

              <!-- All Options -->
              <div v-if="item.options && item.options.length" class="space-y-2">
                <div
                  v-for="(option, optIdx) in item.options"
                  :key="optIdx"
                  class="flex items-start gap-3 p-3 rounded-lg border"
                  :class="getOptionClass(optIdx, item)"
                >
                  <span class="font-bold text-sm mt-0.5">{{ String.fromCharCode(65 + optIdx) }}.</span>
                  <span class="flex-1 text-slate-900 dark:text-white">{{ option }}</span>
                  <div class="flex items-center gap-2 text-xs font-medium">
                    <span v-if="isUserChoice(optIdx, item)" class="px-2 py-0.5 rounded bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                      Your answer
                    </span>
                    <span v-if="isCorrectChoice(optIdx, item)" class="px-2 py-0.5 rounded bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 flex items-center gap-1">
                      <UIcon name="i-lucide-check" /> Correct
                    </span>
                    <span v-else-if="isUserChoice(optIdx, item)" class="px-2 py-0.5 rounded bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200">
                      ✗ Incorrect
                    </span>
                  </div>
                </div>
              </div>

              <!-- Fallback when options aren't available -->
              <template v-else>
                <div>
                  <p class="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Your Answer:</p>
                  <p class="text-slate-900 dark:text-white">{{ formatAnswer(item.user_choice) }}</p>
                </div>
                <div v-if="!item.is_correct">
                  <p class="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Correct Answer:</p>
                  <p class="text-green-700 dark:text-green-300 font-medium">{{ formatAnswer(item.correct_answer) }}</p>
                </div>
              </template>

              <!-- Explanation -->
              <div v-if="item.explanation" class="bg-blue-500/10 dark:bg-blue-500/15 border border-blue-500/20 backdrop-blur-sm rounded-xl p-4">
                <p class="text-sm font-medium text-blue-900 dark:text-blue-200 mb-1">Explanation:</p>
                <p class="text-blue-800 dark:text-blue-300">{{ item.explanation }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-8 flex gap-4 flex-wrap">
          <NuxtLink :to="backLink">
            <button class="glass-card rounded-xl px-6 py-2 text-slate-900 dark:text-white transition-all hover:scale-105">
              &larr; {{ backLabel }}
            </button>
          </NuxtLink>

          <button
            @click="guardAction(() => retakeQuiz())"
            class="btn-gradient rounded-xl px-6 py-2 font-medium flex items-center gap-2"
          >
            <UIcon name="i-lucide-rotate-ccw" /> Retake This Quiz
          </button>

        </div>
      </div>

      <!-- Error State -->
      <div v-else class="text-center py-12">
        <p class="text-red-600 dark:text-red-400 mb-4">Failed to load results</p>
        <NuxtLink to="/quizzes">
          <button class="btn-gradient rounded-xl px-6 py-2">
            Back to Quizzes
          </button>
        </NuxtLink>
      </div>
    </UDashboardPanelContent>

    <SubscriptionModal v-model="showSubscriptionModal" />
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
const showSubscriptionModal = ref(false)

const { isEligible, fetchUser } = useSubscription()

function guardAction(action: () => void) {
  if (isEligible.value) {
    action()
  } else {
    showSubscriptionModal.value = true
  }
}

const backLink = computed(() => {
  const subjectId = result.value?.quiz?.subject_id
  if (subjectId) return `/subjects/${subjectId}`
  const sourceSubjectId = result.value?.quiz?.source_subject_id
  if (sourceSubjectId) return `/subjects/${sourceSubjectId}`
  return '/quizzes'
})

const backLabel = computed(() =>
  backLink.value.startsWith('/subjects') ? 'Back to Subject' : 'Back to Quizzes'
)

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

const toIndexSet = (val: any): number[] => {
  if (val === null || val === undefined) return []
  return Array.isArray(val) ? val : [val]
}

const isUserChoice = (optIdx: number, item: any) =>
  toIndexSet(item.user_choice).includes(optIdx)

const isCorrectChoice = (optIdx: number, item: any) =>
  toIndexSet(item.correct_answer).includes(optIdx)

const getOptionClass = (optIdx: number, item: any) => {
  const isCorrect = isCorrectChoice(optIdx, item)
  const isUser = isUserChoice(optIdx, item)
  if (isCorrect) return 'bg-green-50 dark:bg-green-900/20 border-green-500'
  if (isUser) return 'bg-red-50 dark:bg-red-900/20 border-red-500'
  return 'bg-white/50 dark:bg-white/5 border-white/20 dark:border-white/10'
}

const getBarColor = (accuracy: number) => {
  if (accuracy >= 70) return 'bg-gradient-to-r from-green-500 to-teal-500'
  if (accuracy >= 50) return 'bg-gradient-to-r from-yellow-500 to-orange-400'
  return 'bg-gradient-to-r from-red-500 to-pink-500'
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
  fetchUser()
  try {
    const resultId = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id

    const response = await fetch(`${config.public.apiBase}/quizzes/result/${resultId}/review`, {
      credentials: 'include'
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
