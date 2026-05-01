<script setup lang="ts">
defineProps<{
  collapsed?: boolean
  compact?: boolean
}>()

const config = useRuntimeConfig()
const user = ref({ name: '', email: '' })

onMounted(async () => {
  try {
    const data = await $fetch<{ name: string, email: string }>(`${config.public.apiBase}/users/me`, {
      credentials: 'include'
    })
    user.value = { name: data.name, email: data.email }
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

function goToProfile() {
  navigateTo('/profile')
}

const items = computed(() => {
  const header: any[] = [{
    label: user.value.name || user.value.email,
    type: 'label',
  }]
  const actions: any[] = [
    {
      label: 'Profile',
      icon: 'i-lucide-user',
      onSelect: () => goToProfile(),
    },
    {
      label: 'Log out',
      icon: 'i-lucide-log-out',
      color: 'error',
      onSelect: () => logout(),
    },
  ]
  return [header, actions]
})
</script>

<template>
  <div :class="compact ? 'flex items-center' : 'flex items-center gap-2 px-1 py-1 w-full'">
    <UDropdownMenu :items="items" :content="{ align: 'end' }">
      <button
        type="button"
        :class="compact
          ? 'flex items-center gap-2 px-2 py-1 rounded-xl hover:bg-white/5 transition-colors'
          : 'flex items-center gap-2 flex-1 min-w-0 px-1 py-1 rounded-xl hover:bg-white/5 transition-colors'"
        :aria-label="user.name || user.email"
      >
        <UAvatar :alt="user.name" size="xs" class="shrink-0" />

        <div v-if="!collapsed && !compact" class="flex-1 min-w-0 text-left">
          <p class="text-sm font-medium text-highlighted truncate">{{ user.name }}</p>
          <p class="text-xs text-dimmed truncate">{{ user.email }}</p>
        </div>

        <UIcon
          v-if="!collapsed"
          name="i-lucide-chevron-down"
          class="w-4 h-4 text-slate-500 dark:text-slate-400 shrink-0"
        />
      </button>
    </UDropdownMenu>
  </div>
</template>
