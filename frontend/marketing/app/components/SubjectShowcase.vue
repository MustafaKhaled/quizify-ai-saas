<script setup lang="ts">
// Each tile links to a content file at content/6.exams/<slug>.yml. The
// German tiles are CEFR-level hubs — each level's page lists which modules
// (Grammatik / Hören / Lesen) are available at that level. The level
// pages handle deep links to the per-module landings.
const subjects = [
  {
    slug: 'pmp',
    name: 'PMP Certification',
    icon: '📋',
    color: '#F97316',
    description: 'Project Management Professional. Full coverage of every PMI process group and knowledge area.',
    badge: 'PMI',
    modules: '',
    to: '/exams/pmp'
  },
  {
    slug: 'clf_c02',
    name: 'AWS Cloud Practitioner',
    icon: '☁️',
    color: '#FF9900',
    description: 'CLF-C02 exam prep across all four domains: cloud concepts, security, services, and billing.',
    badge: 'AWS',
    modules: '',
    to: '/exams/clf-c02'
  },
  {
    slug: 'deutsch_a1',
    name: 'German A1',
    icon: '🇩🇪',
    color: '#DC2626',
    description: 'Goethe-Zertifikat A1 prep — calibrated to the question style of the real exam.',
    badge: 'CEFR · A1',
    modules: 'Grammatik',
    to: '/exams/deutsch-a1'
  },
  {
    slug: 'deutsch_a2',
    name: 'German A2',
    icon: '🇩🇪',
    color: '#991B1B',
    description: 'Goethe-Zertifikat A2 — grammar drills plus full Hören and Lesen mock exams on demand.',
    badge: 'CEFR · A2',
    modules: 'Grammatik · Hören · Lesen',
    to: '/exams/deutsch-a2'
  },
  {
    slug: 'deutsch_b1',
    name: 'German B1',
    icon: '🇩🇪',
    color: '#7F1D1D',
    description: 'Goethe-Zertifikat B1 — grammar drills plus full Hören and Lesen mock exams on demand.',
    badge: 'CEFR · B1',
    modules: 'Grammatik · Hören · Lesen',
    to: '/exams/deutsch-b1'
  }
]
</script>

<template>
  <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 not-prose">
    <NuxtLink
      v-for="s in subjects"
      :key="s.slug"
      :to="s.to"
      class="group relative overflow-hidden rounded-xl border border-default bg-default p-6 transition hover:-translate-y-0.5 hover:shadow-lg block"
    >
      <div
        class="absolute inset-x-0 top-0 h-1"
        :style="{ background: s.color }"
      />
      <div class="flex items-start justify-between mb-3">
        <div class="text-3xl leading-none">{{ s.icon }}</div>
        <span
          class="text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full"
          :style="{ background: `${s.color}1A`, color: s.color }"
        >
          {{ s.badge }}
        </span>
      </div>
      <div class="font-semibold text-highlighted mb-1.5">{{ s.name }}</div>
      <p class="text-sm text-muted leading-relaxed">{{ s.description }}</p>
      <p
        v-if="s.modules"
        class="mt-3 text-xs font-medium"
        :style="{ color: s.color }"
      >
        {{ s.modules }}
      </p>
      <div
        class="mt-4 inline-flex items-center gap-1 text-xs font-medium opacity-0 group-hover:opacity-100 transition"
        :style="{ color: s.color }"
      >
        Explore the track
        <UIcon
          name="i-lucide-arrow-right"
          class="size-3.5"
        />
      </div>
    </NuxtLink>
  </div>
</template>
