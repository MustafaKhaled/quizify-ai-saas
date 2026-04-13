<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Login',
  description: 'Login to your account to continue'
})

const config = useRuntimeConfig()

const fields = [{
  name: 'email',
  type: 'text' as const,
  label: 'Email',
  placeholder: 'Enter your email',
  required: true
}, {
  name: 'password',
  label: 'Password',
  type: 'password' as const,
  placeholder: 'Enter your password'
}, {
  name: 'remember',
  label: 'Remember me',
  type: 'checkbox' as const
}]

const providers = [{
  label: 'Google',
  icon: 'i-simple-icons-google',
  onClick: () => {
    navigateTo(`${config.public.apiBase}/auth/google/login`, { external: true })
  }
}]

const schema = z.object({
  email: z.email('Invalid email'),
  password: z.string().min(8, 'Must be at least 8 characters')
})

type Schema = z.output<typeof schema>

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  try {
    // 1. Create Form Data (FastAPI OAuth2 expects this format)
    const formData = new URLSearchParams()
    formData.append('username', payload.data.email) // OAuth2 MUST use the key 'username'
    formData.append('password', payload.data.password)

    // 2. Send the request
    const response = await $fetch<{ access_token: string }>(`${config.public.apiBase}/auth/login`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    })

    if (response.access_token) {
      const dashboardUrl = config.public.dashboardUrl || 'http://localhost:3000'
      window.location.replace(dashboardUrl)
    }

  } catch (error: any) {
    console.error('Login Failed:', error.data)
    const toast = useToast()
    const detail = error?.data?.detail || 'Invalid login credentials'
    toast.add({ title: 'Error', description: detail, color: 'error' })

    if (detail.toLowerCase().includes('verify your email')) {
      showResend.value = true
      loginEmail.value = payload.data.email
    }
  }
}

const showResend = ref(false)
const loginEmail = ref('')
const resendLoading = ref(false)

async function handleResendFromLogin() {
  resendLoading.value = true
  const toast = useToast()
  try {
    await $fetch(`${config.public.apiBase}/auth/resend-verification`, {
      method: 'POST',
      body: { email: loginEmail.value }
    })
    toast.add({ title: 'Sent', description: 'Verification email resent. Check your inbox.', color: 'success' })
  } catch {
    toast.add({ title: 'Error', description: 'Failed to resend. Please try again.', color: 'error' })
  } finally {
    resendLoading.value = false
  }
}
</script>

<template>
  <UAuthForm
    :fields="fields"
    :schema="schema"
    :providers="providers"
    title="Welcome back"
    icon="i-lucide-lock"
    @submit="onSubmit"
  >
    <template #description>
      Don't have an account? <ULink
        to="/signup"
        class="text-primary font-medium"
      >Sign up</ULink>.
    </template>

    <template #password-hint>
      <ULink
        to="/"
        class="text-primary font-medium"
        tabindex="-1"
      >Forgot password?</ULink>
    </template>

    <template #footer>
      <div v-if="showResend" class="mb-3 text-center">
        <button
          @click="handleResendFromLogin"
          :disabled="resendLoading"
          class="text-primary font-medium text-sm underline disabled:opacity-50"
        >
          {{ resendLoading ? 'Sending...' : 'Resend verification email' }}
        </button>
      </div>
      By signing in, you agree to our <ULink
        to="/"
        class="text-primary font-medium"
      >Terms of Service</ULink>.
    </template>
  </UAuthForm>
</template>
