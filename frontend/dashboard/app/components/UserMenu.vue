<script setup lang="ts">
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

async function logout() {
  const token = localStorage.getItem('auth_token')
  if (token) {
    try {
      await $fetch(`${config.public.apiBase}/auth/logout`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      })
    } catch {}
    localStorage.removeItem('auth_token')
  }
  const marketingUrl = config.public.marketingUrl || 'http://localhost:3000'
  window.location.href = `${marketingUrl}/login`
}
</script>

<template>
  <div class="flex items-center gap-2 px-1 py-1 w-full">
    <UAvatar :alt="user.name" size="xs" class="shrink-0" />

    <div v-if="!collapsed" class="flex-1 min-w-0">
      <p class="text-sm font-medium text-highlighted truncate">{{ user.name || 'Loading...' }}</p>
      <p class="text-xs text-dimmed truncate">{{ user.email }}</p>
    </div>

    <UTooltip :text="'Log out'" :delay="300">
      <UButton
        icon="i-lucide-log-out"
        color="error"
        variant="ghost"
        size="xs"
        square
        class="shrink-0"
        @click="logout"
      />
    </UTooltip>
  </div>
</template>
