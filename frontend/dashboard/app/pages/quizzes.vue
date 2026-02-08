<template>
  <div class="h-screen overflow-y-auto bg-gray-50 dark:bg-gray-900 px-6 py-12">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 dark:text-white">My Quizzes</h1>
          <p class="text-gray-600 dark:text-gray-400 mt-2">Manage and retake your quizzes</p>
        </div>
        <NuxtLink to="/quiz-new">
          <button class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium">
            + New Quiz
          </button>
        </NuxtLink>
      </div>

      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <div v-else-if="quizzes.length === 0" class="text-center py-12">
        <p class="text-gray-600 dark:text-gray-400 mb-4">No quizzes yet</p>
        <NuxtLink to="/quiz-new">
          <button class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            Create Your First Quiz
          </button>
        </NuxtLink>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="quiz of quizzes"
          :key="quiz.id"
          class="bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-lg transition-shadow p-6 cursor-pointer"
          @click="navigateTo(`/quiz/${quiz.id}`)"
        >
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">{{ quiz.title }}</h3>
          
          <div class="space-y-2 text-sm text-gray-600 dark:text-gray-400 mb-4">
            <p>📝 {{ quiz.num_questions }} questions</p>
            <p v-if="quiz.time_limit">⏱️ {{ quiz.time_limit }} minutes</p>
            <p>{{ quiz.quiz_type === 'single_choice' ? '✓ Multiple Choice' : '✓✓ Multiple Select' }}</p>
          </div>

          <div class="flex gap-2">
            <button
              @click.stop="deleteQuiz(quiz.id)"
              class="px-3 py-1 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded text-sm"
            >
              Delete
            </button>
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
const quizzes = ref<any[]>([])
const isLoading = ref(true)

const loadQuizzes = async () => {
  try {
    isLoading.value = true
    const { $fetch } = useNuxtApp()
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null

    quizzes.value = await $fetch(`${config.public.apiBase}/quizzes/my_quizzes`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
  } catch (error) {
    console.error('Failed to load quizzes:', error)
  } finally {
    isLoading.value = false
  }
}

const deleteQuiz = async (quizId: string) => {
  if (!confirm('Are you sure you want to delete this quiz?')) return

  try {
    const { $fetch } = useNuxtApp()
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null

    await $fetch(`${config.public.apiBase}/quizzes/${quizId}`, {
      method: 'DELETE',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })

    quizzes.value = quizzes.value.filter(q => q.id !== quizId)
  } catch (error) {
    console.error('Failed to delete quiz:', error)
    alert('Failed to delete quiz')
  }
}

onMounted(() => {
  loadQuizzes()
})
</script>
