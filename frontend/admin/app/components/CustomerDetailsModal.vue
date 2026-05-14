<script setup lang="ts">
interface SubscriptionInfo {
  status: string
  label: string
  is_eligible: boolean
  ends_at: string | null
  trial_ends_at: string | null
  status_label: string | null
}

interface QuizSource {
  id: string
  name: string
  file_name?: string
  upload_date?: string
  start_page?: number
  end_page?: number
}

interface Quiz {
  id: string
  title: string
  created_at?: string
  generation_date?: string
  is_published?: boolean
  attempt_count?: number
  latest_score?: number | null
  latest_attempt_at?: string | null
  num_questions?: number
}

interface QuizAttempt {
  id: string
  score_percentage: number
  is_passed: boolean
  time_taken_seconds: number | null
  time_remaining_seconds: number | null
  started_at: string | null
  ended_at: string | null
  attempt_date: string | null
  user_answers: any
}

interface QuizResultsResponse {
  quiz_id: string
  quiz_title: string
  num_questions: number
  attempts: QuizAttempt[]
}

interface UserDetail {
  id: string
  email: string
  name: string | null
  created_at: string
  is_admin: boolean
  is_pro: boolean
  quizzes_count: number
  sources_count: number
  subscription: SubscriptionInfo | null
  quiz_sources?: QuizSource[]
  quizzes?: Quiz[]
}

const props = defineProps<{
  modelValue: boolean
  userId: string | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const { data: user, pending, error, execute } = useFetch<UserDetail>(
  () => props.userId ? `/api/admin/users/${props.userId}` : null,
  { immediate: false }
)

const deletingSourceId = ref<string | null>(null)
const deletingQuizId = ref<string | null>(null)

// Inline lazy-loaded attempt history: expandedQuizId tracks which quiz row's
// "View attempts" panel is open; attemptsByQuiz caches loaded results so
// re-opening is instant.
const expandedQuizId = ref<string | null>(null)
const loadingAttemptsId = ref<string | null>(null)
const attemptsByQuiz = ref<Record<string, QuizAttempt[]>>({})

async function toggleAttempts(quizId: string) {
  if (expandedQuizId.value === quizId) {
    expandedQuizId.value = null
    return
  }
  expandedQuizId.value = quizId
  if (attemptsByQuiz.value[quizId]) return
  try {
    loadingAttemptsId.value = quizId
    const res = await $fetch<QuizResultsResponse>(`/api/admin/quizzes/${quizId}/results`)
    attemptsByQuiz.value[quizId] = res.attempts
  } catch (e: any) {
    console.error('Failed to load attempts', e)
    alert(e?.data?.detail || e?.message || 'Failed to load attempts')
    expandedQuizId.value = null
  } finally {
    loadingAttemptsId.value = null
  }
}

function scoreBadgeColor(score: number | null | undefined): 'success' | 'warning' | 'error' | 'gray' {
  if (score === null || score === undefined) return 'gray'
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'error'
}

function formatDuration(seconds: number | null): string {
  if (seconds === null || seconds === undefined) return '—'
  if (seconds < 60) return `${seconds}s`
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return s > 0 ? `${m}m ${s}s` : `${m}m`
}

function formatDateTime(iso: string | null): string {
  if (!iso) return '—'
  try {
    return new Date(iso).toLocaleString('en-US', {
      year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit'
    })
  } catch {
    return '—'
  }
}

async function deleteSource(sourceId: string) {
  if (!confirm('Delete this source and all associated quizzes? This cannot be undone.')) return
  try {
    deletingSourceId.value = sourceId
    await $fetch(`/api/admin/quiz-sources/${sourceId}`, { method: 'DELETE' })
    // refresh user details
    await execute()
  } catch (e: any) {
    console.error('Failed to delete source', e)
    alert(e?.data?.detail || e?.message || 'Failed to delete source')
  } finally {
    deletingSourceId.value = null
  }
}

async function deleteQuiz(quizId: string) {
  if (!confirm('Delete this quiz? This cannot be undone.')) return
  try {
    deletingQuizId.value = quizId
    await $fetch(`/api/admin/quizzes/${quizId}`, { method: 'DELETE' })
    // refresh user details
    await execute()
  } catch (e: any) {
    console.error('Failed to delete quiz', e)
    alert(e?.data?.detail || e?.message || 'Failed to delete quiz')
  } finally {
    deletingQuizId.value = null
  }
}

watch(() => isOpen.value, (newVal) => {
  if (newVal && props.userId) {
    execute()
  }
})

function formatDate(dateString: string | null | undefined): string {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
  } catch {
    return 'N/A'
  }
}
</script>

<template>
  <UModal 
  v-model="isOpen" 
  :prevent-close="pending || deletingSourceId !== null || deletingQuizId !== null" 
  size="xl">
    <UCard @click.stop>
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold">
            {{ user?.name || 'Customer Details' }}
          </h2>
          <UButton
            color="gray"
            variant="ghost"
            icon="i-lucide-x"
            @click="isOpen = false"
          />
        </div>
      </template>

      <div class="max-h-[calc(100vh-200px)] overflow-y-auto">

      <!-- Loading State -->
      <div v-if="pending" class="space-y-4">
        <USkeleton class="h-8 w-full" />
        <USkeleton class="h-6 w-3/4" />
        <USkeleton class="h-6 w-2/3" />
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-8">
        <p class="text-red-500 font-medium">Failed to load customer details</p>
      </div>

      <!-- Content -->
      <div v-else-if="user" class="space-y-6">
        <!-- Customer Info -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm font-medium text-gray-500">Name</p>
            <p class="text-base font-semibold">{{ user.name || 'Unnamed' }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">Email</p>
            <p class="text-base font-semibold">{{ user.email }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">Pro Status</p>
            <UBadge :color="user.is_pro ? 'success' : 'gray'" variant="subtle">
              {{ user.is_pro ? 'Pro' : 'Free' }}
            </UBadge>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">Joined</p>
            <p class="text-base font-semibold">{{ formatDate(user.created_at) }}</p>
          </div>
        </div>

        <!-- Subscription Info -->
        <div v-if="user.subscription" class="border-t pt-4">
          <h3 class="font-semibold mb-3">Subscription</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm font-medium text-gray-500">Status</p>
              <UBadge variant="subtle">{{ user.subscription.label }}</UBadge>
            </div>
            <div v-if="user.subscription.ends_at">
              <p class="text-sm font-medium text-gray-500">Expires</p>
              <p class="text-base font-semibold">{{ formatDate(user.subscription.ends_at) }}</p>
            </div>
            <div v-if="user.subscription.trial_ends_at">
              <p class="text-sm font-medium text-gray-500">Trial Ends</p>
              <p class="text-base font-semibold">{{ formatDate(user.subscription.trial_ends_at) }}</p>
            </div>
          </div>
        </div>

        <!-- Quiz Sources -->
        <div class="border-t pt-4">
          <div class="flex items-center gap-2 mb-3">
            <h3 class="font-semibold">Quiz Sources</h3>
            <UBadge variant="subtle">{{ user.quiz_sources?.length || 0 }}</UBadge>
          </div>
          <div v-if="user.quiz_sources?.length" class="space-y-2">
            <div
              v-for="source in user.quiz_sources"
              :key="source.id"
              class="p-3 bg-gray-50 dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700 flex items-start justify-between"
              @click.stop
            >
              <div class="flex-1">
                <p class="font-medium">{{ source.file_name || source.name }}</p>
                <p class="text-xs text-gray-500 mt-1">
                  {{ formatDate(source.upload_date) }}
                  <span v-if="source.start_page || source.end_page">
                    • Pages {{ source.start_page }}-{{ source.end_page }}
                  </span>
                </p>
              </div>
              <UButton
                color="red"
                variant="ghost"
                size="sm"
                icon="i-lucide-trash-2"
                :loading="deletingSourceId === source.id"
                @click.stop="deleteSource(source.id)"
              />
            </div>
          </div>
          <p v-else class="text-gray-500 text-sm">No quiz sources</p>
        </div>

        <!-- Quizzes -->
        <div class="border-t pt-4">
          <div class="flex items-center gap-2 mb-3">
            <h3 class="font-semibold">Quizzes</h3>
            <UBadge variant="subtle">{{ user.quizzes?.length || 0 }}</UBadge>
          </div>
          <div v-if="user.quizzes?.length" class="space-y-2">
            <div
              v-for="quiz in user.quizzes"
              :key="quiz.id"
              class="bg-gray-50 dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700"
              @click.stop
            >
              <div class="p-3 flex items-start justify-between gap-3">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 flex-wrap mb-1">
                    <p class="font-medium truncate">{{ quiz.title }}</p>
                    <UBadge
                      v-if="quiz.latest_score !== null && quiz.latest_score !== undefined"
                      :color="scoreBadgeColor(quiz.latest_score)"
                      variant="subtle"
                      size="xs"
                    >
                      {{ Math.round(quiz.latest_score) }}%
                    </UBadge>
                    <UBadge
                      v-else
                      color="gray"
                      variant="subtle"
                      size="xs"
                    >
                      Not attempted
                    </UBadge>
                  </div>
                  <p class="text-xs text-gray-500">
                    Created {{ formatDate(quiz.created_at || quiz.generation_date) }}
                    <span v-if="(quiz.attempt_count || 0) > 0">
                      · {{ quiz.attempt_count }} attempt{{ quiz.attempt_count === 1 ? '' : 's' }}
                    </span>
                  </p>
                </div>
                <div class="flex items-center gap-1 shrink-0">
                  <UButton
                    v-if="(quiz.attempt_count || 0) > 0"
                    color="primary"
                    variant="ghost"
                    size="sm"
                    :icon="expandedQuizId === quiz.id ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'"
                    :loading="loadingAttemptsId === quiz.id"
                    @click.stop="toggleAttempts(quiz.id)"
                  >
                    Attempts
                  </UButton>
                  <UButton
                    color="red"
                    variant="ghost"
                    size="sm"
                    icon="i-lucide-trash-2"
                    :loading="deletingQuizId === quiz.id"
                    @click.stop="deleteQuiz(quiz.id)"
                  />
                </div>
              </div>

              <!-- Expandable attempt list -->
              <div
                v-if="expandedQuizId === quiz.id"
                class="border-t border-gray-200 dark:border-gray-700 px-3 py-2 space-y-2 bg-white dark:bg-gray-900"
              >
                <div v-if="loadingAttemptsId === quiz.id" class="text-xs text-gray-500 py-2">
                  Loading attempts…
                </div>
                <div v-else-if="!attemptsByQuiz[quiz.id]?.length" class="text-xs text-gray-500 py-2">
                  No attempts recorded.
                </div>
                <div
                  v-for="(attempt, idx) in attemptsByQuiz[quiz.id]"
                  :key="attempt.id"
                  class="flex items-center gap-3 text-xs py-1.5"
                >
                  <span class="text-gray-400 w-6">#{{ (attemptsByQuiz[quiz.id]?.length || 0) - idx }}</span>
                  <UBadge :color="scoreBadgeColor(attempt.score_percentage)" variant="subtle" size="xs">
                    {{ Math.round(attempt.score_percentage) }}%
                  </UBadge>
                  <UBadge :color="attempt.is_passed ? 'success' : 'error'" variant="soft" size="xs">
                    {{ attempt.is_passed ? 'Passed' : 'Failed' }}
                  </UBadge>
                  <span class="text-gray-500">
                    {{ formatDuration(attempt.time_taken_seconds) }}
                  </span>
                  <span class="text-gray-500 ml-auto">
                    {{ formatDateTime(attempt.attempt_date) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <p v-else class="text-gray-500 text-sm">No quizzes</p>
        </div>
      </div>
      </div>
    </UCard>
  </UModal>
</template>
