<script setup lang="ts">
definePageMeta({
  layout: 'auth'
})

const config = useRuntimeConfig()
const email = ref('')
const loading = ref(false)
const message = ref('')
const errorMessage = ref('')

const handleSubmit = async () => {
  errorMessage.value = ''
  message.value = ''
  loading.value = true
  try {
    const res = await $fetch<{ message: string }>(`${config.public.apiBase}/auth/forgot-password`, {
      method: 'POST',
      body: { email: email.value },
    })
    message.value = res.message || 'If that email is registered, a password reset link has been sent.'
  } catch (error: any) {
    errorMessage.value = error.data?.detail || error.message || 'Failed to send reset link. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-md w-full glass-card-elevated rounded-2xl p-8">
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold gradient-text mb-2">Forgot Password</h1>
      <p class="text-slate-500 dark:text-slate-400">
        Enter your email and we'll send you a link to reset your password.
      </p>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Email</label>
        <input
          v-model="email"
          type="email"
          placeholder="you@example.com"
          class="w-full px-4 py-2 glass-input rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 text-slate-900 dark:text-white"
          required
        />
      </div>

      <div v-if="message" class="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-700 dark:text-emerald-400 text-sm">
        {{ message }}
      </div>

      <div v-if="errorMessage" class="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-700 dark:text-red-400 text-sm">
        {{ errorMessage }}
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full py-2 btn-gradient rounded-xl disabled:opacity-50 font-medium"
      >
        {{ loading ? 'Sending...' : 'Send reset link' }}
      </button>
    </form>

    <p class="text-center text-slate-500 dark:text-slate-400 mt-4">
      Remembered it?
      <NuxtLink to="/auth/login" class="gradient-text font-medium">Back to sign in</NuxtLink>
    </p>
  </div>
</template>
