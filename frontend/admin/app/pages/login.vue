<!-- frontend/admin/app/pages/login.vue -->
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
          @submit.prevent="onSubmit"
        />
      </UCard>
    </div>
  </template>
  
<script setup lang="ts">
const { fetch } = useUserSession() // Hook to refresh the session state
const toast = useToast()

async function onSubmit(payload: any) {
  try {
    // 1. Call your LOCAL Nuxt server route (proxy)
    await $fetch('/api/auth/login', {
      method: 'POST',
      body: {
        email: payload.data.email,
        password: payload.data.password
      }
    })

    // 2. IMPORTANT: Manually refresh the session 
    // This makes 'loggedIn.value' change to true in the UI
    await fetch()
    
    toast.add({ title: 'Welcome back!', color: 'green' })
    
    // 3. Redirect - the middleware will now let you through
    await navigateTo('/' , { external: true })
    
  } catch (err: any) {
    toast.add({ 
      title: 'Login Failed', 
      description: 'Check your credentials or database connection.', 
      color: 'red' 
    })
  }
}
  </script>