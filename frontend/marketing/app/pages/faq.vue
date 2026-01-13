<script setup lang="ts">
    // Change 'queryCollection' to 'queryContent'
    const { data: page } = await useAsyncData('faq', () => queryCollection('faq').first())
    const title = computed(() => page.value?.title || 'FAQ - Quizify AI')
    const description = computed(() => page.value?.description || 'Common questions about AI quiz generation.')
    
    useSeoMeta({
      title,
      description
    })
    </script>
    
    <template>
        <UContainer v-if="page" class="py-12">
          <UPageHeader
            :title="page.title"
            :description="page.description"
            class="max-w-none" 
          />
      
          <UPageBody>
            <UAccordion 
              :items="page.items" 
              multiple 
              class="w-full mt-8"
              :ui="{
                wrapper: 'flex flex-col w-full',
                container: 'w-full',
                item: {
                  padding: 'px-4 pb-4 pt-1.5'
                }
              }"
            />
          </UPageBody>
        </UContainer>
      </template>