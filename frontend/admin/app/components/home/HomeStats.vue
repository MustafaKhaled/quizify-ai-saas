<script setup lang="ts">
import type { Period, Range, Stat } from '~/types'

const props = defineProps<{
  period: Period
  range: Range
}>()

function formatCurrency(value: number): string {
  return value.toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0
  })
}

const { data: stats } = await useAsyncData<Stat[]>('stats', async () => {
  try {
    const statsData = await $fetch('/api/stats')
    
    return [{
      title: 'Total Users',
      icon: 'i-lucide-users',
      value: statsData.totalUsers.value,
      variation: statsData.totalUsers.variation
    }, {
      title: 'Pro Users',
      icon: 'i-lucide-crown',
      value: statsData.proUsers.value,
      variation: statsData.proUsers.variation
    }, {
      title: 'Total Quizzes',
      icon: 'i-lucide-file-question',
      value: statsData.totalQuizzes.value,
      variation: statsData.totalQuizzes.variation
    }, {
      title: 'PDF Sources',
      icon: 'i-lucide-file-text',
      value: statsData.totalSources.value,
      variation: statsData.totalSources.variation
    }]
  } catch (err) {
    console.error('Failed to fetch stats:', err)
    // Return default stats on error
    return [{
      title: 'Total Users',
      icon: 'i-lucide-users',
      value: 0,
      variation: 0
    }, {
      title: 'Pro Users',
      icon: 'i-lucide-crown',
      value: 0,
      variation: 0
    }, {
      title: 'Total Quizzes',
      icon: 'i-lucide-file-question',
      value: 0,
      variation: 0
    }, {
      title: 'PDF Sources',
      icon: 'i-lucide-file-text',
      value: 0,
      variation: 0
    }]
  }
}, {
  watch: [() => props.period, () => props.range],
  default: () => []
})
</script>

<template>
  <UPageGrid class="lg:grid-cols-4 gap-4 sm:gap-6 lg:gap-px">
    <UPageCard
      v-for="(stat, index) in stats"
      :key="index"
      :icon="stat.icon"
      :title="stat.title"
      to="/customers"
      variant="subtle"
      :ui="{
        container: 'gap-y-1.5',
        wrapper: 'items-start',
        leading: 'p-2.5 rounded-full bg-primary/10 ring ring-inset ring-primary/25 flex-col',
        title: 'font-normal text-muted text-xs uppercase'
      }"
      class="lg:rounded-none first:rounded-l-lg last:rounded-r-lg hover:z-1"
    >
      <div class="flex items-center gap-2">
        <span class="text-2xl font-semibold text-highlighted">
          {{ stat.value }}
        </span>

        <UBadge
          :color="stat.variation > 0 ? 'success' : 'error'"
          variant="subtle"
          class="text-xs"
        >
          {{ stat.variation > 0 ? '+' : '' }}{{ stat.variation }}%
        </UBadge>
      </div>
    </UPageCard>
  </UPageGrid>
</template>
