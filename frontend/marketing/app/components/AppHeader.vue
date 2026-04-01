<script setup lang="ts">
const route = useRoute()
const config = useRuntimeConfig()

const isLoggedIn = ref(false)

onMounted(async () => {
  try {
    await $fetch(`${config.public.apiBase || 'http://localhost:8000'}/auth/verify`, { credentials: 'include' })
    isLoggedIn.value = true
  } catch {
    isLoggedIn.value = false
  }
})

const dashboardUrl = computed(() =>
  config.public.dashboardUrl || 'http://localhost:3001'
)

function goToDashboard() {
  window.location.href = dashboardUrl.value
}

async function logout() {
  try {
    await $fetch(`${config.public.apiBase || 'http://localhost:8000'}/auth/logout`, {
      method: 'POST',
      credentials: 'include'
    })
  } catch {}
  isLoggedIn.value = false
  await navigateTo('/login')
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
          icon="i-lucide-log-out"
          color="neutral"
          variant="ghost"
          class="lg:hidden"
          @click="logout"
        />
        <UButton
          label="Your Account"
          color="primary"
          variant="solid"
          icon="i-lucide-layout-dashboard"
          class="hidden lg:inline-flex"
          @click="goToDashboard"
        />
        <UButton
          label="Log out"
          color="neutral"
          variant="outline"
          icon="i-lucide-log-out"
          class="hidden lg:inline-flex"
          @click="logout"
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
          class="mb-3"
          @click="goToDashboard"
        />
        <UButton
          label="Log out"
          color="neutral"
          variant="subtle"
          icon="i-lucide-log-out"
          block
          class="mb-1"
          @click="logout"
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
