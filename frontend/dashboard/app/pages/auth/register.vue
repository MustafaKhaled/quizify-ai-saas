<script setup lang="ts">
definePageMeta({
  layout: 'auth'
})

const config = useRuntimeConfig()
const router = useRouter()
const email = ref('')
const password = ref('')
const name = ref('')
const loading = ref(false)
const errorMessage = ref('')
const verificationSent = ref(false)

const handleRegister = async () => {
  errorMessage.value = ''
  loading.value = true

  try {
    const response = await $fetch(`${config.public.apiBase}/auth/register`, {
      method: 'POST',
      body: {
        email: email.value,
        password: password.value,
        name: name.value
      }
    }) as any

    if (response.requires_verification) {
      verificationSent.value = true
    } else if (response.access_token) {
      localStorage.setItem('auth_token', response.access_token)
      localStorage.setItem('user_email', email.value)
      router.push('/dashboard')
    }
  } catch (error: any) {
    errorMessage.value = error.data?.detail || 'Registration failed'
  } finally {
    loading.value = false
  }
}

const resendLoading = ref(false)
const resendMessage = ref('')

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
    <!-- Verification Sent Screen -->
    <div v-if="verificationSent" class="text-center">
      <div class="mb-6">
        <div class="w-16 h-16 bg-blue-500/15 backdrop-blur-sm rounded-full flex items-center justify-center mx-auto mb-4">
          <UIcon name="i-lucide-mail" class="w-8 h-8 text-blue-500" />
        </div>
        <h1 class="text-2xl font-bold gradient-text mb-2">Check your email</h1>
        <p class="text-slate-500 dark:text-slate-400">
          We sent a verification link to <strong class="text-slate-900 dark:text-white">{{ email }}</strong>
        </p>
      </div>

      <p class="text-sm text-slate-500 dark:text-slate-400 mb-4">
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

      <p class="text-center text-slate-500 dark:text-slate-400 mt-6">
        <NuxtLink to="/auth/login" class="gradient-text font-medium">
          Back to Sign in
        </NuxtLink>
      </p>
    </div>

    <!-- Registration Form -->
    <div v-else>
      <div class="text-center mb-6">
        <h1 class="text-2xl font-bold gradient-text mb-2">Create Account</h1>
        <p class="text-slate-500 dark:text-slate-400">Join Quizify AI to create amazing quizzes</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
            Full Name
          </label>
          <input
            v-model="name"
            type="text"
            placeholder="Your name"
            class="w-full px-4 py-2 glass-input rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 text-slate-900 dark:text-white"
            required
          />
        </div>

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
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
            Password
          </label>
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
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2 btn-gradient rounded-xl disabled:opacity-50 font-medium"
        >
          {{ loading ? 'Creating Account...' : 'Create Account' }}
        </button>
      </form>

      <p class="text-center text-slate-500 dark:text-slate-400 mt-4">
        Already have an account?
        <NuxtLink to="/auth/login" class="gradient-text font-medium">
          Sign in
        </NuxtLink>
      </p>
    </div>
  </div>
</template>
