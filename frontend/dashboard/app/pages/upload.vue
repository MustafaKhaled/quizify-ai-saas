<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

definePageMeta({
  title: 'Upload PDF',
  description: 'Upload a PDF to generate quiz questions'
})

const schema = z.object({
  file: z.any().optional(),
  source_id: z.string().optional(),
  quiz_name: z.string().min(1, 'Quiz name is required'),
  quiz_type: z.enum(['single_choice', 'multiple_select']),
  num_questions: z.number().min(1).max(50),
  time_limit: z.number().optional(),
  start_page: z.number().optional(),
  end_page: z.number().optional()
})

type Schema = z.output<typeof schema>

const state = reactive<Partial<Schema>>({
  file: undefined,
  source_id: undefined,
  quiz_name: undefined,
  quiz_type: 'single_choice',
  num_questions: 5,
  time_limit: undefined,
  start_page: undefined,
  end_page: undefined
})

const toast = useToast()
const loading = ref(false)

// Fetch existing sources
const { data: sources } = await useFetch('/api/sources', {
  lazy: true,
  default: () => []
})

const useExistingSource = ref(false)

async function onSubmit(event: FormSubmitEvent<Schema>) {
  if (!useExistingSource.value && !event.data.file) {
    toast.add({
      title: 'Error',
      description: 'Please upload a PDF file or select an existing source',
      color: 'error'
    })
    return
  }

  loading.value = true
  try {
    const formData = new FormData()
    
    if (!useExistingSource.value && event.data.file) {
      formData.append('file', event.data.file)
    } else if (useExistingSource.value && event.data.source_id) {
      formData.append('source_id', event.data.source_id)
    }

    formData.append('quiz_name', event.data.quiz_name)
    formData.append('quiz_type', event.data.quiz_type)
    formData.append('num_questions', event.data.num_questions.toString())
    
    if (event.data.time_limit) {
      formData.append('time_limit', event.data.time_limit.toString())
    }
    if (event.data.start_page) {
      formData.append('start_page', event.data.start_page.toString())
    }
    if (event.data.end_page) {
      formData.append('end_page', event.data.end_page.toString())
    }

    const quiz = await $fetch('/api/quiz/create', {
      method: 'POST',
      body: formData,
      // Don't set Content-Type header, let browser set it with boundary for FormData
    })

    toast.add({
      title: 'Success',
      description: 'Quiz created successfully!',
      color: 'success'
    })

    await navigateTo(`/quiz/${quiz.id}`)
  } catch (err: any) {
    toast.add({
      title: 'Error',
      description: err?.data?.message || 'Failed to create quiz',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <UCard>
      <template #header>
        <h2 class="text-xl font-semibold">Create Quiz from PDF</h2>
      </template>

      <UForm
        :schema="schema"
        :state="state"
        class="space-y-6"
        @submit="onSubmit"
      >
        <!-- Use Existing Source Toggle -->
        <UFormField label="Use Existing PDF Source" name="use_existing">
          <UCheckbox v-model="useExistingSource" />
        </UFormField>

        <!-- Existing Source Selection -->
        <UFormField
          v-if="useExistingSource"
          label="Select PDF Source"
          name="source_id"
        >
          <USelect
            v-model="state.source_id"
            :options="sources.map((s: any) => ({ label: s.file_name, value: s.id }))"
            placeholder="Select a source"
          />
        </UFormField>

        <!-- File Upload -->
        <UFormField
          v-else
          label="PDF File"
          name="file"
          required
        >
          <UInput
            type="file"
            accept=".pdf"
            @change="(e: any) => state.file = e.target.files?.[0]"
          />
        </UFormField>

        <!-- Quiz Name -->
        <UFormField label="Quiz Name" name="quiz_name" required>
          <UInput v-model="state.quiz_name" placeholder="Enter quiz name" />
        </UFormField>

        <!-- Quiz Type -->
        <UFormField label="Quiz Type" name="quiz_type" required>
          <USelect
            v-model="state.quiz_type"
            :options="[
              { label: 'Single Choice', value: 'single_choice' },
              { label: 'Multiple Select', value: 'multiple_select' }
            ]"
          />
        </UFormField>

        <!-- Number of Questions -->
        <UFormField label="Number of Questions" name="num_questions" required>
          <UInput
            v-model.number="state.num_questions"
            type="number"
            min="1"
            max="50"
          />
        </UFormField>

        <!-- Time Limit (Optional) -->
        <UFormField label="Time Limit (minutes, optional)" name="time_limit">
          <UInput
            v-model.number="state.time_limit"
            type="number"
            min="1"
            placeholder="Leave empty for no time limit"
          />
        </UFormField>

        <!-- Page Range (Optional) -->
        <div class="grid grid-cols-2 gap-4">
          <UFormField label="Start Page (optional)" name="start_page">
            <UInput
              v-model.number="state.start_page"
              type="number"
              min="1"
              placeholder="1"
            />
          </UFormField>
          <UFormField label="End Page (optional)" name="end_page">
            <UInput
              v-model.number="state.end_page"
              type="number"
              min="1"
              placeholder="Last page"
            />
          </UFormField>
        </div>

        <div class="flex justify-end gap-2">
          <UButton
            label="Cancel"
            color="gray"
            variant="ghost"
            to="/"
          />
          <UButton
            label="Create Quiz"
            type="submit"
            :loading="loading"
          />
        </div>
      </UForm>
    </UCard>
  </div>
</template>
