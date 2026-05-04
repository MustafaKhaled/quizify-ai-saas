<script setup lang="ts">
// Mirrors backend/agents/__init__.py PREDEFINED_AGENTS — keep slug, name,
// color, and icon in sync with the agent registry. Static here so the
// marketing site renders without depending on the API being up.
// `to` matches a content file at content/6.exams/<slug>.yml — the dynamic
// page at app/pages/exams/[slug].vue renders the niched landing.
const subjects = [
  {
    slug: 'pmp',
    name: 'PMP Certification',
    icon: '📋',
    color: '#F97316',
    description: 'Project Management Professional. Full coverage of every PMI process group and knowledge area.',
    badge: 'PMI',
    to: '/exams/pmp'
  },
  {
    slug: 'clf_c02',
    name: 'AWS Cloud Practitioner',
    icon: '☁️',
    color: '#FF9900',
    description: 'CLF-C02 exam prep across all four domains: cloud concepts, security, services, and billing.',
    badge: 'AWS',
    to: '/exams/clf-c02'
  },
  {
    slug: 'deutsch_a1',
    name: 'German Grammar A1',
    icon: '🇩🇪',
    color: '#DC2626',
    description: 'CEFR A1 grammar drills modeled on Goethe-Zertifikat, telc, and ÖSD A1 question style.',
    badge: 'CEFR A1',
    to: '/exams/deutsch-a1'
  },
  {
    slug: 'deutsch_a2',
    name: 'German Grammar A2',
    icon: '🇩🇪',
    color: '#991B1B',
    description: 'Dativ, Wechselpräpositionen, Konjunktiv II, Nebensätze — every A2 grammar rule.',
    badge: 'CEFR A2',
    to: '/exams/deutsch-a2'
  }
]
</script>

<template>
  <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 not-prose">
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
