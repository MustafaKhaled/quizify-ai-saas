<script setup lang="ts">
definePageMeta({
  layout: 'auth'
})

const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()

const token = computed(() => (route.query.token as string) || '')

const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const handleSubmit = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!token.value) {
    errorMessage.value = 'Reset link is missing or invalid.'
    return
  }
  if (newPassword.value.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters.'
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match.'
    return
  }

  loading.value = true
  try {
    await $fetch(`${config.public.apiBase}/auth/reset-password`, {
      method: 'POST',
      body: { token: token.value, new_password: newPassword.value },
    })
    successMessage.value = 'Password reset successfully. Redirecting to sign in...'
    setTimeout(() => router.push('/auth/login'), 1500)
  } catch (error: any) {
    errorMessage.value = error.data?.detail || error.message || 'Failed to reset password.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-md w-full glass-card-elevated rounded-2xl p-8">
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold gradient-text mb-2">Reset Password</h1>
      <p class="text-slate-500 dark:text-slate-400">Choose a new password for your account.</p>
    </div>

    <div v-if="!token" class="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-700 dark:text-red-400 text-sm mb-4">
      This reset link is missing a token. Request a new one from
      <NuxtLink to="/auth/forgot-password" class="underline gradient-text font-medium">forgot password</NuxtLink>.
    </div>

    <form v-else @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">New Password</label>
        <input
          v-model="newPassword"
          type="password"
          placeholder="At least 8 characters"
          minlength="8"
          maxlength="72"
          class="w-full px-4 py-2 glass-input rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 text-slate-900 dark:text-white"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Confirm Password</label>
        <input
          v-model="confirmPassword"
          type="password"
          placeholder="Repeat new password"
          minlength="8"
          maxlength="72"
          class="w-full px-4 py-2 glass-input rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 text-slate-900 dark:text-white"
          required
        />
      </div>

      <div v-if="successMessage" class="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-700 dark:text-emerald-400 text-sm">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-700 dark:text-red-400 text-sm">
        {{ errorMessage }}
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full py-2 btn-gradient rounded-xl disabled:opacity-50 font-medium"
      >
        {{ loading ? 'Resetting...' : 'Reset password' }}
      </button>
    </form>

    <p class="text-center text-slate-500 dark:text-slate-400 mt-4">
      <NuxtLink to="/auth/login" class="gradient-text font-medium">Back to sign in</NuxtLink>
    </p>
  </div>
</template>
