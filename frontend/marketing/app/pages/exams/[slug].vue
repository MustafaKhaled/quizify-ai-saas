<script setup lang="ts">
const route = useRoute()

const { data: exam } = await useAsyncData(route.path, () =>
  queryCollection('exams').path(route.path).first()
)

if (!exam.value) {
  throw createError({ statusCode: 404, statusMessage: 'Exam landing not found', fatal: true })
}

const title = exam.value.title
const description = exam.value.description

useSeoMeta({
  title,
  ogTitle: title,
  description,
  ogDescription: description
})
</script>

<template>
  <div v-if="exam">
    <UPageHero
      :description="exam.hero.subhead"
      :links="[exam.hero.cta]"
    >
      <template #top>
        <HeroBackground />
      </template>

      <template #headline>
        <span
          class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide"
          :style="{ background: `${exam.color}1A`, color: exam.color }"
        >
          <span class="text-base leading-none">{{ exam.icon }}</span>
          {{ exam.badge }}
        </span>
      </template>

      <template #title>
        <span class="block text-4xl md:text-6xl font-bold leading-tight">
          {{ exam.hero.headline }}
        </span>
        <span
          v-if="exam.hero.tagline"
          class="block text-lg md:text-2xl mt-4 font-medium"
          :style="{ color: exam.color }"
        >{{ exam.hero.tagline }}</span>
      </template>

      <PromotionalVideo />
    </UPageHero>

    <!-- Modules section: rendered when the exam YAML includes a `modules`
         array. Used by level-hub pages (deutsch-a1/a2/b1) to show which
         modules are available at that level — Grammatik, Hören, Lesen.
         Each module card deep-links to its own niched landing page. -->
    <UPageSection
      v-if="exam.modules && exam.modules.items && exam.modules.items.length"
      :title="exam.modules.title"
      :description="exam.modules.description"
    >
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 not-prose">
        <NuxtLink
          v-for="(m, i) in exam.modules.items"
          :key="i"
          :to="m.to"
          class="group relative overflow-hidden rounded-xl border border-default bg-default p-6 transition hover:-translate-y-0.5 hover:shadow-lg block"
        >
          <div
            class="absolute inset-x-0 top-0 h-1"
            :style="{ background: m.color || exam.color }"
          />
          <div class="flex items-start justify-between mb-3">
            <div class="text-3xl leading-none">{{ m.icon }}</div>
            <span
              v-if="m.badge"
              class="text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full"
              :style="{ background: `${(m.color || exam.color)}1A`, color: m.color || exam.color }"
            >
              {{ m.badge }}
            </span>
          </div>
          <div class="font-semibold text-highlighted mb-1.5">{{ m.title }}</div>
          <p class="text-sm text-muted leading-relaxed">{{ m.description }}</p>
          <div
            class="mt-4 inline-flex items-center gap-1 text-xs font-medium opacity-0 group-hover:opacity-100 transition"
            :style="{ color: m.color || exam.color }"
          >
            {{ m.cta || 'Open module' }}
            <UIcon
              name="i-lucide-arrow-right"
              class="size-3.5"
            />
          </div>
        </NuxtLink>
      </div>
    </UPageSection>

    <UPageSection
      :title="exam.pains.title"
      :description="exam.pains.description"
    >
      <ul class="not-prose grid sm:grid-cols-2 gap-3 max-w-3xl mx-auto">
        <li
          v-for="(pain, i) in exam.pains.items"
          :key="i"
          class="flex items-start gap-3 p-4 rounded-xl border border-default bg-default"
        >
          <UIcon
            name="i-lucide-alert-circle"
            class="size-5 shrink-0 mt-0.5"
            :style="{ color: exam.color }"
          />
          <span class="text-default text-sm leading-relaxed">{{ pain }}</span>
        </li>
      </ul>
    </UPageSection>

    <UPageSection
      :title="exam.promises.title"
      :description="exam.promises.description"
    >
      <UPageGrid>
        <UPageCard
          v-for="(item, i) in exam.promises.items"
          :key="i"
          v-bind="item"
          spotlight
        />
      </UPageGrid>
    </UPageSection>

    <UPageSection
      :title="exam.comparison.title"
      :description="exam.comparison.description"
    >
      <ComparisonTable
        :columns="exam.comparison.columns"
        :rows="exam.comparison.rows"
        :accent="exam.color"
      />
    </UPageSection>

    <UPageSection
      v-if="exam.testimonials"
      :title="exam.testimonials.title"
    >
      <UPageColumns class="xl:columns-3">
        <UPageCard
          v-for="(t, i) in exam.testimonials.items"
          :key="i"
          variant="subtle"
          :description="t.quote"
          :ui="{ description: 'before:content-[open-quote] after:content-[close-quote]' }"
        >
          <template #footer>
            <UUser
              v-bind="t.user"
              size="lg"
            />
          </template>
        </UPageCard>
      </UPageColumns>
    </UPageSection>

    <UPageSection
      :title="exam.faq.title || 'Frequently asked questions'"
    >
      <UAccordion
        :items="exam.faq.items"
        :unmount-on-hide="false"
        :default-value="['0']"
        type="multiple"
        class="max-w-3xl mx-auto"
        :ui="{
          trigger: 'text-base text-highlighted',
          body: 'text-base text-muted'
        }"
      />
    </UPageSection>

    <UPageSection class="text-center">
      <NuxtLink
        :to="exam.hero.cta.to"
        class="inline-flex items-center gap-2 px-8 py-4 rounded-xl text-lg font-semibold text-white shadow-lg hover:-translate-y-0.5 transition"
        :style="{ background: exam.color }"
      >
        {{ exam.hero.cta.label }}
        <UIcon
          name="i-lucide-arrow-right"
          class="size-5"
        />
      </NuxtLink>
    </UPageSection>
  </div>
</template>
