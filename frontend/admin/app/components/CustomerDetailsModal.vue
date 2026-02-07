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
  is_published?: boolean
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
              class="p-3 bg-gray-50 dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700 flex items-start justify-between"
              @click.stop
            >
              <div class="flex-1">
                <p class="font-medium">{{ quiz.title }}</p>
                <p class="text-xs text-gray-500 mt-1">
                  Created {{ formatDate(quiz.created_at) }}
                </p>
              </div>
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
          <p v-else class="text-gray-500 text-sm">No quizzes</p>
        </div>
      </div>
      </div>
    </UCard>
  </UModal>
</template>
