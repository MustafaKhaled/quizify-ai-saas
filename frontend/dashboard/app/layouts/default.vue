<script setup lang="ts">
const route = useRoute()
const { user, clear } = useUserSession()

const navigation = [
  {
    label: 'Dashboard',
    icon: 'i-lucide-layout-dashboard',
    to: '/'
  },
  {
    label: 'My Quizzes',
    icon: 'i-lucide-file-question',
    to: '/quizzes'
  },
  {
    label: 'Upload PDF',
    icon: 'i-lucide-upload',
    to: '/upload'
  },
  {
    label: 'Account',
    icon: 'i-lucide-user',
    to: '/account'
  }
]
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <UContainer>
      <div class="flex gap-4 py-4">
        <!-- Sidebar -->
        <aside class="hidden md:block w-64 shrink-0">
          <div class="sticky top-4 space-y-4">
            <div class="flex items-center gap-2 mb-6">
              <UIcon name="i-lucide-brain-circuit" class="w-8 h-8 text-primary" />
              <span class="text-xl font-bold">Quizify</span>
            </div>
            
            <nav class="space-y-1">
              <ULink
                v-for="item in navigation"
                :key="item.to"
                :to="item.to"
                active-class="bg-primary text-white"
                inactive-class="text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
                class="flex items-center gap-3 px-4 py-2 rounded-lg transition-colors"
              >
                <UIcon :name="item.icon" class="w-5 h-5" />
                <span>{{ item.label }}</span>
              </ULink>
            </nav>
          </div>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 min-w-0">
          <!-- Top Bar -->
          <div class="flex items-center justify-between mb-6">
            <div>
              <h1 class="text-2xl font-bold">{{ route.meta.title || 'Dashboard' }}</h1>
              <p v-if="route.meta.description" class="text-sm text-gray-500 mt-1">
                {{ route.meta.description }}
              </p>
            </div>
            
            <div class="flex items-center gap-4">
              <UButton
                v-if="user"
                color="gray"
                variant="ghost"
                @click="clear(); navigateTo('/login')"
              >
                <UIcon name="i-lucide-log-out" class="w-4 h-4 mr-2" />
                Logout
              </UButton>
            </div>
          </div>

          <slot />
        </main>
      </div>
    </UContainer>
  </div>
</template>
