<script setup lang="ts">
const route = useRoute()
const config = useRuntimeConfig()

const isLoggedIn = ref(false)

function hasValidToken(): boolean {
  const token = localStorage.getItem('auth_token')
  if (!token) return false
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    if (payload.exp && payload.exp * 1000 < Date.now()) {
      localStorage.removeItem('auth_token')
      return false
    }
    return true
  } catch {
    localStorage.removeItem('auth_token')
    return false
  }
}

onMounted(() => {
  isLoggedIn.value = hasValidToken()
})

const dashboardUrl = computed(() =>
  config.public.dashboardUrl || 'http://localhost:3001'
)

function goToDashboard() {
  const token = localStorage.getItem('auth_token')
  window.location.href = `${dashboardUrl.value}?token=${token}`
}

const items = computed(() => [{
  label: 'Home',
  to: '/',
  active: route.path.startsWith('/docs')
}, {
  label: 'Pricing',
  to: '/pricing'
},
{
  label: 'FAQ',
  to: '/faq'
},
{
  label: 'Blog',
  to: '/blog'
}])
</script>

<template>
  <UHeader>
    <template #left>
      <NuxtLink to="/">
        <AppLogo class="w-auto h-6 shrink-0" />
      </NuxtLink>
    </template>

    <UNavigationMenu
      :items="items"
      variant="link"
    />

    <template #right>
      <UColorModeButton />

      <!-- Logged in state -->
      <template v-if="isLoggedIn">
        <UButton
          icon="i-lucide-layout-dashboard"
          color="neutral"
          variant="ghost"
          class="lg:hidden"
          @click="goToDashboard"
        />
        <UButton
          label="Your Account"
          color="primary"
          variant="solid"
          icon="i-lucide-layout-dashboard"
          class="hidden lg:inline-flex"
          @click="goToDashboard"
        />
      </template>

      <!-- Logged out state -->
      <template v-else>
        <UButton
          icon="i-lucide-log-in"
          color="neutral"
          variant="ghost"
          to="/login"
          class="lg:hidden"
        />
        <UButton
          label="Sign in"
          color="neutral"
          variant="outline"
          to="/login"
          class="hidden lg:inline-flex"
        />
        <UButton
          label="Get Started"
          color="primary"
          variant="solid"
          to="/pricing"
          class="hidden lg:inline-flex"
        />
      </template>
    </template>

    <template #body>
      <UNavigationMenu
        :items="items"
        orientation="vertical"
        class="-mx-2.5"
      />

      <USeparator class="my-6" />

      <template v-if="isLoggedIn">
        <UButton
          label="Your Account"
          color="primary"
          variant="solid"
          icon="i-lucide-layout-dashboard"
          block
          class="mb-1"
          @click="goToDashboard"
        />
      </template>
      <template v-else>
        <UButton
          label="Sign in"
          color="neutral"
          variant="subtle"
          to="/login"
          block
          class="mb-3"
        />
        <UButton
          label="Get Started"
          color="primary"
          variant="solid"
          to="/pricing"
          block
          class="mb-1"
        />
      </template>
    </template>
  </UHeader>
</template>
