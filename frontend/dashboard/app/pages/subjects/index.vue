<template>
  <UDashboardPanel grow>
    <UDashboardNavbar class="lg:hidden" title="My Subjects" />
    <UDashboardPanelContent class="p-4 sm:p-6 overflow-y-auto bg-mesh min-h-full">
      <div class="flex flex-wrap items-center justify-between gap-3 mb-6 sm:mb-8">
        <div>
          <h1 class="text-2xl sm:text-4xl font-bold gradient-text mb-1">My Subjects</h1>
          <p class="text-sm sm:text-base text-slate-500 dark:text-slate-400">Organize your study material by subject</p>
        </div>
        <div class="flex items-center gap-2">
          <button
            v-if="availablePredefinedAgents.length > 0"
            type="button"
            @click="showBrowseLibrary = true"
            class="px-3 py-2 rounded-xl font-semibold text-sm border border-slate-300 dark:border-slate-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition flex items-center gap-1.5"
          >
            <UIcon name="i-lucide-library" class="w-4 h-4" />
            Browse library
            <span class="px-1.5 py-0.5 text-[10px] font-bold rounded-full bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300">
              {{ availablePredefinedAgents.length }}
            </span>
          </button>
          <NuxtLink to="/subjects/new">
            <button class="px-4 sm:px-5 py-2 btn-gradient rounded-xl transition-colors font-medium text-sm sm:text-base">
              + New Subject
            </button>
          </NuxtLink>
        </div>
      </div>

      <!-- Predefined subject cards — only ones the user has added -->
      <div v-if="myPredefinedAgents.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6 sm:mb-8">
        <div
          v-for="agent in myPredefinedAgents"
          :key="agent.slug"
          class="glass-card rounded-2xl overflow-hidden cursor-pointer hover:shadow-xl transition-all hover:-translate-y-0.5"
          :style="{ boxShadow: `0 8px 24px -12px ${agent.color || '#3B82F6'}55` }"
          @click="launchPredefined(agent.slug)"
        >
          <div class="h-1.5" :style="{ background: `linear-gradient(90deg, ${agent.color || '#3B82F6'}, ${agent.color || '#3B82F6'}cc)` }"></div>
          <div class="p-5 flex items-center gap-4">
            <div
              class="w-12 h-12 rounded-xl flex items-center justify-center text-xl flex-shrink-0 text-white"
              :style="{ background: agent.color || '#3B82F6' }"
            >
              <span>{{ agent.icon || '📚' }}</span>
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2 mb-0.5 flex-wrap">
                <h3 class="text-base font-bold text-slate-900 dark:text-white">{{ agent.name }}</h3>
                <span class="px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide rounded-full text-slate-700 dark:text-slate-300 bg-slate-500/10 border border-slate-500/20">Predefined</span>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400">Ready-to-quiz with grounded AI generation.</p>
            </div>
            <button
              type="button"
              @click.stop="launchPredefined(agent.slug)"
              :disabled="provisioningSlug === agent.slug"
              class="px-3 py-1.5 rounded-lg font-semibold text-xs text-white disabled:opacity-50 transition-transform hover:-translate-y-0.5 flex-shrink-0"
              :style="{ background: agent.color || '#3B82F6' }"
            >
              {{ provisioningSlug === agent.slug ? '...' : 'Open →' }}
            </button>
          </div>
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

    <!-- Browse Library modal — lists predefined agents NOT yet added.
         Nuxt UI v4: open via :open + @update:open, content goes in #content slot. -->
    <UModal :open="showBrowseLibrary" @update:open="showBrowseLibrary = $event" size="xl">
      <template #content>
        <div class="p-6">
          <div class="flex items-start justify-between mb-4 gap-3">
            <div>
              <h2 class="text-lg font-bold gradient-text">Add to your library</h2>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Pick the exams and tracks you're preparing for. You can add or remove them anytime.
              </p>
            </div>
            <UButton color="neutral" variant="ghost" icon="i-lucide-x" @click="showBrowseLibrary = false" />
          </div>

          <div v-if="availablePredefinedAgents.length === 0" class="py-8 text-center">
            <UIcon name="i-lucide-check-circle-2" class="w-10 h-10 text-emerald-500 mx-auto mb-3" />
            <p class="text-sm text-slate-700 dark:text-slate-300 font-semibold">All caught up.</p>
            <p class="text-xs text-slate-500 dark:text-slate-400">You've added every available subject.</p>
          </div>

          <div v-else class="space-y-2 max-h-[60vh] overflow-y-auto">
            <div
              v-for="agent in availablePredefinedAgents"
              :key="agent.slug"
              class="flex items-center gap-3 p-3 rounded-xl border border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 transition"
            >
              <div
                class="w-10 h-10 rounded-lg flex items-center justify-center text-lg flex-shrink-0 text-white"
                :style="{ background: agent.color || '#3B82F6' }"
              >
                {{ agent.icon || '📚' }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 flex-wrap">
                  <h3 class="text-sm font-bold text-slate-900 dark:text-white">{{ agent.name }}</h3>
                  <span
                    v-if="agent.status === 'preview'"
                    class="px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide rounded-full text-amber-700 dark:text-amber-300 bg-amber-500/10 border border-amber-500/30"
                  >Preview</span>
                </div>
                <p class="text-xs text-slate-500 dark:text-slate-400">
                  {{ agent.status === 'preview' ? 'Early access — listening practice prototype.' : 'AI-generated practice questions, grounded in the official syllabus.' }}
                </p>
              </div>
              <button
                type="button"
                :disabled="addingSlug === agent.slug"
                @click="addToLibrary(agent.slug)"
                class="px-3 py-1.5 btn-gradient rounded-lg text-xs font-semibold whitespace-nowrap disabled:opacity-50"
              >
                {{ addingSlug === agent.slug ? 'Adding…' : '+ Add' }}
              </button>
            </div>
          </div>
        </div>
      </template>
    </UModal>
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })

const config = useRuntimeConfig()
const subjects = ref<any[]>([])
const isLoading = ref(true)
const provisioningSlug = ref<string | null>(null)
const showBrowseLibrary = ref(false)

const { agents: predefinedAgentsRef, load: loadPredefinedAgents } = usePredefinedSubjects()
const predefinedAgents = computed(() => predefinedAgentsRef.value || [])

// Same filter pattern as the dashboard: only show predefined cards for agents
// the user has added to their library. Un-added agents live in the Browse
// Library modal until added.
const addedPredefinedSlugs = ref<string[]>([])

async function loadAddedPredefined() {
  try {
    const res = await $fetch<{ added_slugs: string[] }>(
      `${config.public.apiBase}/predefined/added`,
      { credentials: 'include' }
    )
    addedPredefinedSlugs.value = res.added_slugs || []
  } catch {
    addedPredefinedSlugs.value = []
  }
}

const myPredefinedAgents = computed(() =>
  predefinedAgents.value.filter((a) => addedPredefinedSlugs.value.includes(a.slug))
)
const availablePredefinedAgents = computed(() =>
  predefinedAgents.value.filter((a) => !addedPredefinedSlugs.value.includes(a.slug))
)

const addingSlug = ref<string | null>(null)
async function addToLibrary(slug: string) {
  if (addingSlug.value) return
  addingSlug.value = slug
  try {
    await $fetch(`${config.public.apiBase}/predefined/${slug}/provision`, {
      method: 'POST',
      credentials: 'include',
    })
    await loadAddedPredefined()
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Failed to add subject.')
  } finally {
    addingSlug.value = null
  }
}

// Hören / Lesen don't use the generated-quiz subject view — they have their
// own dedicated chapter-picker pages (/horen/<slug>, /lesen/<slug>) that
// drive the audio/reading flow. Route them there directly instead of
// provisioning a subject and dumping the user on /subjects/<id>, which
// would mis-frame the feature as a regular generated-quiz subject.
const HOREN_SLUGS = ['deutsch_a2_horen', 'deutsch_b1_horen'] as const
const LESEN_SLUGS = ['deutsch_a2_lesen', 'deutsch_b1_lesen'] as const

async function launchPredefined(slug: string) {
  if (provisioningSlug.value) return
  if ((HOREN_SLUGS as readonly string[]).includes(slug)) {
    await navigateTo(`/horen/${slug}`)
    return
  }
  if ((LESEN_SLUGS as readonly string[]).includes(slug)) {
    await navigateTo(`/lesen/${slug}`)
    return
  }
  provisioningSlug.value = slug
  try {
    const res = await fetch(`${config.public.apiBase}/predefined/${slug}/provision`, {
      method: 'POST',
      credentials: 'include',
    })
    if (res.status === 403) {
      alert('Pro plan required to access this subject.')
      return
    }
    if (!res.ok) {
      alert('Failed to start. Please try again.')
      return
    }
    const subject = await res.json()
    if (subject?.id) await navigateTo(`/subjects/${subject.id}`)
  } finally {
    provisioningSlug.value = null
  }
}

onMounted(async () => {
  loadPredefinedAgents().catch(() => {})
  loadAddedPredefined().catch(() => {})
  try {
    const res = await fetch(`${config.public.apiBase}/subjects`, { credentials: 'include' })
    if (res.ok) {
      const all = await res.json()
      // Filter out predefined-subject rows from the user-subjects list (they have their own cards above)
      const agents = await loadPredefinedAgents().catch(() => [])
      const predefinedNames = new Set(agents.map((a) => a.name))
      subjects.value = all.filter((s: any) => !predefinedNames.has(s.name))
    }
  } catch (e) {
    console.error('Failed to load subjects:', e)
  } finally {
    isLoading.value = false
  }
})
</script>
