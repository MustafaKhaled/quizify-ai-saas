<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="w-full px-4 py-12">
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-2">Create Quiz</h1>
        <p class="text-gray-600 dark:text-gray-400">Upload a PDF and generate an AI-powered quiz</p>
      </div>

      <!-- Upload Section -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Upload PDF</h2>
        
        <div
          class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center transition-colors"
          :class="isDragover ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-500' : ''"
          @dragover.prevent="isDragover = true"
          @dragleave.prevent="isDragover = false"
          @drop.prevent="handleFileDrop"
        >
          <div class="mb-4">
            <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
              <path d="M28 8H12a4 4 0 00-4 4v20a4 4 0 004 4h24a4 4 0 004-4V20m-8-12l-4-4m0 0l-4 4m4-4v12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <p class="text-lg font-semibold text-gray-900 dark:text-white mb-1">Drag and drop your PDF</p>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">or click to browse</p>
          <input
            ref="fileInput"
            type="file"
            accept=".pdf"
            class="hidden"
            @change="handleFileSelect"
          />
          <button
            @click="fileInput?.click()"
            :disabled="isUploading"
            class="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {{ isUploading ? 'Uploading...' : 'Choose PDF' }}
          </button>
        </div>

        <div v-if="uploadedSource" class="mt-4 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
          <p class="text-green-800 dark:text-green-200">✓ {{ uploadedSource.file_name }} uploaded successfully</p>
        </div>
      </div>

      <!-- Quiz Configuration -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Quiz Settings</h2>
        
        <form @submit.prevent="createQuiz" class="space-y-4">
          <!-- Quiz Title -->
          <div>
            <label class="block text-sm font-medium text-gray-900 dark:text-white mb-2">Quiz Title *</label>
            <input
              v-model="formData.quiz_name"
              type="text"
              placeholder="e.g., Introduction to Biology"
              required
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- Quiz Type -->
          <div>
            <label class="block text-sm font-medium text-gray-900 dark:text-white mb-2">Question Type</label>
            <select
              v-model="formData.quiz_type"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="single_choice">Multiple Choice</option>
              <option value="multiple_select">Multiple Select</option>
            </select>
          </div>

          <!-- Number of Questions -->
          <div>
            <label class="block text-sm font-medium text-gray-900 dark:text-white mb-2">Number of Questions *</label>
            <input
              v-model.number="formData.num_questions"
              type="number"
              min="1"
              max="50"
              required
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- Time Limit -->
          <div>
            <label class="block text-sm font-medium text-gray-900 dark:text-white mb-2">Time Limit (minutes, optional)</label>
            <input
              v-model.number="formData.time_limit"
              type="number"
              min="1"
              placeholder="Leave empty for unlimited"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="isCreating || !uploadedSource"
            class="w-full px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
          >
            {{ isCreating ? 'Creating Quiz...' : 'Create Quiz' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const fileInput = ref<HTMLInputElement>()
const isDragover = ref(false)
const isUploading = ref(false)
const isCreating = ref(false)
const uploadedSource = ref<any>(null)

const formData = ref({
  source_id: '',
  quiz_name: '',
  quiz_type: 'single_choice',
  num_questions: 10,
  time_limit: null as number | null
})

const handleFileDrop = async (e: DragEvent) => {
  isDragover.value = false
  const files = e.dataTransfer?.files
  if (files?.length) {
    await uploadFile(files[0])
  }
}

const handleFileSelect = async (e: Event) => {
  const files = (e.target as HTMLInputElement).files
  if (files?.length) {
    await uploadFile(files[0])
  }
}

const uploadFile = async (file: File) => {
  if (!file.type.includes('pdf')) {
    alert('Please upload a PDF file')
    return
  }

  try {
    isUploading.value = true
    const formDataToSend = new FormData()
    formDataToSend.append('file', file)
    
    const { $fetch } = useNuxtApp()
    const config = useRuntimeConfig()
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null

    const response = await $fetch(`${config.public.apiBase}/sources/upload`, {
      method: 'POST',
      body: formDataToSend,
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })

    uploadedSource.value = response
    formData.value.source_id = response.id
  } catch (error) {
    console.error('Upload failed:', error)
    alert('Failed to upload PDF')
  } finally {
    isUploading.value = false
  }
}

const createQuiz = async () => {
  if (!formData.value.source_id) {
    alert('Please upload a PDF first')
    return
  }

  if (!formData.value.quiz_name.trim()) {
    alert('Please enter a quiz title')
    return
  }

  try {
    isCreating.value = true
    const { $fetch } = useNuxtApp()
    const config = useRuntimeConfig()
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null

    const formDataToSend = new FormData()
    formDataToSend.append('source_id', formData.value.source_id)
    formDataToSend.append('quiz_name', formData.value.quiz_name)
    formDataToSend.append('quiz_type', formData.value.quiz_type)
    formDataToSend.append('num_questions', String(formData.value.num_questions))
    if (formData.value.time_limit) {
      formDataToSend.append('time_limit', String(formData.value.time_limit))
    }

    const quiz = await $fetch(`${config.public.apiBase}/quizzes/create`, {
      method: 'POST',
      body: formDataToSend,
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })

    alert('Quiz created successfully!')
    await navigateTo(`/quiz/${quiz.id}`)
  } catch (error: any) {
    console.error('Quiz creation failed:', error)
    alert(error?.data?.detail || 'Failed to create quiz')
  } finally {
    isCreating.value = false
  }
}
</script>
