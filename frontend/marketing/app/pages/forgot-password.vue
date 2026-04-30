<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Forgot password',
  description: 'Reset your Quizify account password'
})

const config = useRuntimeConfig()
const toast = useToast()

const fields = [{
  name: 'email',
  type: 'text' as const,
  label: 'Email',
  placeholder: 'you@example.com',
  required: true,
}]

const schema = z.object({
  email: z.email('Invalid email'),
})

type Schema = z.output<typeof schema>

const submitted = ref(false)

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  try {
    await $fetch<{ message: string }>(`${config.public.apiBase}/auth/forgot-password`, {
      method: 'POST',
      body: { email: payload.data.email },
    })
    submitted.value = true
  } catch (error: any) {
    const detail = error?.data?.detail || 'Failed to send reset link. Please try again.'
    toast.add({ title: 'Error', description: detail, color: 'error' })
  }
}
</script>

<template>
  <div v-if="submitted" class="max-w-md w-full mx-auto text-center py-12">
    <div class="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
      <span class="text-3xl">&#9993;</span>
    </div>
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Check your email</h1>
    <p class="text-gray-600 dark:text-gray-400 mb-2">
      If that email is registered, a password reset link has been sent.
    </p>
    <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
      The link expires in 1 hour.
    </p>
    <p class="mt-6">
      <ULink to="/login" class="text-primary font-medium">Back to Login</ULink>
    </p>
  </div>

  <UAuthForm
    v-else
    :fields="fields"
    :schema="schema"
    title="Forgot your password?"
    icon="i-lucide-key-round"
    :submit="{ label: 'Send reset link' }"
    @submit="onSubmit"
  >
    <template #description>
      Enter your email and we'll send you a link to choose a new password.
    </template>

    <template #footer>
      Remembered it?
      <ULink to="/login" class="text-primary font-medium">Back to sign in</ULink>.
    </template>
  </UAuthForm>
</template>
