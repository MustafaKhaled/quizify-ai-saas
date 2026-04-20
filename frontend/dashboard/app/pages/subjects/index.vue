<template>
  <UDashboardPanel grow>
    <UDashboardPanelContent class="p-6 overflow-y-auto bg-mesh min-h-full">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-4xl font-bold gradient-text mb-1">My Subjects</h1>
          <p class="text-slate-500 dark:text-slate-400">Organize your study material by subject</p>
        </div>
        <NuxtLink to="/subjects/new">
          <button class="px-5 py-2 btn-gradient rounded-xl transition-colors font-medium">
            + New Subject
          </button>
        </NuxtLink>
      </div>

      <div v-if="isLoading" class="flex items-center justify-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <div v-else-if="subjects.length === 0" class="text-center py-20">
        <div class="flex justify-center mb-4">
          <UIcon name="i-lucide-book-open" class="w-12 h-12 text-slate-300 dark:text-slate-600" />
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-2">No subjects yet</h2>
        <p class="text-slate-500 dark:text-slate-400 mb-6">Create your first subject to start organizing your quizzes</p>
        <NuxtLink to="/subjects/new">
          <button class="px-6 py-2 btn-gradient rounded-xl transition-colors font-medium">
            Create Subject
          </button>
        </NuxtLink>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="subject in subjects"
          :key="subject.id"
          class="glass-card rounded-2xl hover:shadow-xl hover:shadow-blue-500/10 transition-all hover:-translate-y-0.5 cursor-pointer overflow-hidden"
          @click="navigateTo(`/subjects/${subject.id}`)"
        >
          <!-- Color bar -->
          <div class="h-2" :style="{ backgroundColor: subject.color || '#3B82F6' }"></div>

          <div class="p-5">
            <div class="flex items-start justify-between mb-3">
              <h2 class="text-xl font-bold text-slate-900 dark:text-white leading-tight">{{ subject.name }}</h2>
              <div
                class="w-8 h-8 rounded-full flex-shrink-0 ml-2"
                :style="{ backgroundColor: subject.color || '#3B82F6' }"
              ></div>
            </div>

            <div class="flex gap-4 text-sm text-slate-500 dark:text-slate-400">
              <span>{{ subject.source_count }} {{ subject.source_count === 1 ? 'source' : 'sources' }}</span>
              <span>{{ subject.quiz_count }} {{ subject.quiz_count === 1 ? 'quiz' : 'quizzes' }}</span>
            </div>

            <p class="text-xs text-slate-500 dark:text-slate-400 mt-3">
              Created {{ new Date(subject.created_at).toLocaleDateString() }}
            </p>
          </div>
        </div>
      </div>
    </UDashboardPanelContent>
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })

const config = useRuntimeConfig()
const subjects = ref<any[]>([])
const isLoading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch(`${config.public.apiBase}/subjects`, { credentials: 'include' })
    if (res.ok) subjects.value = await res.json()
  } catch (e) {
    console.error('Failed to load subjects:', e)
  } finally {
    isLoading.value = false
  }
})
</script>
