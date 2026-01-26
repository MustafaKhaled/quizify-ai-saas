<script setup lang="ts">
definePageMeta({
  title: 'My Quizzes',
  description: 'View and manage your quizzes'
})

const toast = useToast()

const { data: quizzes, refresh } = await useFetch('/api/quizzes', {
  lazy: true,
  default: () => []
})

async function deleteQuiz(quizId: string) {
  if (!confirm('Are you sure you want to delete this quiz?')) return

  try {
    const config = useRuntimeConfig()
    const session = await useUserSession()
    
    await $fetch(`${config.public.apiBase}/quizzes/${quizId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${session.token.value}`
      }
    })

    toast.add({
      title: 'Success',
      description: 'Quiz deleted successfully',
      color: 'success'
    })

    await refresh()
  } catch (err: any) {
    toast.add({
      title: 'Error',
      description: err?.data?.message || 'Failed to delete quiz',
      color: 'error'
    })
  }
}
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-bold">My Quizzes</h2>
      <UButton to="/upload" icon="i-lucide-plus">
        Create New Quiz
      </UButton>
    </div>

    <div v-if="quizzes?.length === 0" class="text-center py-12">
      <UIcon name="i-lucide-file-question" class="w-16 h-16 mx-auto mb-4 text-gray-400" />
      <p class="text-gray-500 mb-4">No quizzes yet</p>
      <UButton to="/upload">Create Your First Quiz</UButton>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <UCard
        v-for="quiz in quizzes"
        :key="quiz.id"
        class="hover:shadow-lg transition-shadow"
      >
        <template #header>
          <h3 class="font-semibold text-lg">{{ quiz.title }}</h3>
        </template>

        <div class="space-y-2">
          <div class="flex items-center gap-2 text-sm text-gray-500">
            <UIcon name="i-lucide-help-circle" class="w-4 h-4" />
            <span>{{ quiz.num_questions }} questions</span>
          </div>
          <div class="flex items-center gap-2 text-sm text-gray-500">
            <UIcon name="i-lucide-tag" class="w-4 h-4" />
            <span>{{ quiz.quiz_type === 'single_choice' ? 'Single Choice' : 'Multiple Select' }}</span>
          </div>
          <div v-if="quiz.time_limit" class="flex items-center gap-2 text-sm text-gray-500">
            <UIcon name="i-lucide-clock" class="w-4 h-4" />
            <span>{{ quiz.time_limit }} minutes</span>
          </div>
          <div class="flex items-center gap-2 text-sm text-gray-500">
            <UIcon name="i-lucide-calendar" class="w-4 h-4" />
            <span>{{ new Date(quiz.generation_date).toLocaleDateString() }}</span>
          </div>
        </div>

        <template #footer>
          <div class="flex gap-2">
            <UButton
              :to="`/quiz/${quiz.id}`"
              class="flex-1"
              variant="outline"
            >
              Take Quiz
            </UButton>
            <UButton
              color="error"
              variant="ghost"
              icon="i-lucide-trash"
              @click="deleteQuiz(quiz.id)"
            />
          </div>
        </template>
      </UCard>
    </div>
  </div>
</template>
