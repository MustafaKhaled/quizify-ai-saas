<template>
    <div class="flex h-screen items-center justify-center bg-gray-50 dark:bg-gray-900">
      <UCard class="w-full max-w-md">
        <UAuthForm
          title="Admin Login"
          description="Access your Exam Intelligence Dashboard"
          :fields="[
            { name: 'email', type: 'email', label: 'Email', placeholder: 'admin@quizify.ai' },
            { name: 'password', type: 'password', label: 'Password' }
          ]"
          @submit="onSubmit"
        />
      </UCard>
    </div>
  </template>
  
<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

  definePageMeta({
    layout: false // This disables the dashboard sidebar/header
  })
  
const { fetch } = useUserSession()
const config = useRuntimeConfig()

interface Schema {
  email?: string
  password?: string
}

async function onSubmit(payload: FormSubmitEvent<Schema>) {
try {
// 1. Create Form Data (FastAPI OAuth2 expects this format)
const formData = new URLSearchParams()
formData.append('username', payload.data.email) // OAuth2 MUST use the key 'username'
formData.append('password', payload.data.password)

// 2. Send the request
const response = await $fetch(`${config.public.apiBase}/auth/login`, {
    method: 'POST',
    headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
})

const toast = useToast()
toast.add({ title: 'Success', description: 'Login Success', color: 'green' })

console.log('Login Success:', response)

await navigateTo('/dashboard')

} catch (error: any) {
console.error('Login Failed:', error.data)
const toast = useToast()
toast.add({ title: 'Error', description: 'Invalid login credentials', color: 'red' })
}
}
  </script>