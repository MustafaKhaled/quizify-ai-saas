<script setup lang="ts">
defineProps<{
  collapsed?: boolean
  compact?: boolean
}>()

const config = useRuntimeConfig()
const user = ref({ name: '', email: '', has_password: true })

const showChangePassword = ref(false)
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const changeLoading = ref(false)
const changeError = ref('')
const changeSuccess = ref('')

onMounted(async () => {
  try {
    const data = await $fetch<{ name: string, email: string, has_password?: boolean }>(`${config.public.apiBase}/users/me`, {
      credentials: 'include'
    })
    user.value = {
      name: data.name,
      email: data.email,
      has_password: data.has_password ?? true,
    }
  } catch {}
})

function openChangePassword() {
  changeError.value = ''
  changeSuccess.value = ''
  currentPassword.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
  showChangePassword.value = true
}

async function submitChangePassword() {
  changeError.value = ''
  changeSuccess.value = ''
  if (newPassword.value.length < 8) {
    changeError.value = 'New password must be at least 8 characters.'
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    changeError.value = 'New passwords do not match.'
    return
  }
  changeLoading.value = true
  try {
    await $fetch(`${config.public.apiBase}/auth/change-password`, {
      method: 'POST',
      credentials: 'include',
      body: {
        current_password: currentPassword.value,
        new_password: newPassword.value,
      },
    })
    changeSuccess.value = 'Password changed successfully.'
    setTimeout(() => {
      showChangePassword.value = false
    }, 1200)
  } catch (e: any) {
    changeError.value = e.data?.detail || e.message || 'Failed to change password.'
  } finally {
    changeLoading.value = false
  }
}

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

const items = computed(() => {
  const header: any[] = [{
    label: user.value.name || user.value.email,
    type: 'label',
  }]
  const actions: any[] = []
  if (user.value.has_password) {
    actions.push({
      label: 'Change password',
      icon: 'i-lucide-key',
      onSelect: () => openChangePassword(),
    })
  }
  actions.push({
    label: 'Log out',
    icon: 'i-lucide-log-out',
    color: 'error',
    onSelect: () => logout(),
  })
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

    <!-- Change password modal -->
    <Teleport to="body">
      <div
        v-if="showChangePassword"
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
        @click.self="showChangePassword = false"
      >
        <div class="glass-card-elevated rounded-2xl shadow-xl w-full max-w-md p-6">
          <h2 class="text-xl font-bold gradient-text mb-1">Change Password</h2>
          <p class="text-sm text-slate-500 dark:text-slate-400 mb-5">
            You'll stay signed in here, but other devices will be signed out.
          </p>
          <form @submit.prevent="submitChangePassword" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Current Password</label>
              <input
                v-model="currentPassword"
                type="password"
                class="w-full px-3 py-2 glass-input rounded-xl text-sm text-slate-900 dark:text-white"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">New Password</label>
              <input
                v-model="newPassword"
                type="password"
                minlength="8"
                maxlength="72"
                placeholder="At least 8 characters"
                class="w-full px-3 py-2 glass-input rounded-xl text-sm text-slate-900 dark:text-white"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Confirm New Password</label>
              <input
                v-model="confirmPassword"
                type="password"
                minlength="8"
                maxlength="72"
                class="w-full px-3 py-2 glass-input rounded-xl text-sm text-slate-900 dark:text-white"
                required
              />
            </div>

            <div v-if="changeSuccess" class="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-700 dark:text-emerald-400 text-sm">
              {{ changeSuccess }}
            </div>
            <div v-if="changeError" class="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-700 dark:text-red-400 text-sm">
              {{ changeError }}
            </div>

            <div class="flex gap-3 pt-2">
              <button
                type="button"
                @click="showChangePassword = false"
                class="flex-1 py-2 border border-gray-300 dark:border-gray-600 rounded-xl text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="changeLoading"
                class="flex-1 py-2 btn-gradient rounded-xl text-sm font-medium disabled:opacity-50"
              >
                {{ changeLoading ? 'Saving...' : 'Change password' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>
