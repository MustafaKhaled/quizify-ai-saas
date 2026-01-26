<script setup lang="ts">
import type { User } from '~/types'

const props = withDefaults(defineProps<{
  count?: number
  selectedUsers?: User[]
}>(), {
  count: 0,
  selectedUsers: () => []
})

const emit = defineEmits<{
  deleted: []
}>()

const open = ref(false)
const toast = useToast()
const loading = ref(false)

async function onSubmit() {
  if (!props.selectedUsers || props.selectedUsers.length === 0) {
    return
  }

  loading.value = true
  try {
    // Delete each selected user
    for (const user of props.selectedUsers) {
      await $fetch('/api/users/delete', {
        method: 'POST',
        body: { email: user.email }
      })
    }

    toast.add({
      title: 'Success',
      description: `${props.count} user(s) deleted successfully`,
      color: 'success'
    })

    emit('deleted')
    open.value = false
  } catch (err: any) {
    toast.add({
      title: 'Error',
      description: err?.data?.message || 'Failed to delete users',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <UModal
    v-model:open="open"
    :title="`Delete ${count} customer${count > 1 ? 's' : ''}`"
    :description="`Are you sure, this action cannot be undone.`"
  >
    <slot />

    <template #body>
      <div class="flex justify-end gap-2">
        <UButton
          label="Cancel"
          color="neutral"
          variant="subtle"
          @click="open = false"
        />
        <UButton
          label="Delete"
          color="error"
          variant="solid"
          :loading="loading"
          @click="onSubmit"
        />
      </div>
    </template>
  </UModal>
</template>
