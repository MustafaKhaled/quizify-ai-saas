<script setup lang="ts">
const { data: page } = await useAsyncData('pricing', () => queryCollection('pricing').first())

const title = page.value?.seo?.title || page.value?.title
const description = page.value?.seo?.description || page.value?.description

useSeoMeta({
  title,
  ogTitle: title,
  description,
  ogDescription: description
})

defineOgImageComponent('Saas')

const isYearly = ref('0')

const items = ref([
  {
    label: 'Monthly',
    value: '0'
  },
  {
    label: 'Yearly',
    value: '1',
    discount: 'Save 25%' // Adding this for the custom slot
  }
])
</script>

<template>
  <div v-if="page">
    <UPageHero
      :title="page.title"
      :description="page.description"
    >
      <template #links>
        <UTabs
          v-model="isYearly"
          :items="items"
          color="neutral"
          size="xs"
          class="w-56" 
          :ui="{
            list: 'ring ring-accented rounded-full',
            indicator: 'rounded-full',
            trigger: 'w-1/2'
          }"
        >
          <template #default="{ item }">
            <div class="flex items-center gap-1.5">
              <span>{{ item.label }}</span>
              <span v-if="item.value === '1'" class="text-green-500 font-bold text-[10px]">
                SAVE 25%
              </span>
            </div>
          </template>
        </UTabs>
      </template>
    </UPageHero>

    <UContainer>
      <UPricingPlans scale>
        <UPricingPlan
          v-for="(plan, index) in page.plans"
          :key="index"
          v-bind="plan"
          :price="isYearly === '1' ? plan.price.year : plan.price.month"
          :billing-cycle="isYearly === '1' ? '/year' : '/month'"
        />
      </UPricingPlans>
    </UContainer>

    <UPageSection>
      <UPageLogos>
        <UIcon
          v-for="icon in page.logos.icons"
          :key="icon"
          :name="icon"
          class="w-12 h-12 flex-shrink-0 text-muted"
        />
      </UPageLogos>
    </UPageSection>

    <UPageSection
      :title="page.faq.title"
      :description="page.faq.description"
    >
      <UAccordion
        :items="page.faq.items"
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
  </div>
</template>
