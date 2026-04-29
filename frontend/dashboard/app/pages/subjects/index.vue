<template>
  <UDashboardPanel grow>
    <UDashboardNavbar class="lg:hidden" title="My Subjects" />
    <UDashboardPanelContent class="p-4 sm:p-6 overflow-y-auto bg-mesh min-h-full">
      <div class="flex flex-wrap items-center justify-between gap-3 mb-6 sm:mb-8">
        <div>
          <h1 class="text-2xl sm:text-4xl font-bold gradient-text mb-1">My Subjects</h1>
          <p class="text-sm sm:text-base text-slate-500 dark:text-slate-400">Organize your study material by subject</p>
        </div>
        <NuxtLink to="/subjects/new">
          <button class="px-4 sm:px-5 py-2 btn-gradient rounded-xl transition-colors font-medium text-sm sm:text-base">
            + New Subject
          </button>
        </NuxtLink>
      </div>

      <!-- Predefined PMP card (always visible, idempotent) -->
      <div
        class="glass-card rounded-2xl overflow-hidden cursor-pointer hover:shadow-xl hover:shadow-orange-500/10 transition-all hover:-translate-y-0.5 mb-6 sm:mb-8"
        @click="launchPMP()"
      >
        <div class="h-1.5" style="background: linear-gradient(90deg, #F97316, #FB923C)"></div>
        <div class="p-5 sm:p-6 flex flex-wrap items-center gap-4 sm:gap-6">
          <div class="flex items-center gap-4 min-w-0 flex-1">
            <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0" style="background: linear-gradient(135deg, #F97316, #FB923C); box-shadow: 0 8px 24px -8px rgba(249, 115, 22, 0.5)">
              <span>📋</span>
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2 mb-1 flex-wrap">
                <h3 class="text-lg sm:text-xl font-bold text-slate-900 dark:text-white">PMP Practice</h3>
                <span class="px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide rounded-full text-orange-700 dark:text-orange-300 bg-orange-500/10 border border-orange-500/20">Predefined</span>
              </div>
              <p class="text-sm text-slate-500 dark:text-slate-400">10 PMBOK knowledge areas, ready-to-quiz with grounded AI generation.</p>
            </div>
          </div>
          <button
            type="button"
            @click.stop="launchPMP()"
            :disabled="pmpProvisioning"
            class="px-5 py-2 rounded-xl font-semibold text-sm text-white disabled:opacity-50 transition-transform hover:-translate-y-0.5"
            style="background: linear-gradient(135deg, #F97316, #FB923C); box-shadow: 0 8px 24px -8px rgba(249, 115, 22, 0.5)"
          >
            {{ pmpProvisioning ? 'Loading...' : 'Open PMP →' }}
          </button>
        </div>
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
const pmpProvisioning = ref(false)

async function launchPMP() {
  if (pmpProvisioning.value) return
  pmpProvisioning.value = true
  try {
    const res = await fetch(`${config.public.apiBase}/predefined/pmp/provision`, {
      method: 'POST',
      credentials: 'include',
    })
    if (res.status === 403) {
      alert('Pro plan required to access PMP practice.')
      return
    }
    if (!res.ok) {
      alert('Failed to start PMP. Please try again.')
      return
    }
    const subject = await res.json()
    if (subject?.id) await navigateTo(`/subjects/${subject.id}`)
  } finally {
    pmpProvisioning.value = false
  }
}

onMounted(async () => {
  try {
    const res = await fetch(`${config.public.apiBase}/subjects`, { credentials: 'include' })
    if (res.ok) {
      const all = await res.json()
      subjects.value = all.filter((s: any) => s.name !== 'PMP')
    }
  } catch (e) {
    console.error('Failed to load subjects:', e)
  } finally {
    isLoading.value = false
  }
})
</script>
