<script setup lang="ts">
  // 1. Data Fetching
  const { data: page } = await useAsyncData('faq', () => queryCollection('faq').first())
  
  // 2. SEO Logic
  // We use a computed property or watch the page data to ensure title/desc update when data loads
  const title = computed(() => page.value?.title || 'FAQ - Quizify AI')
  const description = computed(() => page.value?.description || 'Common questions about AI quiz generation.')
  
  useSeoMeta({
    title: title,
    ogTitle: title,
    description: description,
    ogDescription: description
  })
  </script>
  
  <template>
    <UContainer v-if="page" class="py-12">
      <UPageHeader
        :title="page.title"
        :description="page.description"
      />
  
      <UPageBody>
        <UAccordion 
          :items="page.items" 
          multiple 
          class="max-w-3xl mx-auto mt-8"
        />
      </UPageBody>
    </UContainer>
    
    <UContainer v-else class="py-12 text-center">
      <p>Loading FAQ...</p>
    </UContainer>
  </template>