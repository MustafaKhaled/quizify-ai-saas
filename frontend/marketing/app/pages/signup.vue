<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Sign up',
  description: 'Create an account to get started'
})

const config = useRuntimeConfig()

const toast = useToast()

const fields = [{
  name: 'name',
  type: 'text' as const,
  label: 'Name',
  placeholder: 'Enter your name'
}, {
  name: 'email',
  type: 'text' as const,
  label: 'Email',
  placeholder: 'Enter your email'
}, {
  name: 'password',
  label: 'Password',
  type: 'password' as const,
  placeholder: 'Enter your password'
}]

const providers = [{
  label: 'Google',
  icon: 'i-simple-icons-google',
  onClick: () => {
    navigateTo(`${config.public.apiBase}/auth/google/login`, {
      external: true
    })
  }
}]

const PRO_MONTHLY_PRICE_ID = 'price_1Slw1QGxfejNiimXsa3DfZ8R'
const PRO_YEARLY_PRICE_ID = 'price_1Slw1jGxfejNiimXMN0PHObK'

const route = useRoute()
const plan = route.query.plan as string | undefined
const priceId = plan === 'yearly' ? PRO_YEARLY_PRICE_ID
  : plan === 'monthly' ? PRO_MONTHLY_PRICE_ID
  : undefined

const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.email('Invalid email'),
  password: z.string().min(8, 'Must be at least 8 characters')
})

type Schema = z.output<typeof schema>

const verificationSent = ref(false)
const registeredEmail = ref('')

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  try {
    const response = await $fetch<{ access_token?: string, requires_verification?: boolean, checkout_url?: string, message?: string }>(`${config.public.apiBase}/auth/register`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: {
        name: payload.data.name,
        email: payload.data.email,
        password: payload.data.password,
        ...(priceId ? { price_id: priceId } : {})
      },
    })

    if (response.checkout_url) {
      // Paid plan: go straight to Stripe, webhook will verify the user on payment
      window.location.href = response.checkout_url
    } else if (response.requires_verification) {
      // Trial plan: require email verification
      registeredEmail.value = payload.data.email
      verificationSent.value = true
    } else if (response.access_token) {
      const dashboardUrl = config.public.dashboardUrl || 'http://localhost:3000'
      window.location.replace(dashboardUrl)
    }

  } catch (error: any) {
    const detail = error?.data?.detail || 'Failed to create account'
    toast.add({ title: 'Error', description: detail, color: 'error' })
  }
}

const resendLoading = ref(false)

async function handleResend() {
  resendLoading.value = true
  try {
    await $fetch(`${config.public.apiBase}/auth/resend-verification`, {
      method: 'POST',
      body: { email: registeredEmail.value }
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
  <!-- Verification Sent Screen -->
  <div v-if="verificationSent" class="max-w-md w-full mx-auto text-center py-12">
    <div class="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
      <span class="text-3xl">&#9993;</span>
    </div>
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Check your email</h1>
    <p class="text-gray-600 dark:text-gray-400 mb-2">
      We sent a verification link to <strong class="text-gray-900 dark:text-white">{{ registeredEmail }}</strong>
    </p>
    <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
      Click the link in the email to activate your account. The link expires in 24 hours.
    </p>
    <button
      @click="handleResend"
      :disabled="resendLoading"
      class="text-primary font-medium text-sm disabled:opacity-50"
    >
      {{ resendLoading ? 'Sending...' : "Didn't receive it? Resend email" }}
    </button>
    <p class="mt-6">
      <ULink to="/login" class="text-primary font-medium">Back to Login</ULink>
    </p>
  </div>

  <!-- Registration Form -->
  <UAuthForm
    v-else
    :fields="fields"
    :schema="schema"
    :providers="providers"
    title="Create an account"
    :submit="{ label: 'Create account' }"
    @submit="onSubmit"
  >
    <template #description>
      Already have an account? <ULink
        to="/login"
        class="text-primary font-medium"
      >Login</ULink>.
    </template>

    <template #footer>
      By signing up, you agree to our <ULink
        to="/"
        class="text-primary font-medium"
      >Terms of Service</ULink>.
    </template>
  </UAuthForm>
</template>
