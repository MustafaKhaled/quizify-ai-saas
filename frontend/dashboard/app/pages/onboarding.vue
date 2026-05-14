<template>
  <div class="min-h-screen bg-mesh flex items-center justify-center p-4 sm:p-8">
    <div class="w-full max-w-3xl">

      <div class="text-center mb-8">
        <h1 class="text-3xl sm:text-4xl font-bold mb-2">
          <span class="gradient-text">Welcome{{ userName ? `, ${userName}` : '' }}</span>
          <span class="ml-1">👋</span>
        </h1>
        <p class="text-slate-600 dark:text-slate-400 text-sm sm:text-base">
          What are you preparing for? Pick the subjects you'd like in your library.
          You can add or remove more anytime.
        </p>
      </div>

      <div v-if="loading" class="text-center py-16">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500 mx-auto" />
      </div>

      <div v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
          <button
            v-for="agent in agents"
            :key="agent.slug"
            type="button"
            @click="toggleSelection(agent.slug)"
            class="relative glass-card rounded-2xl p-5 text-left transition-all hover:-translate-y-0.5 hover:shadow-xl"
            :class="selectedSlugs.includes(agent.slug)
              ? 'ring-2 ring-blue-500 dark:ring-blue-400 shadow-xl'
              : 'ring-1 ring-transparent'"
          >
            <div class="absolute top-3 right-3">
              <div
                v-if="selectedSlugs.includes(agent.slug)"
                class="w-6 h-6 rounded-full bg-blue-500 text-white flex items-center justify-center"
              >
                <UIcon name="i-lucide-check" class="w-4 h-4" />
              </div>
              <div
                v-else
                class="w-6 h-6 rounded-full border-2 border-slate-300 dark:border-slate-600"
              />
            </div>
            <div class="flex items-center gap-3 mb-2">
              <div
                class="w-11 h-11 rounded-xl flex items-center justify-center text-xl flex-shrink-0 text-white"
                :style="{ background: agent.color || '#3B82F6' }"
              >
                {{ agent.icon || '📚' }}
              </div>
              <div class="min-w-0">
                <h3 class="font-bold text-slate-900 dark:text-white text-sm">{{ agent.name }}</h3>
                <span
                  v-if="agent.status === 'preview'"
                  class="inline-block mt-0.5 px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide rounded-full text-amber-700 dark:text-amber-300 bg-amber-500/10 border border-amber-500/30"
                >Preview</span>
              </div>
            </div>
            <p class="text-xs text-slate-500 dark:text-slate-400">
              {{ agent.status === 'preview'
                  ? 'Early access — listening practice prototype.'
                  : 'AI-generated practice grounded in the official syllabus.' }}
            </p>
          </button>
        </div>

        <p v-if="error" class="text-sm text-red-600 dark:text-red-400 mb-3 text-center">{{ error }}</p>

        <div class="flex items-center justify-between gap-3 flex-wrap">
          <p class="text-xs text-slate-500 dark:text-slate-400">
            {{ selectedSlugs.length }} selected
            <span v-if="selectedSlugs.length === 0">— pick at least one to continue</span>
          </p>
          <button
            type="button"
            :disabled="submitting || selectedSlugs.length === 0"
            @click="confirmSelection"
            class="px-6 py-2.5 btn-gradient rounded-xl font-semibold text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ submitting ? 'Adding…' : 'Continue →' }}
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
// Onboarding sits OUTSIDE the dashboard layout so it can fully own the screen
// for first-run users. It's required (must select ≥1) — once submitted, the
// user lands on /dashboard and can manage their library from there via the
// Browse Library modal.
definePageMeta({ layout: false })

const config = useRuntimeConfig()
const { user: subUser, fetchUser } = useSubscription()
const { agents: agentsRef, load: loadAgents } = usePredefinedSubjects()

const agents = computed(() => agentsRef.value || [])
const userName = computed(() => subUser.value?.name || '')

const selectedSlugs = ref<string[]>([])
const loading = ref(true)
const submitting = ref(false)
const error = ref<string | null>(null)

function toggleSelection(slug: string) {
  const idx = selectedSlugs.value.indexOf(slug)
  if (idx >= 0) selectedSlugs.value.splice(idx, 1)
  else selectedSlugs.value.push(slug)
}

async function confirmSelection() {
  if (submitting.value || selectedSlugs.value.length === 0) return
  submitting.value = true
  error.value = null
  try {
    // Provision each selected agent in parallel — /provision is idempotent so
    // this is safe to retry. If any fail, we surface the first failure.
    await Promise.all(
      selectedSlugs.value.map((slug) =>
        $fetch(`${config.public.apiBase}/predefined/${slug}/provision`, {
          method: 'POST',
          credentials: 'include',
        })
      )
    )
    await navigateTo('/dashboard')
  } catch (e: any) {
    error.value = e?.data?.detail || e?.message || 'Could not save your selection. Try again.'
    submitting.value = false
  }
}

onMounted(async () => {
  loading.value = true
  try {
    // If the user already has subjects, skip onboarding — this page should
    // only be the first-time experience. Bypassing protects against:
    //   - bookmarked /onboarding revisits
    //   - users who get redirected here in error
    const [_, addedRes] = await Promise.all([
      loadAgents().catch(() => null),
      fetchUser().catch(() => null),
      (async () => null)(), // placeholder to align tuple shape
    ])
    void _
    void addedRes
    const added = await $fetch<{ added_slugs: string[] }>(
      `${config.public.apiBase}/predefined/added`,
      { credentials: 'include' }
    )
    if (added.added_slugs?.length > 0) {
      await navigateTo('/dashboard', { replace: true })
      return
    }
  } catch {
    // If anything blows up loading state, still let the user pick.
  } finally {
    loading.value = false
  }
})
</script>
