<script setup lang="ts">
definePageMeta({
  layout: 'auth'
})

const config = useRuntimeConfig()
const router = useRouter()
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')
const showResend = ref(false)
const resendMessage = ref('')
const resendLoading = ref(false)

const handleLogin = async () => {
  errorMessage.value = ''
  showResend.value = false
  loading.value = true

  try {
    const formData = new FormData()
    formData.append('username', email.value)
    formData.append('password', password.value)

    const response = await $fetch(`${config.public.apiBase}/auth/login`, {
      method: 'POST',
      body: formData,
      credentials: 'include'
    }) as any

    if (response.access_token) {
      localStorage.setItem('auth_token', response.access_token)
      localStorage.setItem('user_email', email.value)
      router.push('/dashboard')
    }
  } catch (error: any) {
    const detail = error.data?.detail || error.message || 'Login failed'
    errorMessage.value = detail
    if (detail.toLowerCase().includes('verify your email')) {
      showResend.value = true
    }
  } finally {
    loading.value = false
  }
}

const handleResend = async () => {
  resendLoading.value = true
  resendMessage.value = ''
  try {
    await $fetch(`${config.public.apiBase}/auth/resend-verification`, {
      method: 'POST',
      body: { email: email.value }
    })
    resendMessage.value = 'Verification email sent! Check your inbox.'
  } catch {
    resendMessage.value = 'Failed to resend. Please try again.'
  } finally {
    resendLoading.value = false
  }
}
</script>

<template>
  <div class="max-w-md w-full glass-card-elevated rounded-2xl p-8">
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold gradient-text mb-2">Welcome Back</h1>
      <p class="text-slate-500 dark:text-slate-400">Sign in to your Quizify AI account</p>
    </div>

    <form @submit.prevent="handleLogin" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
          Email
        </label>
        <input
          v-model="email"
          type="email"
          placeholder="you@example.com"
          class="w-full px-4 py-2 glass-input rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 text-slate-900 dark:text-white"
          required
        />
      </div>

      <div>
        <div class="flex items-center justify-between mb-1">
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">
            Password
          </label>
          <NuxtLink to="/auth/forgot-password" class="text-xs gradient-text font-medium">
            Forgot password?
          </NuxtLink>
        </div>
        <input
          v-model="password"
          type="password"
          placeholder="••••••••"
          class="w-full px-4 py-2 glass-input rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 text-slate-900 dark:text-white"
          required
        />
      </div>

      <div v-if="errorMessage" class="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-700 dark:text-red-400 text-sm">
        {{ errorMessage }}
        <div v-if="showResend" class="mt-2">
          <button
            @click="handleResend"
            :disabled="resendLoading"
            class="gradient-text font-medium text-sm underline disabled:opacity-50"
          >
            {{ resendLoading ? 'Sending...' : 'Resend verification email' }}
          </button>
          <p v-if="resendMessage" class="mt-1 text-blue-600 dark:text-blue-400 text-xs">{{ resendMessage }}</p>
        </div>
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full py-2 btn-gradient rounded-xl disabled:opacity-50 font-medium"
      >
        {{ loading ? 'Signing in...' : 'Sign In' }}
      </button>
    </form>

    <p class="text-center text-slate-500 dark:text-slate-400 mt-4">
      Don't have an account?
      <NuxtLink to="/auth/register" class="gradient-text font-medium">
        Create one
      </NuxtLink>
    </p>
  </div>
</template>
