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
