<script setup lang="ts">
defineProps<{
  collapsed?: boolean
}>()

const config = useRuntimeConfig()
const user = ref({ name: '', email: '' })

onMounted(async () => {
  try {
    const data = await $fetch<{ name: string, email: string }>(`${config.public.apiBase}/users/me`, {
      credentials: 'include'
    })
    user.value = data
  } catch {}
})

async function logout() {
  try {
    await $fetch(`${config.public.apiBase}/auth/logout`, {
      method: 'POST',
      credentials: 'include'
    })
  } catch {}
  const marketingUrl = config.public.marketingUrl || 'http://localhost:3000'
  window.location.href = `${marketingUrl}/login`
}
</script>

<template>
  <div class="flex items-center gap-2 px-1 py-1 w-full">
    <UAvatar :alt="user.name" size="xs" class="shrink-0" />

    <div v-if="!collapsed" class="flex-1 min-w-0">
      <p class="text-sm font-medium text-highlighted truncate">{{ user.name }}</p>
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
