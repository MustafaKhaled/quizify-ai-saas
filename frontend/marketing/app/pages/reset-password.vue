<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Reset password',
  description: 'Choose a new password for your Quizify account'
})

const config = useRuntimeConfig()
const route = useRoute()
const toast = useToast()

const token = computed(() => (route.query.token as string) || '')

const fields = [{
  name: 'password',
  type: 'password' as const,
  label: 'New password',
  placeholder: 'At least 8 characters',
  required: true,
}, {
  name: 'confirm',
  type: 'password' as const,
  label: 'Confirm new password',
  placeholder: 'Repeat your new password',
  required: true,
}]

const schema = z.object({
  password: z.string().min(8, 'Must be at least 8 characters').max(72, 'Too long'),
  confirm: z.string(),
}).refine((d) => d.password === d.confirm, {
  message: 'Passwords do not match',
  path: ['confirm'],
})

type Schema = z.output<typeof schema>

const success = ref(false)

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  if (!token.value) {
    toast.add({ title: 'Error', description: 'Reset link is missing or invalid.', color: 'error' })
    return
  }
  try {
    await $fetch(`${config.public.apiBase}/auth/reset-password`, {
      method: 'POST',
      body: { token: token.value, new_password: payload.data.password },
    })
    success.value = true
    setTimeout(() => navigateTo('/login'), 1800)
  } catch (error: any) {
    const detail = error?.data?.detail || 'Failed to reset password.'
    toast.add({ title: 'Error', description: detail, color: 'error' })
  }
}
</script>

<template>
  <div v-if="!token" class="max-w-md w-full mx-auto text-center py-12">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Invalid reset link</h1>
    <p class="text-gray-600 dark:text-gray-400 mb-6">
      This reset link is missing a token. Request a new one below.
    </p>
    <ULink to="/forgot-password" class="text-primary font-medium">Send a new reset link</ULink>
  </div>

  <div v-else-if="success" class="max-w-md w-full mx-auto text-center py-12">
    <div class="w-16 h-16 bg-emerald-100 dark:bg-emerald-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
      <UIcon name="i-lucide-check" class="w-8 h-8 text-emerald-600 dark:text-emerald-400" />
    </div>
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Password updated</h1>
    <p class="text-gray-600 dark:text-gray-400 mb-6">
      Redirecting you to sign in…
    </p>
  </div>

  <UAuthForm
    v-else
    :fields="fields"
    :schema="schema"
    title="Choose a new password"
    icon="i-lucide-lock"
    :submit="{ label: 'Reset password' }"
    @submit="onSubmit"
  >
    <template #description>
      Pick a strong password you don't use anywhere else.
    </template>

    <template #footer>
      <ULink to="/login" class="text-primary font-medium">Back to sign in</ULink>
    </template>
  </UAuthForm>
</template>
