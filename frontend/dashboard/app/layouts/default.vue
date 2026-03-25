<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

const open = ref(false)

const links = [[{
  label: 'Dashboard',
  icon: 'i-lucide-house',
  to: '/dashboard',
  onSelect: () => {
    open.value = false
  }
}, {
  label: 'New Quiz',
  icon: 'i-lucide-plus-circle',
  to: '/quiz-new',
  onSelect: () => {
    open.value = false
  }
}, {
  label: 'My Quizzes',
  icon: 'i-lucide-book-open',
  to: '/quizzes',
  onSelect: () => {
    open.value = false
  }
}]] satisfies NavigationMenuItem[][]
</script>

<template>
  <UDashboardGroup unit="rem">
    <UDashboardSidebar
      id="default"
      v-model:open="open"
      collapsible
      resizable
      class="bg-elevated/25"
      :ui="{ footer: 'lg:border-t lg:border-default' }"
    >
      <template #header="{ collapsed }">
        <TeamsMenu :collapsed="collapsed" />
      </template>

      <template #default="{ collapsed }">
        <UDashboardSearchButton :collapsed="collapsed" class="bg-transparent ring-default" />

        <UNavigationMenu
          :collapsed="collapsed"
          :items="links[0]"
          orientation="vertical"
          tooltip
          popover
        />
      </template>

      <template #footer="{ collapsed }">
        <UserMenu :collapsed="collapsed" />
      </template>
    </UDashboardSidebar>

    <slot />

    <NotificationsSlideover />
  </UDashboardGroup>
</template>
