<script setup lang="ts">
    // 1. Data Fetching: This pulls the content from your /content/faq.yml file
    const { data: page } = await useAsyncData('faq', () => queryCollection('faq').first())

    const title = page.value?.seo?.title || page.value?.title
    const description = page.value?.seo?.description || page.value?.description

    useSeoMeta({
    title,
    ogTitle: title,
    description,
    ogDescription: description
    })

    // 2. SEO: This tells Google what this page is about
    useSeoMeta({
      title: 'FAQ - Quizify AI',
      description: 'Common questions about AI quiz generation and exam timers.'
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
    </template>