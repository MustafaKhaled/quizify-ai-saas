<template>
  <UDashboardPanel grow>
    <UDashboardNavbar class="lg:hidden" title="Dashboard" />
    <UDashboardPanelContent class="p-4 sm:p-6 overflow-y-auto bg-mesh min-h-full">

      <!-- Subscription Success -->
      <div v-if="subscriptionSuccess" class="mb-6 p-4 glass-card border-green-500/30 rounded-2xl flex items-center justify-between">
        <p class="text-green-700 dark:text-green-300 font-medium">You're now a Pro member! Enjoy unlimited quiz generation.</p>
        <button @click="subscriptionSuccess = false" class="text-green-500 hover:text-green-700 dark:text-green-400">&times;</button>
      </div>

      <!-- Welcome + Subscription Badge -->
      <div class="flex flex-wrap items-start justify-between gap-3 mb-6 sm:mb-8">
        <h1 class="text-2xl sm:text-4xl font-bold">
          <span class="gradient-text">Welcome{{ userName ? `, ${userName}` : '' }}</span> 👋
        </h1>

        <div v-if="subscriptionBadgeLabel" class="flex flex-col items-end gap-1.5">
          <UPopover>
            <span
              class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-xl border cursor-pointer select-none"
              :class="subscriptionBadgeColor"
            >
              <span class="w-1.5 h-1.5 rounded-full" :class="subscriptionDotColor" />
              {{ subscriptionBadgeLabel }}
            </span>
            <template #content>
              <div class="px-4 py-3 text-sm text-slate-700 dark:text-slate-300 max-w-56">
                <p class="font-semibold mb-1">{{ subscriptionBadgeLabel }}</p>
                <p class="text-xs text-slate-500 dark:text-slate-400">{{ subscriptionBadgeDetail }}</p>
                <p
                  v-if="horenQuotaLine"
                  class="text-xs text-slate-500 dark:text-slate-400 mt-1.5 pt-1.5 border-t border-slate-200/70 dark:border-slate-700/70"
                >
                  {{ horenQuotaLine }}
                </p>
                <p
                  v-if="lesenQuotaLine"
                  class="text-xs text-slate-500 dark:text-slate-400 mt-1.5"
                  :class="{ 'pt-1.5 border-t border-slate-200/70 dark:border-slate-700/70': !horenQuotaLine }"
                >
                  {{ lesenQuotaLine }}
                </p>
                <!-- Upgrade prompt — shown when any limit the user could
                     resolve by upgrading has been reached. Pro users at the
                     weekly Hören/Lesen cap don't see this (they need to
                     wait for the rolling window; upgrading wouldn't help). -->
                <div
                  v-if="needsUpgrade"
                  class="mt-2 pt-2 border-t border-slate-200/70 dark:border-slate-700/70"
                >
                  <p
                    v-if="upgradeReasonLabel"
                    class="text-xs font-medium text-amber-700 dark:text-amber-300 mb-1.5 flex items-center gap-1"
                  >
                    <UIcon name="i-lucide-alert-triangle" class="w-3.5 h-3.5" />
                    {{ upgradeReasonLabel }}
                  </p>
                  <button
                    @click="showSubscriptionModal = true"
                    class="w-full px-3 py-1.5 btn-gradient rounded-lg text-xs font-semibold"
                  >
                    Upgrade to Pro
                  </button>
                </div>
              </div>
            </template>
          </UPopover>
          <span
            v-if="quizzesRemainingLabel"
            class="text-xs text-slate-500 dark:text-slate-400 font-medium"
          >{{ quizzesRemainingLabel }}</span>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mb-10">
        <NuxtLink to="/subjects/new">
          <button class="px-6 py-2.5 btn-gradient rounded-xl font-semibold">
            + Create Subject
          </button>
        </NuxtLink>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 mb-8 sm:mb-10">
        <div class="glass-card rounded-2xl p-6 text-center">
          <p class="text-slate-500 dark:text-slate-400 text-sm mb-2">Total Quizzes</p>
          <p class="text-4xl font-bold gradient-text">{{ stats.totalQuizzes }}</p>
        </div>
        <div class="glass-card rounded-2xl p-6 text-center">
          <p class="text-slate-500 dark:text-slate-400 text-sm mb-2">Average Score</p>
          <p class="text-4xl font-bold gradient-text">{{ stats.averageScore }}%</p>
        </div>
      </div>

      <!-- Predefined Subjects (only the ones the user has added) -->
      <div class="mb-8 sm:mb-10">
        <div class="flex items-center justify-between mb-4 gap-3 flex-wrap">
          <h2 class="text-2xl font-bold text-slate-900 dark:text-white">My Subjects</h2>
          <button
            v-if="availablePredefinedAgents.length > 0"
            type="button"
            @click="showBrowseLibrary = true"
            class="px-3 py-1.5 rounded-lg font-semibold text-xs border border-slate-300 dark:border-slate-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition flex items-center gap-1.5"
          >
            <UIcon name="i-lucide-library" class="w-3.5 h-3.5" />
            Browse library
            <span class="px-1.5 py-0.5 text-[10px] font-bold rounded-full bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300">
              {{ availablePredefinedAgents.length }}
            </span>
          </button>
        </div>

        <div
          v-if="myPredefinedAgents.length === 0"
          class="glass-card rounded-2xl p-8 text-center"
        >
          <UIcon name="i-lucide-bookmark-plus" class="w-10 h-10 text-slate-400 mx-auto mb-3" />
          <p class="text-sm text-slate-700 dark:text-slate-300 mb-1 font-semibold">No subjects yet in your library.</p>
          <p class="text-xs text-slate-500 dark:text-slate-400 mb-4">
            Add the exams or grammar levels you're preparing for and they'll show up here.
          </p>
          <button
            v-if="availablePredefinedAgents.length > 0"
            type="button"
            @click="showBrowseLibrary = true"
            class="px-4 py-2 btn-gradient rounded-xl text-sm font-semibold"
          >
            Browse library
          </button>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div
            v-for="agent in myPredefinedAgents"
            :key="agent.slug"
            class="glass-card rounded-2xl overflow-hidden cursor-pointer hover:shadow-xl transition-all hover:-translate-y-0.5"
            :style="{ boxShadow: `0 8px 24px -12px ${agent.color || '#3B82F6'}55` }"
            @click="openPredefined(agent)"
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
                  <span
                    v-if="agent.status === 'preview'"
                    class="px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide rounded-full text-amber-700 dark:text-amber-300 bg-amber-500/10 border border-amber-500/30"
                  >Preview</span>
                  <span
                    v-else
                    class="px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide rounded-full text-slate-700 dark:text-slate-300 bg-slate-500/10 border border-slate-500/20"
                  >Predefined</span>
                </div>
                <p class="text-xs text-slate-500 dark:text-slate-400">
                  {{ agent.status === 'preview' ? 'Early access — try the listening practice prototype.' : 'Ready-to-quiz with grounded AI generation.' }}
                </p>
              </div>
              <button
                type="button"
                @click.stop="openPredefined(agent)"
                :disabled="provisioningSlug === agent.slug"
                class="px-3 py-1.5 rounded-lg font-semibold text-xs text-white disabled:opacity-50 transition-transform hover:-translate-y-0.5 flex-shrink-0"
                :style="{ background: agent.color || '#3B82F6' }"
              >
                {{ provisioningSlug === agent.slug ? '...' : (agent.status === 'preview' ? 'Try preview →' : 'Start →') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Recommended for You -->
      <div v-if="weakTopics.length > 0" class="mb-8 sm:mb-10">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Recommended for You</h2>
          <span class="text-xs text-slate-500 dark:text-slate-400">Topics with &lt; 70% accuracy</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4">
          <div
            v-for="t in weakTopics"
            :key="`${t.origin}:${t.topic}:${t.source_id || t.subject_id || ''}`"
            class="glass-card rounded-2xl p-4 sm:p-5 flex items-start gap-4"
          >
            <div class="flex-shrink-0">
              <span class="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-orange-500/10 text-orange-600 dark:text-orange-300">
                <UIcon name="i-lucide-target" class="w-6 h-6" />
              </span>
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex items-start justify-between gap-3 mb-1 flex-wrap">
                <p class="font-semibold text-slate-900 dark:text-white truncate">{{ t.topic }}</p>
                <span
                  class="px-2 py-0.5 rounded-full text-xs font-bold flex-shrink-0"
                  :class="accuracyBadge(t.accuracy)"
                >{{ t.accuracy }}%</span>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 mb-3">
                <span v-if="weakTopicAgentName(t)" class="text-orange-600 dark:text-orange-400 font-medium">{{ weakTopicAgentName(t) }}</span>
                <span v-else-if="t.subject_name">{{ t.subject_name }}</span>
                <span v-if="t.source_name"> · {{ t.source_name }}</span>
                <span> · {{ t.correct }}/{{ t.total }} correct</span>
              </p>
              <button
                type="button"
                @click="practiceWeakTopic(t)"
                :disabled="practicingTopicKey === topicKey(t)"
                class="px-4 py-1.5 btn-gradient rounded-lg text-xs font-semibold disabled:opacity-50"
              >
                {{ practicingTopicKey === topicKey(t) ? 'Loading...' : `Practice ${weakTopicAgentName(t) ? 'chapter' : 'topic'}` }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Subjects -->
      <div class="mb-10">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Recent Subjects</h2>
          <NuxtLink to="/subjects" class="text-sm font-medium gradient-text hover:opacity-80 transition-opacity">View all &rarr;</NuxtLink>
        </div>

        <div v-if="recentSubjects.length === 0" class="text-slate-500 dark:text-slate-400 text-sm">
          No subjects yet. <NuxtLink to="/subjects/new" class="gradient-text font-medium hover:opacity-80">Create your first subject</NuxtLink>.
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="subject in recentSubjects"
            :key="subject.id"
            class="glass-card rounded-2xl hover:shadow-xl hover:shadow-blue-500/10 transition-all hover:-translate-y-0.5 cursor-pointer overflow-hidden"
            @click="navigateTo(`/subjects/${subject.id}`)"
          >
            <div class="h-1 rounded-t-2xl" :style="{ backgroundColor: subject.color || '#3B82F6' }"></div>
            <div class="p-4">
              <div class="flex items-center gap-3 mb-2">
                <div class="w-3 h-3 rounded-full flex-shrink-0" :style="{ backgroundColor: subject.color || '#3B82F6' }"></div>
                <h3 class="font-bold text-slate-900 dark:text-white truncate">{{ subject.name }}</h3>
              </div>
              <p class="text-sm text-slate-500 dark:text-slate-400">
                {{ subject.quiz_count }} {{ subject.quiz_count === 1 ? 'quiz' : 'quizzes' }}
              </p>
            </div>
          </div>
        </div>
      </div>

    </UDashboardPanelContent>

    <SubscriptionModal v-model="showSubscriptionModal" />

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
const route = useRoute()

const { user: subUser, fetchUser: fetchSubscriptionUser, refreshUser } = useSubscription()

const userName = computed(() => subUser.value?.name || '')
const subscriptionSuccess = ref(false)
const showSubscriptionModal = ref(false)
const showBrowseLibrary = ref(false)

// Slugs of predefined agents the user has added to their library.
// Backed by the GET /predefined/added endpoint. Filters the dashboard's
// predefined-cards grid AND gates per-feature UI (e.g. Hören quota only
// surfaces when the user has Hören in their library).
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

// Both A2 and B1 Hören count as "Hören in library" for the purpose of
// surfacing the shared quota in the subscription badge popover. The
// backend cap counts all audio_listening quizzes regardless of level.
const HOREN_SLUGS = ['deutsch_a2_horen', 'deutsch_b1_horen'] as const
const horenSlugInLibrary = computed<string | null>(() =>
  HOREN_SLUGS.find((s) => addedPredefinedSlugs.value.includes(s)) ?? null
)
const hasHorenInLibrary = computed(() => horenSlugInLibrary.value !== null)

// Hören quota — fetched only when the user has any Hören level in their library.
// Surfaced in the subscription badge popover so users can see their current
// Hören allowance without leaving the dashboard. Independent of the generic
// quiz count because Hören is the expensive feature with its own per-feature cap.
type HorenQuota = {
  tier: 'pro' | 'trial' | 'expired'
  limit: number
  used: number
  remaining: number
  period: 'week' | 'trial' | 'none'
}
const horenQuota = ref<HorenQuota | null>(null)

async function loadHorenQuota() {
  const slugForQuota = horenSlugInLibrary.value
  if (!slugForQuota) {
    horenQuota.value = null
    return
  }
  try {
    horenQuota.value = await $fetch<HorenQuota>(
      `${config.public.apiBase}/horen/${slugForQuota}/quota`,
      { credentials: 'include' }
    )
  } catch {
    horenQuota.value = null
  }
}

const horenQuotaLine = computed<string>(() => {
  const q = horenQuota.value
  if (!q) return ''
  if (q.tier === 'expired') return ''  // No Hören access — don't add noise to the popover
  const periodWord = q.period === 'week' ? 'in 7 Tagen' : 'in der Probezeit'
  return `Hören: ${q.remaining} von ${q.limit} ${periodWord}`
})

// Lesen — separate quota from Hören (text-only, ~10× cheaper to generate).
// Only fetched once the user has B1 Lesen in their library so the popover
// doesn't show an irrelevant cap to users who haven't opted into Lesen.
const LESEN_SLUGS = ['deutsch_a2_lesen', 'deutsch_b1_lesen'] as const
const lesenSlugInLibrary = computed<string | null>(() =>
  LESEN_SLUGS.find((s) => addedPredefinedSlugs.value.includes(s)) ?? null
)
const hasLesenInLibrary = computed(() => lesenSlugInLibrary.value !== null)
const lesenQuota = ref<HorenQuota | null>(null)

async function loadLesenQuota() {
  const slugForQuota = lesenSlugInLibrary.value
  if (!slugForQuota) {
    lesenQuota.value = null
    return
  }
  try {
    lesenQuota.value = await $fetch<HorenQuota>(
      `${config.public.apiBase}/lesen/${slugForQuota}/quota`,
      { credentials: 'include' }
    )
  } catch {
    lesenQuota.value = null
  }
}

const lesenQuotaLine = computed<string>(() => {
  const q = lesenQuota.value
  if (!q) return ''
  if (q.tier === 'expired') return ''
  const periodWord = q.period === 'week' ? 'in 7 Tagen' : 'in der Probezeit'
  return `Lesen: ${q.remaining} von ${q.limit} ${periodWord}`
})

// ── Upgrade prompt logic ────────────────────────────────────────────────────
// Surface an "Upgrade to Pro" CTA whenever the user has hit a limit they
// could resolve by upgrading. We deliberately DON'T trigger for Pro users
// at their weekly Hören/Lesen cap — upgrading wouldn't help them; they
// just need to wait for the rolling 7-day window. The play pages already
// show that wait time inline.

const trialQuizzesExhausted = computed(() => {
  const sub = subUser.value?.subscription
  if (!sub || sub.status !== 'trial_active') return false
  const limit = sub.trial_quiz_limit ?? 3
  const used = subUser.value?.quizzes_count ?? 0
  return used >= limit
})

const horenLimitedAndCanUpgrade = computed(() => {
  const q = horenQuota.value
  if (!q) return false
  return q.tier !== 'pro' && !q.remaining  // trial-cap or no-sub — upgrading fixes both
})

const lesenLimitedAndCanUpgrade = computed(() => {
  const q = lesenQuota.value
  if (!q) return false
  return q.tier !== 'pro' && !q.remaining
})

const subscriptionExpired = computed(() => {
  const status = subUser.value?.subscription?.status || ''
  return status === 'trial_expired' || status.startsWith('expired_')
})

const needsUpgrade = computed(() =>
  subscriptionExpired.value
  || trialQuizzesExhausted.value
  || horenLimitedAndCanUpgrade.value
  || lesenLimitedAndCanUpgrade.value
)

// One-line reason for the badge popover so the user knows WHY they're
// being prompted. First match wins (most-blocking first).
const upgradeReasonLabel = computed<string>(() => {
  if (subscriptionExpired.value) return 'Subscription expired'
  if (trialQuizzesExhausted.value) return 'Trial quiz limit reached'
  if (horenLimitedAndCanUpgrade.value) return 'Hören trial limit reached'
  if (lesenLimitedAndCanUpgrade.value) return 'Lesen trial limit reached'
  return ''
})

const subscriptionBadgeLabel = computed(() => {
  const status = subUser.value?.subscription?.status || ''
  if (status === 'trial_active') return 'Trial'
  if (status === 'trial_expired') return 'Expired'
  if (status.startsWith('expired_')) return 'Expired'
  if (status.startsWith('active_')) return 'Pro'
  return ''
})

const subscriptionBadgeDetail = computed(() => {
  const sub = subUser.value?.subscription
  if (!sub) return ''
  const status = sub.status || ''

  if (status === 'trial_active') {
    const limit = sub.trial_quiz_limit ?? 3
    const used = subUser.value?.quizzes_count ?? 0
    const remaining = Math.max(0, limit - used)
    const parts = [`${remaining} ${remaining === 1 ? 'quiz' : 'quizzes'} remaining`]
    if (sub.trial_ends_at) parts.push(`Expires ${new Date(sub.trial_ends_at).toLocaleDateString()}`)
    return parts.join(' · ')
  }
  if (status === 'trial_expired') {
    return sub.trial_ends_at ? `Expired on ${new Date(sub.trial_ends_at).toLocaleDateString()}` : 'Trial expired'
  }
  if (status.startsWith('expired_')) {
    return sub.ends_at ? `Expired on ${new Date(sub.ends_at).toLocaleDateString()}` : 'Subscription expired'
  }
  if (status.startsWith('active_') && sub.ends_at) {
    return `Renews ${new Date(sub.ends_at).toLocaleDateString()}`
  }
  return ''
})

const subscriptionBadgeColor = computed(() => {
  const status = subUser.value?.subscription?.status || ''
  if (status.startsWith('active_')) return 'text-green-700 dark:text-green-300 bg-green-500/10 border-green-500/20'
  if (status === 'trial_active') return 'text-blue-700 dark:text-blue-300 bg-blue-500/10 border-blue-500/20'
  return 'text-red-700 dark:text-red-300 bg-red-500/10 border-red-500/20'
})

const subscriptionDotColor = computed(() => {
  const status = subUser.value?.subscription?.status || ''
  if (status.startsWith('active_')) return 'bg-green-500'
  if (status === 'trial_active') return 'bg-blue-500'
  return 'bg-red-500'
})

const quizzesRemainingLabel = computed(() => {
  const sub = subUser.value?.subscription
  if (!sub || sub.status !== 'trial_active') return ''
  const limit = sub.trial_quiz_limit ?? 3
  const used = subUser.value?.quizzes_count ?? 0
  const remaining = Math.max(0, limit - used)
  return `${remaining} ${remaining === 1 ? 'quiz' : 'quizzes'} remaining`
})
const recentSubjects = ref<any[]>([])
const stats = ref({ totalQuizzes: 0, averageScore: 0 })

type WeakTopic = {
  topic: string
  total: number
  correct: number
  accuracy: number
  origin: string  // agent slug ('pmp', 'clf_c02', ...) or 'user'
  chapter_slug: string | null
  subject_id: string | null
  subject_name: string | null
  source_id: string | null
  source_name: string | null
}

const { agents: predefinedAgentsRef, load: loadPredefinedAgents } = usePredefinedSubjects()
const predefinedAgents = computed(() => predefinedAgentsRef.value || [])

// The dashboard grid only shows agents the user has explicitly added.
// Un-added agents live in the Browse Library modal until added.
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
    await $fetch(
      `${config.public.apiBase}/predefined/${slug}/provision`,
      { method: 'POST', credentials: 'include' }
    )
    await loadAddedPredefined()
    // Hören / Lesen quotas become relevant once their respective subjects are
    // added — refresh now so the popover shows the cap without a page reload.
    if ((HOREN_SLUGS as readonly string[]).includes(slug)) await loadHorenQuota()
    if ((LESEN_SLUGS as readonly string[]).includes(slug)) await loadLesenQuota()
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Failed to add subject.')
  } finally {
    addingSlug.value = null
  }
}

const rawWeakTopics = ref<WeakTopic[]>([])
// Hide Hören / Lesen weak topics from the "Recommended for You" list.
// Those features have their own per-feature quota and a separate practice
// flow on the agent page; surfacing them here would invite users to burn
// scarce Hören credits on auto-generated practice quizzes.
const EXCLUDED_WEAK_TOPIC_ORIGINS = new Set<string>([
  ...HOREN_SLUGS,
  ...LESEN_SLUGS,
])
const weakTopics = computed<WeakTopic[]>(() =>
  rawWeakTopics.value.filter((t) => !EXCLUDED_WEAK_TOPIC_ORIGINS.has(t.origin))
)
const provisioningSlug = ref<string | null>(null)
const practicingTopicKey = ref<string | null>(null)

function weakTopicAgentName(t: WeakTopic): string | null {
  const agent = predefinedAgents.value.find((a) => a.slug === t.origin)
  return agent?.name || null
}

const topicKey = (t: WeakTopic) =>
  `${t.origin}:${t.topic}:${t.source_id || t.subject_id || ''}`

const accuracyBadge = (accuracy: number) => {
  if (accuracy >= 50) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300'
  return 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
}

async function provisionPredefined(slug: string): Promise<any | null> {
  const res = await fetch(`${config.public.apiBase}/predefined/${slug}/provision`, {
    method: 'POST',
    credentials: 'include',
  })
  if (res.status === 403) {
    showSubscriptionModal.value = true
    return null
  }
  if (!res.ok) {
    alert(`Failed to start. Please try again.`)
    return null
  }
  return res.json()
}

async function launchPredefined(slug: string) {
  if (provisioningSlug.value) return
  provisioningSlug.value = slug
  try {
    const subject = await provisionPredefined(slug)
    if (subject?.id) await navigateTo(`/subjects/${subject.id}`)
  } finally {
    provisioningSlug.value = null
  }
}

// Routes a predefined card based on its `status`. Live cards go through the
// standard provision-then-navigate flow; preview cards jump straight to the
// preview surface (e.g. /horen/<slug> for the B1 Hören prototype).
function openPredefined(agent: { slug: string; status?: 'live' | 'preview'; preview_path?: string | null }) {
  if (agent.status === 'preview') {
    const path = agent.preview_path || `/horen/${agent.slug}`
    navigateTo(path)
    return
  }
  launchPredefined(agent.slug)
}

async function practiceWeakTopic(t: WeakTopic) {
  practicingTopicKey.value = topicKey(t)
  try {
    const isPredefined = predefinedAgents.value.some((a) => a.slug === t.origin)
    if (isPredefined) {
      const subject = await provisionPredefined(t.origin)
      if (!subject?.id) return
      const url = t.chapter_slug
        ? `/subjects/${subject.id}?focus_chapter=${encodeURIComponent(t.chapter_slug)}`
        : `/subjects/${subject.id}`
      await navigateTo(url)
      return
    }
    if (t.source_id) {
      const params = new URLSearchParams()
      if (t.subject_id) params.set('subject_id', t.subject_id)
      params.set('source_id', t.source_id)
      if (t.source_name) params.set('source_name', t.source_name)
      params.set('focus_topics', t.topic)
      await navigateTo(`/quiz-new?${params.toString()}`)
      return
    }
    if (t.subject_id) {
      await navigateTo(`/subjects/${t.subject_id}`)
    }
  } finally {
    practicingTopicKey.value = null
  }
}

onMounted(async () => {
  loadPredefinedAgents().catch(() => {})
  // Load the user's added predefined subjects FIRST so we know whether to
  // fetch Hören quota and whether to redirect to onboarding.
  await loadAddedPredefined()

  // First-time experience: a user who hasn't added any predefined subjects
  // (and likely hasn't created custom ones either) gets sent to /onboarding
  // for the multi-select welcome screen. This only runs for accounts that
  // truly have nothing — anyone with prior activity stays on the dashboard.
  if (addedPredefinedSlugs.value.length === 0) {
    await navigateTo('/onboarding')
    return
  }

  loadHorenQuota().catch(() => {})
  loadLesenQuota().catch(() => {})

  if (route.query.subscription === 'success') {
    subscriptionSuccess.value = true
    await refreshUser(true)
    navigateTo('/dashboard', { replace: true })
  } else {
    await fetchSubscriptionUser()
  }
  const api = config.public.apiBase

  const [subjectsRes, quizzesRes, resultsRes, weakRes] = await Promise.allSettled([
    fetch(`${api}/subjects`, { credentials: 'include' }),
    fetch(`${api}/quizzes/my_quizzes`, { credentials: 'include' }),
    fetch(`${api}/quizzes/my_results`, { credentials: 'include' }),
    fetch(`${api}/recommendations/weak-topics?limit=4`, { credentials: 'include' }),
  ])

  if (subjectsRes.status === 'fulfilled' && subjectsRes.value.ok) {
    const all = await subjectsRes.value.json()
    recentSubjects.value = all.slice(0, 6)
  }

  if (quizzesRes.status === 'fulfilled' && quizzesRes.value.ok) {
    const quizzes = await quizzesRes.value.json()
    stats.value.totalQuizzes = quizzes.length
  }

  if (resultsRes.status === 'fulfilled' && resultsRes.value.ok) {
    const results = await resultsRes.value.json()
    if (results.length > 0) {
      const total = results.reduce((sum: number, r: any) => sum + r.score_percentage, 0)
      stats.value.averageScore = Math.round(total / results.length)
    }
  }

  if (weakRes.status === 'fulfilled' && weakRes.value.ok) {
    rawWeakTopics.value = await weakRes.value.json()
  }
})
</script>
