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

        <UPopover v-if="subscriptionBadgeLabel">
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
              <button
                v-if="!subUser?.subscription?.is_eligible"
                @click="showSubscriptionModal = true"
                class="mt-2 w-full px-3 py-1.5 btn-gradient rounded-lg text-xs font-semibold"
              >
                Upgrade to Pro
              </button>
            </div>
          </template>
        </UPopover>
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

      <!-- Predefined: PMP -->
      <div class="mb-8 sm:mb-10">
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">Predefined Subjects</h2>
        <div
          class="glass-card rounded-2xl overflow-hidden cursor-pointer hover:shadow-xl hover:shadow-orange-500/10 transition-all hover:-translate-y-0.5"
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
              {{ pmpProvisioning ? 'Loading...' : 'Start PMP →' }}
            </button>
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
                <span v-if="t.origin === 'pmp'" class="text-orange-600 dark:text-orange-400 font-medium">PMP</span>
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
                {{ practicingTopicKey === topicKey(t) ? 'Loading...' : `Practice ${t.origin === 'pmp' ? 'chapter' : 'topic'}` }}
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
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })

const config = useRuntimeConfig()
const route = useRoute()

const { user: subUser, fetchUser: fetchSubscriptionUser, refreshUser, isPro } = useSubscription()

const userName = computed(() => subUser.value?.name || '')
const subscriptionSuccess = ref(false)
const showSubscriptionModal = ref(false)

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
const recentSubjects = ref<any[]>([])
const stats = ref({ totalQuizzes: 0, averageScore: 0 })

type WeakTopic = {
  topic: string
  total: number
  correct: number
  accuracy: number
  origin: 'pmp' | 'user'
  chapter_slug: string | null
  subject_id: string | null
  subject_name: string | null
  source_id: string | null
  source_name: string | null
}

const weakTopics = ref<WeakTopic[]>([])
const pmpProvisioning = ref(false)
const practicingTopicKey = ref<string | null>(null)

const topicKey = (t: WeakTopic) =>
  `${t.origin}:${t.topic}:${t.source_id || t.subject_id || ''}`

const accuracyBadge = (accuracy: number) => {
  if (accuracy >= 50) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300'
  return 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
}

async function provisionPMPSubject(): Promise<any | null> {
  const res = await fetch(`${config.public.apiBase}/predefined/pmp/provision`, {
    method: 'POST',
    credentials: 'include',
  })
  if (res.status === 403) {
    showSubscriptionModal.value = true
    return null
  }
  if (!res.ok) {
    alert('Failed to start PMP. Please try again.')
    return null
  }
  return res.json()
}

async function launchPMP() {
  if (pmpProvisioning.value) return
  pmpProvisioning.value = true
  try {
    const subject = await provisionPMPSubject()
    if (subject?.id) await navigateTo(`/subjects/${subject.id}`)
  } finally {
    pmpProvisioning.value = false
  }
}

async function practiceWeakTopic(t: WeakTopic) {
  practicingTopicKey.value = topicKey(t)
  try {
    if (t.origin === 'pmp') {
      const subject = await provisionPMPSubject()
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
    weakTopics.value = await weakRes.value.json()
  }
})
</script>
