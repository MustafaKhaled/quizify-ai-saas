<script setup lang="ts">
definePageMeta({
  layout: 'auth'
})

const config = useRuntimeConfig()
const route = useRoute()
const status = ref<'loading' | 'pending' | 'success' | 'error'>('loading')
const errorMessage = ref('')
const userEmail = ref('')

const resendLoading = ref(false)
const resendMessage = ref('')

const handleResend = async () => {
  if (!userEmail.value) {
    resendMessage.value = 'Please log in again to resend verification.'
    return
  }
  resendLoading.value = true
  resendMessage.value = ''
  try {
    await $fetch(`${config.public.apiBase}/auth/resend-verification`, {
      method: 'POST',
      body: { email: userEmail.value }
    })
    resendMessage.value = 'Verification email sent! Check your inbox.'
  } catch {
    resendMessage.value = 'Failed to resend. Please try again.'
  } finally {
    resendLoading.value = false
  }
}

onMounted(async () => {
  const token = route.query.token as string | undefined

  userEmail.value = localStorage.getItem('user_email') || ''

  // No token — user was redirected here because they're unverified
  if (!token) {
    status.value = 'pending'
    return
  }

  try {
    const response = await fetch(`${config.public.apiBase}/auth/verify-email?token=${encodeURIComponent(token)}`, {
      credentials: 'include'
    })

    if (response.ok) {
      status.value = 'success'
      setTimeout(() => {
        navigateTo('/dashboard?verified=true')
      }, 2000)
    } else {
      const data = await response.json().catch(() => null)
      status.value = 'error'
      errorMessage.value = data?.detail || 'Verification failed. The link may be expired.'
    }
  } catch (e: any) {
    status.value = 'error'
    errorMessage.value = 'Something went wrong. Please try again.'
  }
})
</script>

<template>
  <div class="max-w-md w-full mx-auto text-center glass-card-elevated rounded-2xl p-8">
    <!-- Loading -->
    <div v-if="status === 'loading'">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
      <h1 class="text-xl font-bold gradient-text">Verifying your email...</h1>
    </div>

    <!-- Pending: user hasn't verified yet -->
    <div v-else-if="status === 'pending'">
      <div class="w-16 h-16 bg-yellow-500/15 backdrop-blur-sm rounded-full flex items-center justify-center mx-auto mb-4">
        <UIcon name="i-lucide-mail" class="w-8 h-8 text-yellow-500" />
      </div>
      <h1 class="text-2xl font-bold gradient-text mb-2">Verify your email</h1>
      <p v-if="userEmail" class="text-slate-500 dark:text-slate-400 mb-2">
        We sent a verification link to <strong class="text-slate-900 dark:text-white">{{ userEmail }}</strong>
      </p>
      <p v-else class="text-slate-500 dark:text-slate-400 mb-2">
        Please check your inbox for the verification link.
      </p>
      <p class="text-sm text-slate-500 dark:text-slate-400 mb-6">
        Click the link in the email to activate your account. The link expires in 24 hours.
      </p>

      <div v-if="resendMessage" class="p-3 mb-4 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-700 dark:text-blue-300 text-sm">
        {{ resendMessage }}
      </div>

      <button
        @click="handleResend"
        :disabled="resendLoading"
        class="gradient-text font-medium text-sm disabled:opacity-50"
      >
        {{ resendLoading ? 'Sending...' : "Didn't receive it? Resend email" }}
      </button>

      <p class="text-slate-500 dark:text-slate-400 mt-6">
        <NuxtLink to="/auth/login" class="gradient-text font-medium">
          Back to Sign in
        </NuxtLink>
      </p>
    </div>

    <!-- Success -->
    <div v-else-if="status === 'success'">
      <div class="w-16 h-16 bg-green-500/15 backdrop-blur-sm rounded-full flex items-center justify-center mx-auto mb-4">
        <UIcon name="i-lucide-check" class="w-8 h-8 text-green-500" />
      </div>
      <h1 class="text-2xl font-bold gradient-text mb-2">Email verified!</h1>
      <p class="text-slate-500 dark:text-slate-400 mb-4">Your account is now active. Redirecting to dashboard...</p>
    </div>

    <!-- Error -->
    <div v-else>
      <div class="w-16 h-16 bg-red-500/15 backdrop-blur-sm rounded-full flex items-center justify-center mx-auto mb-4">
        <UIcon name="i-lucide-x" class="w-8 h-8 text-red-500" />
      </div>
      <h1 class="text-2xl font-bold gradient-text mb-2">Verification failed</h1>
      <p class="text-red-500 dark:text-red-400 mb-4">{{ errorMessage }}</p>

      <div v-if="userEmail" class="mb-4">
        <div v-if="resendMessage" class="p-3 mb-3 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-700 dark:text-blue-300 text-sm">
          {{ resendMessage }}
        </div>
        <button
          @click="handleResend"
          :disabled="resendLoading"
          class="gradient-text font-medium text-sm disabled:opacity-50"
        >
          {{ resendLoading ? 'Sending...' : 'Send a new verification link' }}
        </button>
      </div>

      <p class="text-slate-500 dark:text-slate-400 mt-4">
        <NuxtLink to="/auth/login" class="gradient-text font-medium">
          Back to Sign in
        </NuxtLink>
      </p>
    </div>
  </div>
</template>
