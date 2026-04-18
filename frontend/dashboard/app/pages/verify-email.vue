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
  <div class="max-w-md w-full mx-auto text-center">
    <!-- Loading -->
    <div v-if="status === 'loading'">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
      <h1 class="text-xl font-bold text-gray-900 dark:text-white">Verifying your email...</h1>
    </div>

    <!-- Pending: user hasn't verified yet -->
    <div v-else-if="status === 'pending'">
      <div class="w-16 h-16 bg-yellow-100 dark:bg-yellow-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
        <span class="text-3xl">&#9993;</span>
      </div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Verify your email</h1>
      <p v-if="userEmail" class="text-gray-600 dark:text-gray-400 mb-2">
        We sent a verification link to <strong class="text-gray-900 dark:text-white">{{ userEmail }}</strong>
      </p>
      <p v-else class="text-gray-600 dark:text-gray-400 mb-2">
        Please check your inbox for the verification link.
      </p>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
        Click the link in the email to activate your account. The link expires in 24 hours.
      </p>

      <div v-if="resendMessage" class="p-3 mb-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg text-blue-700 dark:text-blue-300 text-sm">
        {{ resendMessage }}
      </div>

      <button
        @click="handleResend"
        :disabled="resendLoading"
        class="text-blue-600 hover:text-blue-700 dark:text-blue-400 font-medium text-sm disabled:opacity-50"
      >
        {{ resendLoading ? 'Sending...' : "Didn't receive it? Resend email" }}
      </button>

      <p class="text-gray-600 dark:text-gray-400 mt-6">
        <NuxtLink to="/auth/login" class="text-blue-600 hover:text-blue-700 dark:text-blue-400 font-medium">
          Back to Sign in
        </NuxtLink>
      </p>
    </div>

    <!-- Success -->
    <div v-else-if="status === 'success'">
      <div class="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
        <span class="text-3xl text-green-600">&#10003;</span>
      </div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Email verified!</h1>
      <p class="text-gray-600 dark:text-gray-400 mb-4">Your account is now active. Redirecting to dashboard...</p>
    </div>

    <!-- Error -->
    <div v-else>
      <div class="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
        <span class="text-3xl text-red-600">&#10007;</span>
      </div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Verification failed</h1>
      <p class="text-red-600 dark:text-red-400 mb-4">{{ errorMessage }}</p>

      <div v-if="userEmail" class="mb-4">
        <div v-if="resendMessage" class="p-3 mb-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg text-blue-700 dark:text-blue-300 text-sm">
          {{ resendMessage }}
        </div>
        <button
          @click="handleResend"
          :disabled="resendLoading"
          class="text-blue-600 hover:text-blue-700 dark:text-blue-400 font-medium text-sm disabled:opacity-50"
        >
          {{ resendLoading ? 'Sending...' : 'Send a new verification link' }}
        </button>
      </div>

      <p class="text-gray-600 dark:text-gray-400 mt-4">
        <NuxtLink to="/auth/login" class="text-blue-600 hover:text-blue-700 dark:text-blue-400 font-medium">
          Back to Sign in
        </NuxtLink>
      </p>
    </div>
  </div>
</template>
