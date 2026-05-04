<script setup lang="ts">
defineProps<{
  columns: Array<{ name: string, highlight?: boolean }>
  rows: Array<{ feature: string, values: Array<'yes' | 'no' | 'partial'> }>
  // Optional brand color for the highlighted Quizify column header bar.
  accent?: string
}>()

const STATUS_META = {
  yes: { icon: 'i-lucide-check', class: 'text-success' },
  no: { icon: 'i-lucide-x', class: 'text-error opacity-60' },
  partial: { icon: 'i-lucide-minus', class: 'text-warning' }
} as const
</script>

<template>
  <div class="not-prose overflow-x-auto">
    <table class="w-full border-collapse">
      <thead>
        <tr>
          <th class="text-left text-xs uppercase tracking-wide text-muted font-semibold pb-4 pr-4">
            Capability
          </th>
          <th
            v-for="(col, i) in columns"
            :key="i"
            class="text-center text-sm font-semibold pb-4 px-4 relative"
            :class="col.highlight ? 'text-highlighted' : 'text-muted'"
          >
            <div
              v-if="col.highlight && accent"
              class="absolute inset-x-2 top-0 h-1 rounded-full"
              :style="{ background: accent }"
            />
            {{ col.name }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, ri) in rows"
          :key="ri"
          class="border-t border-default"
        >
          <td class="py-3 pr-4 text-sm text-default">{{ row.feature }}</td>
          <td
            v-for="(val, ci) in row.values"
            :key="ci"
            class="py-3 px-4 text-center"
            :class="columns[ci]?.highlight ? 'bg-elevated/40' : ''"
          >
            <UIcon
              :name="STATUS_META[val].icon"
              class="size-5 inline-block"
              :class="STATUS_META[val].class"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
