<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

definePageMeta({
  title: 'Account Settings',
  description: 'Manage your account settings'
})

const { user, fetch } = useUserSession()
const toast = useToast()
const config = useRuntimeConfig()

const schema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters').optional(),
  password: z.string().min(8, 'Password must be at least 8 characters').optional()
})

type Schema = z.output<typeof schema>

const state = reactive<Partial<Schema>>({
  name: user.value?.name || '',
  password: undefined
})

const loading = ref(false)

async function onSubmit(event: FormSubmitEvent<Schema>) {
  loading.value = true
  try {
    const session = await useUserSession()
    
    await $fetch(`${config.public.apiBase}/users/me`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${session.token.value}`
      },
      body: {
        name: event.data.name,
        password: event.data.password
      }
    })

    toast.add({
      title: 'Success',
      description: 'Profile updated successfully',
      color: 'success'
    })

    await fetch() // Refresh user session
  } catch (err: any) {
    toast.add({
      title: 'Error',
      description: err?.data?.message || 'Failed to update profile',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto space-y-6">
    <!-- Account Info -->
    <UCard>
      <template #header>
        <h2 class="text-xl font-semibold">Account Information</h2>
      </template>

      <div class="space-y-4">
        <div>
          <label class="text-sm font-medium text-gray-500">Email</label>
          <p class="mt-1">{{ user?.email }}</p>
        </div>
        <div>
          <label class="text-sm font-medium text-gray-500">Subscription</label>
          <p class="mt-1">{{ user?.subscription?.label || 'Trial' }}</p>
        </div>
      </div>
    </UCard>

    <!-- Update Profile -->
    <UCard>
      <template #header>
        <h2 class="text-xl font-semibold">Update Profile</h2>
      </template>

      <UForm
        :schema="schema"
        :state="state"
        class="space-y-4"
        @submit="onSubmit"
      >
        <UFormField label="Name" name="name">
          <UInput v-model="state.name" placeholder="Your name" />
        </UFormField>

        <UFormField label="New Password (leave empty to keep current)" name="password">
          <UInput v-model="state.password" type="password" placeholder="Enter new password" />
        </UFormField>

        <div class="flex justify-end">
          <UButton
            type="submit"
            :loading="loading"
          >
            Update Profile
          </UButton>
        </div>
      </UForm>
    </UCard>
  </div>
</template>
