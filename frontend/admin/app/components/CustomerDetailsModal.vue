<template>
  <UModal v-model="isOpen" :prevent-close="loading">
    <UCard class="w-full max-w-4xl">
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold">Customer Details</h2>
          <UButton
            variant="ghost"
            icon="i-lucide-x"
            @click="isOpen = false"
          />
        </div>
      </template>

      <div v-if="loading" class="flex justify-center py-8">
        <USkeleton class="h-12 w-full" />
      </div>

      <div v-else-if="error" class="text-center py-8">
        <p class="text-red-500">{{ error }}</p>
        <UButton label="Close" @click="isOpen = false" class="mt-4" />
      </div>

      <div v-else-if="user">
        <!-- User Info Section -->
        <div class="space-y-4 p-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm font-medium text-gray-500">Name</p>
              <p class="text-lg font-semibold">{{ user.name || 'Unnamed' }}</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-500">Email</p>
              <p class="text-lg font-semibold">{{ user.email }}</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-500">Status</p>
              <div class="flex gap-2 mt-1">
                <UBadge variant="subtle">
                  {{ user.is_pro ? 'Pro' : 'Free' }}
                </UBadge>
                <UBadge v-if="user.is_admin" variant="subtle">
                  Admin
                </UBadge>
              </div>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-500">Joined</p>
              <p class="text-lg font-semibold">{{ formatDate(user.created_at) }}</p>
            </div>
          </div>
        </div>

        <!-- Subscription Section -->
        <div class="p-4">
          <h3 class="text-lg font-semibold mb-4">Subscription</h3>
          <div v-if="user.subscription" class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm font-medium text-gray-500">Status</p>
              <UBadge variant="subtle">
                {{ user.subscription.label }}
              </UBadge>
            </div>
            <div v-if="user.subscription.ends_at">
              <p class="text-sm font-medium text-gray-500">Expires</p>
              <p class="text-lg font-semibold">{{ formatDate(user.subscription.ends_at) }}</p>
            </div>
            <div v-if="user.subscription.trial_ends_at">
              <p class="text-sm font-medium text-gray-500">Trial Ends</p>
              <p class="text-lg font-semibold">{{ formatDate(user.subscription.trial_ends_at) }}</p>
            </div>
          </div>
        </div>

        <!-- Quiz Sources Section -->
        <div class="p-4">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold">Quiz Sources (PDFs)</h3>
            <UBadge variant="subtle">{{ user.quiz_sources?.length || 0 }}</UBadge>
          </div>
          <div v-if="user.quiz_sources && user.quiz_sources.length > 0" class="space-y-2">
            <div
              v-for="source in user.quiz_sources"
              :key="source.id"
              class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
            >
              <div class="flex items-center gap-3">
                <UIcon name="i-lucide-file-pdf" class="text-red-500" />
                <div>
                  <p class="font-medium">{{ source.file_name }}</p>
                  <p class="text-xs text-gray-500">
                    Uploaded {{ formatDate(source.upload_date) }}
                    <span v-if="source.start_page || source.end_page">
                      • Pages {{ source.start_page }}-{{ source.end_page }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8">
            <p class="text-gray-500">No quiz sources uploaded</p>
          </div>
        </div>

        <!-- Quizzes Section -->
        <div class="p-4">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold">Quizzes Created</h3>
            <UBadge variant="subtle">{{ user.quizzes?.length || 0 }}</UBadge>
          </div>
          <div v-if="user.quizzes && user.quizzes.length > 0" class="space-y-2">
            <div
              v-for="quiz in user.quizzes"
              :key="quiz.id"
              class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
            >
              <div class="flex-1">
                <p class="font-medium">{{ quiz.title }}</p>
                <p class="text-xs text-gray-500">
                  {{ quiz.num_questions }} questions
                  <span v-if="quiz.time_limit"> • {{ quiz.time_limit }}m time limit</span>
                  • Created {{ formatDate(quiz.generation_date) }}
                </p>
              </div>
              <UBadge variant="subtle">
                {{ quiz.quiz_type }}
              </UBadge>
            </div>
          </div>
          <div v-else class="text-center py-8">
            <p class="text-gray-500">No quizzes created</p>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-3">
          <UButton @click="isOpen = false">Close</UButton>
        </div>
      </template>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
interface SubscriptionInfo {
  status: string
  label: string
  is_eligible: boolean
  ends_at: string | null
  trial_ends_at: string | null
  status_label: string | null
}

interface QuizSourceInfo {
  id: string
  file_name: string
  upload_date: string
  start_page: number | null
  end_page: number | null
}

interface QuizInfo {
  id: string
  source_id: string
  title: string
  quiz_type: string
  num_questions: number
  time_limit: number | null
  content: any
  generation_date: string
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
  quiz_sources: QuizSourceInfo[]
  quizzes: QuizInfo[]
}

const props = defineProps<{
  userId?: string
}>()

const emit = defineEmits<{
  close: []
}>()

const isOpen = defineModel<boolean>('modelValue', { default: false })

const user = ref<UserDetail | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const fetchUserDetails = async () => {
  if (!props.userId) {
    console.log('No userId provided')
    return
  }

  loading.value = true
  error.value = null

  try {
    console.log('Fetching user details for:', props.userId)
    const data = await $fetch<UserDetail>(`/api/admin/users/${props.userId}`)
    console.log('User details fetched:', data)
    user.value = data
  } catch (err: any) {
    console.error('Error fetching user details:', err)
    error.value = err.data?.message || 'Failed to load user details'
  } finally {
    loading.value = false
  }
}

watch(isOpen, async (newVal) => {
  console.log('Modal isOpen changed to:', newVal, 'userId:', props.userId)
  if (newVal && props.userId) {
    await fetchUserDetails()
  }
})

watch(() => props.userId, async (newUserId) => {
  console.log('UserId prop changed to:', newUserId, 'isOpen:', isOpen.value)
  if (isOpen.value && newUserId) {
    await fetchUserDetails()
  }
})
</script>
