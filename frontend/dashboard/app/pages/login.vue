<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Login',
  description: 'Login to your Quizify account'
})

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(1, 'Password is required')
})

type Schema = z.output<typeof schema>

const state = reactive<Partial<Schema>>({
  email: undefined,
  password: undefined
})

const toast = useToast()
const { fetch } = useUserSession()

async function onSubmit(event: FormSubmitEvent<Schema>) {
  try {
    await $fetch('/api/auth/login', {
      method: 'POST',
      body: {
        email: event.data.email,
        password: event.data.password
      },
      credentials: 'include'
    })

    await nextTick()
    await fetch()

    toast.add({ title: 'Welcome back!', color: 'success' })
    await navigateTo('/')
  } catch (err: any) {
    toast.add({
      title: 'Login Failed',
      description: err?.data?.message || 'Invalid credentials',
      color: 'error'
    })
  }
}
</script>

<template>
  <UCard>
    <UAuthForm
      title="Welcome to Quizify"
      description="Login to create and take quizzes"
      :fields="[
        { name: 'email', type: 'email', label: 'Email', placeholder: 'your@email.com' },
        { name: 'password', type: 'password', label: 'Password' }
      ]"
      :schema="schema"
      :state="state"
      @submit="onSubmit"
    >
      <template #description>
        Don't have an account? <ULink to="/signup" class="text-primary font-medium">Sign up</ULink>.
      </template>
    </UAuthForm>
  </UCard>
</template>
    </UAuthForm>
  </UCard>
</template>
