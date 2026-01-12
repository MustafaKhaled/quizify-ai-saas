<script setup lang="ts">
const route = useRoute()

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
      <TemplateMenu />
    </template>

    <UNavigationMenu
      :items="items"
      variant="link"
    />

    <template #right>
      <UColorModeButton />

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
        color="secondary"
        variant="solid"
        to="/pricing"
        class="lg:hidden lg:inline-flex"
        />

    </template>

    <template #body>
      <UNavigationMenu
        :items="items"
        orientation="vertical"
        class="-mx-2.5"
      />

      <USeparator class="my-6" />

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
        color="solid"
        variant="subtle"
        to="/pricing"
        block
        class="mb-1"
        />

    </template>
  </UHeader>
</template>
