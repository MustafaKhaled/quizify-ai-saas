<script setup lang="ts">
definePageMeta({
  title: 'Dashboard',
  description: 'Overview of your quizzes and activity'
})

const { user } = useUserSession()
const config = useRuntimeConfig()
const toast = useToast()

// Fetch user's quizzes
const { data: quizzes, refresh: refreshQuizzes } = await useFetch('/api/quizzes', {
  lazy: true,
  default: () => []
})

// Fetch user's sources
const { data: sources, refresh: refreshSources } = await useFetch('/api/sources', {
  lazy: true,
  default: () => []
})

const stats = computed(() => ({
  totalQuizzes: quizzes.value?.length || 0,
  totalSources: sources.value?.length || 0,
  recentQuizzes: quizzes.value?.slice(0, 5) || []
}))
</script>

<template>
  <div class="space-y-6">
    <!-- Welcome Section -->
    <UCard>
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold">Welcome back, {{ user?.name || 'User' }}!</h2>
          <p class="text-gray-500 mt-1">
            {{ user?.subscription?.label || 'Free Trial' }}
          </p>
        </div>
        <UButton to="/upload" icon="i-lucide-plus" size="lg">
          Create Quiz
        </UButton>
      </div>
    </UCard>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <UCard>
        <div class="flex items-center gap-4">
          <div class="p-3 bg-primary/10 rounded-lg">
            <UIcon name="i-lucide-file-question" class="w-6 h-6 text-primary" />
          </div>
          <div>
            <p class="text-sm text-gray-500">Total Quizzes</p>
            <p class="text-2xl font-bold">{{ stats.totalQuizzes }}</p>
          </div>
        </div>
      </UCard>

      <UCard>
        <div class="flex items-center gap-4">
          <div class="p-3 bg-green-500/10 rounded-lg">
            <UIcon name="i-lucide-file-text" class="w-6 h-6 text-green-500" />
          </div>
          <div>
            <p class="text-sm text-gray-500">PDF Sources</p>
            <p class="text-2xl font-bold">{{ stats.totalSources }}</p>
          </div>
        </div>
      </UCard>

      <UCard>
        <div class="flex items-center gap-4">
          <div class="p-3 bg-blue-500/10 rounded-lg">
            <UIcon name="i-lucide-crown" class="w-6 h-6 text-blue-500" />
          </div>
          <div>
            <p class="text-sm text-gray-500">Subscription</p>
            <p class="text-lg font-semibold">{{ user?.subscription?.label || 'Trial' }}</p>
          </div>
        </div>
      </UCard>
    </div>

    <!-- Recent Quizzes -->
    <UCard>
      <template #header>
        <h3 class="text-lg font-semibold">Recent Quizzes</h3>
      </template>
      
      <div v-if="stats.recentQuizzes.length === 0" class="text-center py-8 text-gray-500">
        <UIcon name="i-lucide-file-question" class="w-12 h-12 mx-auto mb-2 opacity-50" />
        <p>No quizzes yet. Create your first quiz!</p>
        <UButton to="/upload" class="mt-4">Get Started</UButton>
      </div>

      <div v-else class="space-y-2">
        <div
          v-for="quiz in stats.recentQuizzes"
          :key="quiz.id"
          class="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
        >
          <div class="flex-1">
            <h4 class="font-semibold">{{ quiz.title }}</h4>
            <p class="text-sm text-gray-500">
              {{ quiz.num_questions }} questions • {{ quiz.quiz_type }}
            </p>
          </div>
          <div class="flex gap-2">
            <UButton
              :to="`/quiz/${quiz.id}`"
              size="sm"
              variant="outline"
            >
              Take Quiz
            </UButton>
          </div>
        </div>
      </div>
    </UCard>
  </div>
</template>
