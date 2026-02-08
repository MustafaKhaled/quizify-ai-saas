<script setup lang="ts">
definePageMeta({
  layout: 'auth'
})

const router = useRouter()
const { $fetch } = useNuxtApp()
const email = ref('')
const password = ref('')
const name = ref('')
const loading = ref(false)
const errorMessage = ref('')

const handleRegister = async () => {
  errorMessage.value = ''
  loading.value = true

  try {
    const response = await $fetch('/api/auth/register', {
      method: 'POST',
      body: {
        email: email.value,
        password: password.value,
        name: name.value
      }
    })

    if (response.access_token) {
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
</script>

<template>
  <div class="max-w-md w-full">
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Create Account</h1>
      <p class="text-gray-600 dark:text-gray-400">Join Quizify AI to create amazing quizzes</p>
    </div>

    <form @submit.prevent="handleRegister" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Full Name
        </label>
        <input
          v-model="name"
          type="text"
          placeholder="Your name"
          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Email
        </label>
        <input
          v-model="email"
          type="email"
          placeholder="you@example.com"
          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Password
        </label>
        <input
          v-model="password"
          type="password"
          placeholder="••••••••"
          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white"
          required
        />
      </div>

      <div v-if="errorMessage" class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-400 text-sm">
        {{ errorMessage }}
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium rounded-lg transition-colors"
      >
        {{ loading ? 'Creating Account...' : 'Create Account' }}
      </button>
    </form>

    <p class="text-center text-gray-600 dark:text-gray-400 mt-4">
      Already have an account?
      <NuxtLink to="/auth/login" class="text-blue-600 hover:text-blue-700 dark:text-blue-400 font-medium">
        Sign in
      </NuxtLink>
    </p>
  </div>
</template>
