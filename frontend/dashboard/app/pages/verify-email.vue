<script setup lang="ts">
definePageMeta({
  layout: 'auth'
})

const config = useRuntimeConfig()
const route = useRoute()
const status = ref<'loading' | 'success' | 'error'>('loading')
const errorMessage = ref('')

onMounted(async () => {
  const token = route.query.token as string | undefined

  if (!token) {
    status.value = 'error'
    errorMessage.value = 'Missing verification token.'
    return
  }

  try {
    // The backend verify-email endpoint sets the auth cookie and redirects,
    // but since we're calling it from the frontend we handle the redirect ourselves.
    const response = await fetch(`${config.public.apiBase}/auth/verify-email?token=${encodeURIComponent(token)}`, {
      credentials: 'include',
      redirect: 'manual' // Don't follow redirect — we handle it
    })

    if (response.status === 302 || response.ok) {
      status.value = 'success'
      // Redirect to dashboard after a short delay
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
      <NuxtLink to="/auth/login" class="text-blue-600 hover:text-blue-700 dark:text-blue-400 font-medium">
        Back to Sign in
      </NuxtLink>
    </div>
  </div>
</template>
