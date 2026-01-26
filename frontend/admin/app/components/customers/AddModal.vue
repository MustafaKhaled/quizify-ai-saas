<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

const schema = z.object({
  name: z.string().min(2, 'Too short'),
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters').optional(),
  is_admin: z.boolean().optional()
})

const emit = defineEmits<{
  created: []
}>()

const open = ref(false)
const loading = ref(false)

type Schema = z.output<typeof schema>

const state = reactive<Partial<Schema>>({
  name: undefined,
  email: undefined,
  password: undefined,
  is_admin: false
})

const toast = useToast()
async function onSubmit(event: FormSubmitEvent<Schema>) {
  loading.value = true
  try {
    await $fetch('/api/users/create', {
      method: 'POST',
      body: {
        name: event.data.name,
        email: event.data.email,
        password: event.data.password,
        is_admin: event.data.is_admin || false
      }
    })

    toast.add({ 
      title: 'Success', 
      description: `New user ${event.data.name} added`, 
      color: 'success' 
    })
    
    emit('created')
    open.value = false
    // Reset form
    state.name = undefined
    state.email = undefined
    state.password = undefined
    state.is_admin = false
  } catch (err: any) {
    toast.add({
      title: 'Error',
      description: err?.data?.message || 'Failed to create user',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <UModal v-model:open="open" title="New customer" description="Add a new customer to the database">
    <UButton label="New customer" icon="i-lucide-plus" />

    <template #body>
      <UForm
        :schema="schema"
        :state="state"
        class="space-y-4"
        @submit="onSubmit"
      >
        <UFormField label="Name" placeholder="John Doe" name="name">
          <UInput v-model="state.name" class="w-full" />
        </UFormField>
        <UFormField label="Email" placeholder="john.doe@example.com" name="email">
          <UInput v-model="state.email" class="w-full" />
        </UFormField>
        <UFormField label="Password (optional)" placeholder="Leave empty for auto-generated" name="password">
          <UInput v-model="state.password" type="password" class="w-full" />
        </UFormField>
        <UFormField label="Admin" name="is_admin">
          <UCheckbox v-model="state.is_admin" />
        </UFormField>
        <div class="flex justify-end gap-2">
          <UButton
            label="Cancel"
            color="neutral"
            variant="subtle"
            @click="open = false"
          />
          <UButton
            label="Create"
            color="primary"
            variant="solid"
            type="submit"
            :loading="loading"
          />
        </div>
      </UForm>
    </template>
  </UModal>
</template>
