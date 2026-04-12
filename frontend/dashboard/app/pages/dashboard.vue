<template>
  <UDashboardPanel grow>
    <UDashboardPanelContent class="p-6 overflow-y-auto">

      <!-- Subscription Success -->
      <div v-if="subscriptionSuccess" class="mb-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg flex items-center justify-between">
        <p class="text-green-800 dark:text-green-200 font-medium">You're now a Pro member! Enjoy unlimited quiz generation.</p>
        <button @click="subscriptionSuccess = false" class="text-green-600 hover:text-green-800 dark:text-green-400">&times;</button>
      </div>

      <!-- Welcome -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white">
          Welcome{{ userName ? `, ${userName}` : '' }} 👋
        </h1>
      </div>

      <!-- Subscription Status -->
      <div v-if="subUser" class="mb-8">
        <div
          class="rounded-lg shadow p-5 flex items-center justify-between"
          :class="subscriptionCardClass"
        >
          <div>
            <p class="text-sm font-medium" :class="subscriptionTextMuted">Subscription</p>
            <p class="text-lg font-bold" :class="subscriptionTextPrimary">{{ subUser.subscription?.label || 'No Plan' }}</p>
            <p v-if="subscriptionDetail" class="text-sm mt-1" :class="subscriptionTextMuted">
              {{ subscriptionDetail }}
            </p>
          </div>
          <button
            v-if="!subUser.subscription?.is_eligible"
            @click="showSubscriptionModal = true"
            class="px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold text-sm"
          >
            Upgrade to Pro
          </button>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mb-10">
        <NuxtLink to="/subjects/new">
          <button class="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold">
            + Create Subject
          </button>
        </NuxtLink>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
          <p class="text-gray-600 dark:text-gray-400 text-sm mb-2">Total Quizzes</p>
          <p class="text-4xl font-bold text-gray-900 dark:text-white">{{ stats.totalQuizzes }}</p>
        </div>
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
          <p class="text-gray-600 dark:text-gray-400 text-sm mb-2">Average Score</p>
          <p class="text-4xl font-bold text-gray-900 dark:text-white">{{ stats.averageScore }}%</p>
        </div>
      </div>

      <!-- Recent Subjects -->
      <div class="mb-10">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Recent Subjects</h2>
          <NuxtLink to="/subjects" class="text-sm text-blue-600 hover:underline">View all →</NuxtLink>
        </div>

        <div v-if="recentSubjects.length === 0" class="text-gray-500 dark:text-gray-400 text-sm">
          No subjects yet. <NuxtLink to="/subjects/new" class="text-blue-600 hover:underline">Create your first subject</NuxtLink>.
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="subject in recentSubjects"
            :key="subject.id"
            class="bg-white dark:bg-gray-800 rounded-xl shadow hover:shadow-md transition-shadow cursor-pointer border border-gray-100 dark:border-gray-700 overflow-hidden"
            @click="navigateTo(`/subjects/${subject.id}`)"
          >
            <div class="h-1.5" :style="{ backgroundColor: subject.color || '#3B82F6' }"></div>
            <div class="p-4">
              <div class="flex items-center gap-3 mb-2">
                <div class="w-3 h-3 rounded-full flex-shrink-0" :style="{ backgroundColor: subject.color || '#3B82F6' }"></div>
                <h3 class="font-bold text-gray-900 dark:text-white truncate">{{ subject.name }}</h3>
              </div>
              <p class="text-sm text-gray-500 dark:text-gray-400">
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
const recentSubjects = ref<any[]>([])
const stats = ref({ totalQuizzes: 0, averageScore: 0 })

const subscriptionDetail = computed(() => {
  const sub = subUser.value?.subscription
  if (!sub) return ''
  const status = sub.status || ''

  if (status.startsWith('active_') && sub.ends_at) {
    const ends = new Date(sub.ends_at)
    const now = new Date()
    const daysLeft = Math.ceil((ends.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
    return `Renews on ${ends.toLocaleDateString()} (${daysLeft} days left)`
  }
  if (status.startsWith('expired_')) {
    const ends = sub.ends_at ? new Date(sub.ends_at).toLocaleDateString() : ''
    return ends ? `Expired on ${ends}` : 'Subscription expired'
  }
  if (status === 'trial_expired') return 'Your free trial has ended'
  return ''
})

const subscriptionCardClass = computed(() => {
  const status = subUser.value?.subscription?.status || ''
  if (status.startsWith('active_')) return 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800'
  if (status === 'trial_active') return 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800'
  return 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800'
})

const subscriptionTextPrimary = computed(() => {
  const status = subUser.value?.subscription?.status || ''
  if (status.startsWith('active_')) return 'text-green-800 dark:text-green-200'
  if (status === 'trial_active') return 'text-blue-800 dark:text-blue-200'
  return 'text-red-800 dark:text-red-200'
})

const subscriptionTextMuted = computed(() => {
  const status = subUser.value?.subscription?.status || ''
  if (status.startsWith('active_')) return 'text-green-600 dark:text-green-400'
  if (status === 'trial_active') return 'text-blue-600 dark:text-blue-400'
  return 'text-red-600 dark:text-red-400'
})

onMounted(async () => {
  if (route.query.subscription === 'success') {
    subscriptionSuccess.value = true
    await refreshUser()
    navigateTo('/dashboard', { replace: true })
  } else {
    await fetchSubscriptionUser()
  }
  const api = config.public.apiBase

  const [subjectsRes, quizzesRes, resultsRes] = await Promise.allSettled([
    fetch(`${api}/subjects`, { credentials: 'include' }),
    fetch(`${api}/quizzes/my_quizzes`, { credentials: 'include' }),
    fetch(`${api}/quizzes/my_results`, { credentials: 'include' }),
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
})
</script>
