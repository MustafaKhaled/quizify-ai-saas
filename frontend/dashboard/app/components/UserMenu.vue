<script setup lang="ts">
import type { DropdownMenuItem } from '@nuxt/ui'

defineProps<{
  collapsed?: boolean
}>()

const config = useRuntimeConfig()

const user = ref({ name: '', email: '' })

onMounted(async () => {
  const token = localStorage.getItem('auth_token')
  if (!token) return
  try {
    const data = await $fetch<{ name: string, email: string }>(`${config.public.apiBase}/users/me`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = data
  } catch {}
})

function logout() {
  localStorage.removeItem('auth_token')
  const marketingUrl = config.public.marketingUrl || 'http://localhost:3000'
  window.location.href = `${marketingUrl}/login`
}

const items = computed<DropdownMenuItem[][]>(() => [[{
  type: 'label',
  label: user.value.name || 'Loading...',
  description: user.value.email
}], [{
  label: 'Log out',
  icon: 'i-lucide-log-out',
  color: 'error' as const,
  onSelect: logout
}]])
</script>

<template>
  <UDropdownMenu
    :items="items"
    :content="{ align: 'center', collisionPadding: 12 }"
    :ui="{ content: collapsed ? 'w-48' : 'w-(--reka-dropdown-menu-trigger-width)' }"
  >
    <UButton
      :label="collapsed ? undefined : (user.name || 'Loading...')"
      :trailing-icon="collapsed ? undefined : 'i-lucide-chevrons-up-down'"
      color="neutral"
      variant="ghost"
      block
      :square="collapsed"
      class="data-[state=open]:bg-elevated"
      :ui="{ trailingIcon: 'text-dimmed' }"
    >
      <template #leading>
        <UAvatar :alt="user.name" size="xs" />
      </template>
    </UButton>
  </UDropdownMenu>
</template>
