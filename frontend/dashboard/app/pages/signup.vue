<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Sign Up',
  description: 'Create your Quizify account'
})

const schema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters')
})

type Schema = z.output<typeof schema>

const state = reactive<Partial<Schema>>({
  name: undefined,
  email: undefined,
  password: undefined
})

const toast = useToast()
const loading = ref(false)
const config = useRuntimeConfig()

async function onSubmit(event: FormSubmitEvent<Schema>) {
  loading.value = true
  try {
    const response = await $fetch(`${config.public.apiBase}/auth/register`, {
      method: 'POST',
      body: {
        email: event.data.email,
        password: event.data.password,
        name: event.data.name
      }
    })

    // Auto-login after registration
    await $fetch('/api/auth/login', {
      method: 'POST',
      body: {
        email: event.data.email,
        password: event.data.password
      },
      credentials: 'include'
    })

    const { fetch } = useUserSession()
    await fetch()

    toast.add({ title: 'Account created!', color: 'success' })
    await navigateTo('/')
  } catch (err: any) {
    toast.add({
      title: 'Sign Up Failed',
      description: err?.response?._data?.detail || err?.data?.message || 'Failed to create account',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <UCard>
    <UAuthForm
      title="Create Account"
      description="Sign up to start creating quizzes"
      :fields="[
        { name: 'name', type: 'text', label: 'Name', placeholder: 'Your name' },
        { name: 'email', type: 'email', label: 'Email', placeholder: 'your@email.com' },
        { name: 'password', type: 'password', label: 'Password' }
      ]"
      :schema="schema"
      :state="state"
      @submit="onSubmit"
    >
      <template #description>
        Already have an account? <ULink to="/login" class="text-primary font-medium">Login</ULink>.
      </template>
    </UAuthForm>
  </UCard>
</template>
