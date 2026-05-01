<script setup lang="ts">
definePageMeta({ layout: 'default' })

const config = useRuntimeConfig()
const router = useRouter()

type Me = {
  id: string
  email: string
  name?: string | null
  has_password?: boolean
  is_pro?: boolean
  subscription?: {
    status?: string
    label?: string
    is_eligible?: boolean
    ends_at?: string | null
    trial_ends_at?: string | null
    status_label?: string
  } | null
}

const me = ref<Me | null>(null)
const isLoading = ref(true)

async function loadMe() {
  isLoading.value = true
  try {
    const data = await $fetch<Me>(`${config.public.apiBase}/users/me`, {
      credentials: 'include',
    })
    me.value = data
  } catch (e) {
    console.error('Failed to load profile', e)
  } finally {
    isLoading.value = false
  }
}

onMounted(loadMe)

// ── Change password ────────────────────────────────────────────────────────
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const pwLoading = ref(false)
const pwError = ref('')
const pwSuccess = ref('')

async function submitChangePassword() {
  pwError.value = ''
  pwSuccess.value = ''
  if (newPassword.value.length < 8) {
    pwError.value = 'New password must be at least 8 characters.'
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    pwError.value = 'New passwords do not match.'
    return
  }
  pwLoading.value = true
  try {
    await $fetch(`${config.public.apiBase}/auth/change-password`, {
      method: 'POST',
      credentials: 'include',
      body: {
        current_password: currentPassword.value,
        new_password: newPassword.value,
      },
    })
    pwSuccess.value = 'Password changed successfully.'
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (e: any) {
    pwError.value = e.data?.detail || e.message || 'Failed to change password.'
  } finally {
    pwLoading.value = false
  }
}

// ── Cancel subscription ────────────────────────────────────────────────────
const cancelLoading = ref(false)

async function cancelSubscription() {
  if (!confirm('Cancel subscription? You\'ll keep Pro access until the end of the current billing period.')) return
  cancelLoading.value = true
  try {
    const res = await $fetch<{ message: string, ends_at: string | null }>(
      `${config.public.apiBase}/subscription/cancel`,
      { method: 'POST', credentials: 'include' },
    )
    alert(res.message)
    await loadMe()
  } catch (e: any) {
    alert(e.data?.detail || e.message || 'Failed to cancel subscription.')
  } finally {
    cancelLoading.value = false
  }
}

// ── Delete account ─────────────────────────────────────────────────────────
const deleteConfirmation = ref('')
const deleteLoading = ref(false)

const canDelete = computed(() => deleteConfirmation.value === 'DELETE')

async function deleteAccount() {
  if (!canDelete.value) return
  if (!confirm('This permanently deletes your account, all subjects, sources, quizzes, and cancels any active subscription. This cannot be undone. Proceed?')) return
  deleteLoading.value = true
  try {
    await $fetch(`${config.public.apiBase}/users/me`, {
      method: 'DELETE',
      credentials: 'include',
    })
    const marketingUrl = config.public.marketingUrl || 'http://localhost:3000'
    window.location.href = `${marketingUrl}/login`
  } catch (e: any) {
    alert(e.data?.detail || e.message || 'Failed to delete account.')
    deleteLoading.value = false
  }
}

// ── Display helpers ────────────────────────────────────────────────────────
const subscriptionLabel = computed(() => me.value?.subscription?.label || 'Trial')
const subscriptionEndsAt = computed(() => {
  const raw = me.value?.subscription?.ends_at || me.value?.subscription?.trial_ends_at
  if (!raw) return null
  return new Date(raw).toLocaleDateString()
})
const isCancelling = computed(() => me.value?.subscription?.status === 'canceling')
const canCancel = computed(() =>
  me.value?.is_pro && !isCancelling.value && me.value?.subscription?.status !== 'trial',
)
</script>

<template>
  <UDashboardPanel grow>
    <UDashboardNavbar class="lg:hidden" title="Profile" />
    <UDashboardPanelContent class="p-4 sm:p-6 overflow-y-auto bg-mesh min-h-full">
      <div class="max-w-3xl mx-auto">
        <div class="mb-6 sm:mb-8">
          <NuxtLink to="/dashboard" class="text-sm text-blue-600 hover:underline">← Back to Dashboard</NuxtLink>
          <h1 class="text-2xl sm:text-4xl font-bold gradient-text mt-2">Profile</h1>
        </div>

        <div v-if="isLoading" class="flex items-center justify-center py-20">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
        </div>

        <div v-else-if="me" class="space-y-6">
          <!-- Account info -->
          <section class="glass-card rounded-2xl p-5 sm:p-6">
            <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-4">Account</h2>
            <dl class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
              <dt class="text-slate-500 dark:text-slate-400">Name</dt>
              <dd class="sm:col-span-2 text-slate-900 dark:text-white font-medium">{{ me.name || '—' }}</dd>
              <dt class="text-slate-500 dark:text-slate-400">Email</dt>
              <dd class="sm:col-span-2 text-slate-900 dark:text-white font-medium">{{ me.email }}</dd>
              <dt class="text-slate-500 dark:text-slate-400">Sign-in method</dt>
              <dd class="sm:col-span-2 text-slate-900 dark:text-white font-medium">
                {{ me.has_password ? 'Email + Password' : 'Google' }}
              </dd>
            </dl>
          </section>

          <!-- Change password -->
          <section v-if="me.has_password" class="glass-card rounded-2xl p-5 sm:p-6">
            <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-1">Change Password</h2>
            <p class="text-sm text-slate-500 dark:text-slate-400 mb-4">
              You'll stay signed in here, but other devices will be signed out.
            </p>
            <form @submit.prevent="submitChangePassword" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Current Password</label>
                <input
                  v-model="currentPassword"
                  type="password"
                  class="w-full px-3 py-2 glass-input rounded-xl text-sm text-slate-900 dark:text-white"
                  required
                />
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">New Password</label>
                  <input
                    v-model="newPassword"
                    type="password"
                    minlength="8"
                    maxlength="72"
                    placeholder="At least 8 characters"
                    class="w-full px-3 py-2 glass-input rounded-xl text-sm text-slate-900 dark:text-white"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Confirm New Password</label>
                  <input
                    v-model="confirmPassword"
                    type="password"
                    minlength="8"
                    maxlength="72"
                    class="w-full px-3 py-2 glass-input rounded-xl text-sm text-slate-900 dark:text-white"
                    required
                  />
                </div>
              </div>
              <div v-if="pwSuccess" class="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-700 dark:text-emerald-400 text-sm">
                {{ pwSuccess }}
              </div>
              <div v-if="pwError" class="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-700 dark:text-red-400 text-sm">
                {{ pwError }}
              </div>
              <button
                type="submit"
                :disabled="pwLoading"
                class="px-5 py-2 btn-gradient rounded-xl text-sm font-medium disabled:opacity-50"
              >
                {{ pwLoading ? 'Saving...' : 'Change password' }}
              </button>
            </form>
          </section>

          <!-- Subscription -->
          <section class="glass-card rounded-2xl p-5 sm:p-6">
            <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-1">Subscription</h2>
            <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
              <div>
                <p class="text-base font-medium text-slate-900 dark:text-white">{{ subscriptionLabel }}</p>
                <p v-if="subscriptionEndsAt" class="text-sm text-slate-500 dark:text-slate-400">
                  {{ isCancelling ? 'Ends on' : 'Renews on' }} {{ subscriptionEndsAt }}
                </p>
              </div>
              <span
                class="px-2 py-0.5 rounded-full text-xs font-bold"
                :class="me.is_pro ? 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400' : 'bg-slate-500/10 text-slate-600 dark:text-slate-400'"
              >
                {{ me.is_pro ? 'Active' : 'Inactive' }}
              </span>
            </div>
            <div v-if="isCancelling" class="p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl text-amber-700 dark:text-amber-400 text-sm mb-3">
              Your subscription is set to cancel at the end of the current billing period.
            </div>
            <button
              v-if="canCancel"
              @click="cancelSubscription"
              :disabled="cancelLoading"
              class="px-5 py-2 rounded-xl text-sm font-medium border border-red-500/30 text-red-600 dark:text-red-400 hover:bg-red-500/10 disabled:opacity-50"
            >
              {{ cancelLoading ? 'Cancelling...' : 'Cancel subscription' }}
            </button>
            <p v-else-if="!me.is_pro" class="text-sm text-slate-500 dark:text-slate-400">
              No active paid subscription.
            </p>
          </section>

          <!-- Danger zone -->
          <section class="glass-card rounded-2xl p-5 sm:p-6 border border-red-500/20">
            <h2 class="text-lg font-bold text-red-600 dark:text-red-400 mb-1">Delete account</h2>
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-4">
              Permanently deletes your account, all subjects, sources, quizzes, and cancels any active subscription.
              This cannot be undone.
            </p>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
              Type <span class="font-mono font-bold">DELETE</span> to confirm
            </label>
            <input
              v-model="deleteConfirmation"
              type="text"
              class="w-full sm:w-64 px-3 py-2 glass-input rounded-xl text-sm text-slate-900 dark:text-white mb-3"
              placeholder="DELETE"
            />
            <div>
              <button
                @click="deleteAccount"
                :disabled="!canDelete || deleteLoading"
                class="px-5 py-2 rounded-xl text-sm font-medium bg-red-600 text-white hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ deleteLoading ? 'Deleting...' : 'Delete my account' }}
              </button>
            </div>
          </section>
        </div>
      </div>
    </UDashboardPanelContent>
  </UDashboardPanel>
</template>
