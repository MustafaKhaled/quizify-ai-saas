<template>
  <UDashboardPanel grow>
    <UDashboardPanelContent class="p-6 overflow-y-auto bg-mesh">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-4xl font-bold gradient-text">My Quizzes</h1>
          <p class="text-slate-500 dark:text-slate-400 mt-2">Manage and retake your quizzes</p>
        </div>
        <NuxtLink to="/quiz-new">
          <button class="btn-gradient rounded-xl px-6 py-2 font-medium">
            + New Quiz
          </button>
        </NuxtLink>
      </div>

      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <div v-else-if="quizzes.length === 0" class="text-center py-12">
        <p class="text-slate-500 dark:text-slate-400 mb-4">No quizzes yet</p>
        <NuxtLink to="/quiz-new">
          <button class="btn-gradient rounded-xl px-6 py-2">
            Create Your First Quiz
          </button>
        </NuxtLink>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="quiz of quizzes"
          :key="quiz.id"
          class="glass-card rounded-2xl hover:shadow-2xl transition-all hover:scale-[1.02] p-6 cursor-pointer"
          @click="handleQuizClick(quiz.id)"
        >
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">{{ quiz.title }}</h3>

          <div class="space-y-2 text-sm text-slate-500 dark:text-slate-400 mb-4">
            <p class="flex items-center gap-2"><UIcon name="i-lucide-file-text" /> {{ quiz.num_questions }} questions</p>
            <p v-if="quiz.time_limit" class="flex items-center gap-2"><UIcon name="i-lucide-clock" /> {{ quiz.time_limit }} minutes</p>
            <p class="flex items-center gap-2"><UIcon name="i-lucide-check" /> {{ quiz.quiz_type === 'single_choice' ? 'Multiple Choice' : 'Multiple Select' }}</p>
            <p v-if="quiz.lastResult" class="text-blue-600 dark:text-blue-400 font-medium flex items-center gap-2">
              <UIcon name="i-lucide-check" /> Completed - <span class="gradient-text font-bold">{{ Math.round(quiz.lastResult.score_percentage) }}%</span>
            </p>
          </div>

          <div class="flex gap-2">
            <button
              @click.stop="deleteQuiz(quiz.id)"
              class="px-3 py-1 text-red-600 dark:text-red-400 hover:bg-red-500/10 rounded-lg text-sm transition-colors"
            >
              Delete
            </button>
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
const quizzes = ref<any[]>([])
const isLoading = ref(true)

const loadQuizzes = async () => {
  try {
    isLoading.value = true
    const response = await fetch(`${config.public.apiBase}/quizzes/my_quizzes`, {
      credentials: 'include'
    })

    if (response.ok) {
      const quizData = await response.json()

      // Fetch results for each quiz to check if completed
      const quizzesWithResults = await Promise.all(
        quizData.map(async (quiz: any) => {
          try {
            const resultsResponse = await fetch(`${config.public.apiBase}/quizzes/results/${quiz.id}`, {
              credentials: 'include'
            })

            if (resultsResponse.ok) {
              const results = await resultsResponse.json()
              return {
                ...quiz,
                lastResult: results.length > 0 ? results[0] : null
              }
            }
          } catch (error) {
            console.error(`Failed to load results for quiz ${quiz.id}:`, error)
          }
          return quiz
        })
      )

      quizzes.value = quizzesWithResults
    } else {
      console.error('Failed to load quizzes:', response.status)
    }
  } catch (error) {
    console.error('Failed to load quizzes:', error)
  } finally {
    isLoading.value = false
  }
}

const handleQuizClick = async (quizId: string) => {
  const quiz = quizzes.value.find(q => q.id === quizId)

  // If quiz has been completed, show results. Otherwise, take the quiz
  if (quiz?.lastResult) {
    await navigateTo(`/results/${quiz.lastResult.id}`)
  } else {
    await navigateTo(`/quiz/${quizId}`)
  }
}

const deleteQuiz = async (quizId: string) => {
  if (!confirm('Are you sure you want to delete this quiz?')) return

  try {
    const response = await fetch(`${config.public.apiBase}/quizzes/${quizId}`, {
      method: 'DELETE',
      credentials: 'include'
    })

    if (response.ok) {
      quizzes.value = quizzes.value.filter(q => q.id !== quizId)
      alert('Quiz deleted successfully!')
    } else {
      alert('Failed to delete quiz')
    }
  } catch (error) {
    console.error('Failed to delete quiz:', error)
    alert('Failed to delete quiz')
  }
}

onMounted(() => {
  loadQuizzes()
})
</script>
