<template>
  <UDashboardPanel grow>
    <UDashboardPanelContent class="p-6 overflow-y-auto bg-mesh">
      <div class="mb-8">
        <h1 class="text-4xl font-bold gradient-text mb-2">
          {{ mode === 'focused' ? '🎯 Practice Weak Areas' : 'Create Quiz' }}
        </h1>
        <p class="text-slate-500 dark:text-slate-400">
          {{ mode === 'focused'
            ? `Generate a quiz focused on: ${focusTopics.join(', ')}`
            : existingSourceName
              ? `Generating from source: ${existingSourceName}`
              : 'Upload a file and generate an AI-powered quiz' }}
        </p>
      </div>

      <!-- Upload Section (only for normal mode) -->
      <div v-if="mode === 'normal'" class="glass-card rounded-2xl p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Upload File</h2>
        
        <div
          class="border-2 border-dashed border-white/30 dark:border-white/15 rounded-2xl p-8 text-center transition-colors"
          :class="isDragover ? 'bg-blue-500/10 border-blue-500/40' : ''"
          @dragover.prevent="isDragover = true"
          @dragleave.prevent="isDragover = false"
          @drop.prevent="handleFileDrop"
        >
          <div class="mb-4">
            <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
              <path d="M28 8H12a4 4 0 00-4 4v20a4 4 0 004 4h24a4 4 0 004-4V20m-8-12l-4-4m0 0l-4 4m4-4v12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <p class="text-lg font-semibold text-slate-900 dark:text-white mb-1">Drag and drop your file</p>
          <p class="text-sm text-slate-500 dark:text-slate-400 mb-4">PDF, DOCX, PPTX, or TXT</p>
          <input
            ref="fileInput"
            type="file"
            accept=".pdf,.docx,.pptx,.txt"
            class="hidden"
            @change="handleFileSelect"
          />
          <button
            @click="fileInput?.click()"
            :disabled="isCreating"
            class="inline-block px-6 py-2 btn-gradient rounded-xl disabled:opacity-50 transition-colors"
          >
            Choose File
          </button>
        </div>

        <!-- Source Name — always visible so user can name before selecting file -->
        <div class="mt-4 space-y-3">
          <div>
            <label class="block text-sm font-medium text-gray-900 dark:text-white mb-1">Source Name</label>
            <input
              v-model="sourceName"
              type="text"
              placeholder="e.g. Chapter 1, Lecture Notes"
              class="w-full px-4 py-2 glass-input rounded-xl text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p class="text-xs text-slate-400 dark:text-slate-500 mt-1">A friendly name for this source</p>
          </div>
          <div v-if="selectedFile" class="p-4 bg-green-500/10 border border-green-500/20 rounded-xl">
            <p class="text-green-800 dark:text-green-200"><UIcon name="i-lucide-check-circle" class="w-4 h-4 inline text-green-500" /> {{ selectedFile.name }} selected</p>
          </div>
        </div>
      </div>

      <!-- Source info when using existing source (non-editable) -->
      <div v-if="mode !== 'normal' && existingSourceName" class="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 mb-6 border border-gray-200 dark:border-gray-700">
        <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-0.5">Source</p>
        <p class="font-medium text-gray-900 dark:text-white">{{ existingSourceName }}</p>
      </div>

      <!-- Quiz Configuration -->
      <div class="glass-card rounded-2xl p-6">
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
              class="w-full px-4 py-2 glass-input rounded-xl text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- Quiz Type -->
          <div>
            <label class="block text-sm font-medium text-gray-900 dark:text-white mb-2">Question Type</label>
            <select
              v-model="formData.quiz_type"
              class="w-full px-4 py-2 glass-input rounded-xl text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="single_choice">Multiple Choice</option>
              <option value="multiple_select">Multiple Select</option>
              <option value="true_or_false">True or False</option>
            </select>
          </div>

          <!-- Number of Questions -->
          <div>
            <label class="block text-sm font-medium text-gray-900 dark:text-white mb-2">Number of Questions *</label>
            <input
              v-model.number="formData.num_questions"
              type="number"
              min="1"
              max="30"
              required
              class="w-full px-4 py-2 glass-input rounded-xl text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
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
              class="w-full px-4 py-2 glass-input rounded-xl text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="isCreating || (mode === 'normal' && !selectedFile)"
            class="w-full px-6 py-2 btn-gradient rounded-xl disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {{ isCreating ? 'Creating Quiz...' : 'Create Quiz' }}
          </button>
        </form>
      </div>
    </UDashboardPanelContent>

    <SubscriptionModal v-model="showSubscriptionModal" />
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const route = useRoute()
const fileInput = ref<HTMLInputElement>()
const isDragover = ref(false)
const isCreating = ref(false)
const selectedFile = ref<File | null>(null)
const showSubscriptionModal = ref(false)

// Support for focused quiz mode
const mode = ref<'normal' | 'focused' | 'full'>('normal')
const focusTopics = ref<string[]>([])
const sourceId = ref<string | null>(null)
const subjectId = ref<string | null>(null)
const sourceName = ref('')            // editable name for new upload
const existingSourceName = ref('')    // read-only display for existing source

const formData = ref({
  quiz_name: '',
  quiz_type: 'single_choice',
  num_questions: 10,
  time_limit: null as number | null
})

const handleFileDrop = (e: DragEvent) => {
  isDragover.value = false
  const files = e.dataTransfer?.files
  if (files?.length && files[0]) {
    selectFile(files[0])
  }
}

const handleFileSelect = (e: Event) => {
  const files = (e.target as HTMLInputElement).files
  if (files?.length && files[0]) {
    selectFile(files[0])
  }
}

const SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.pptx', '.txt']

const selectFile = (file: File) => {
  const ext = '.' + file.name.split('.').pop()?.toLowerCase()
  if (!SUPPORTED_EXTENSIONS.includes(ext)) {
    alert('Unsupported file type. Please upload a PDF, DOCX, PPTX, or TXT file.')
    return
  }
  selectedFile.value = file
  // Auto-fill source name with file name (without extension) if not already set
  if (!sourceName.value) {
    sourceName.value = file.name.replace(/\.[^.]+$/, '')
  }
}

onMounted(() => {
  if (route.query.subject_id) subjectId.value = route.query.subject_id as string
  if (route.query.source_name) existingSourceName.value = route.query.source_name as string

  if (route.query.focus_topics) {
    focusTopics.value = (route.query.focus_topics as string).split(',')
    mode.value = 'focused'
    sourceId.value = route.query.source_id as string
    formData.value.quiz_name = `Practice: ${focusTopics.value.slice(0, 2).join(', ')}`
  } else if (route.query.source_id) {
    // Any time a source_id is provided (retake or new quiz from existing source),
    // skip the file upload — the source already exists.
    sourceId.value = route.query.source_id as string
    mode.value = 'full'
    if (route.query.mode === 'full') {
      formData.value.quiz_name = 'Full Quiz Retake'
    }
  }
})

const createQuiz = async () => {
  console.log('🚀 createQuiz called')
  console.log('Selected file:', selectedFile.value)
  console.log('Form data:', formData.value)
  console.log('Mode:', mode.value)

  // For normal mode, file is required
  if (mode.value === 'normal' && !selectedFile.value) {
    alert('Please select a file first')
    return
  }

  if (!formData.value.quiz_name.trim()) {
    alert('Please enter a quiz title')
    return
  }

  try {
    isCreating.value = true
    const config = useRuntimeConfig()
    console.log('📍 API Base:', config.public.apiBase)

    // Determine endpoint and prepare data based on mode
    const endpoint = mode.value === 'focused'
      ? '/quizzes/create-focused'
      : '/quizzes/create'

    const formDataToSend = new FormData()

    if (mode.value === 'focused') {
      // Focused quiz: use existing source with specific topics
      formDataToSend.append('source_id', sourceId.value!)
      formDataToSend.append('focus_topics', focusTopics.value.join(','))
    } else if (mode.value === 'full') {
      // Full retake: use existing source
      formDataToSend.append('source_id', sourceId.value!)
    } else {
      // Normal mode: upload new file
      formDataToSend.append('file', selectedFile.value!)
    }

    formDataToSend.append('quiz_name', formData.value.quiz_name)
    formDataToSend.append('quiz_type', formData.value.quiz_type)
    formDataToSend.append('num_questions', String(formData.value.num_questions))
    if (formData.value.time_limit) {
      formDataToSend.append('time_limit', String(formData.value.time_limit))
    }
    if (subjectId.value) {
      formDataToSend.append('subject_id', subjectId.value)
    }
    if (mode.value === 'normal' && sourceName.value.trim()) {
      formDataToSend.append('source_name', sourceName.value.trim())
    }

    console.log('📤 Sending request to:', `${config.public.apiBase}${endpoint}`)

    // Use fetch directly with proper headers
    const response = await fetch(`${config.public.apiBase}${endpoint}`, {
      method: 'POST',
      body: formDataToSend,
      credentials: 'include'
    })

    if (!response.ok) {
      if (response.status === 403) {
        showSubscriptionModal.value = true
        return
      }
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    const quiz = await response.json()

    console.log('✅ Success:', quiz)
    alert('Quiz created successfully!')
    await navigateTo(`/quiz/${quiz.id}`, { replace: true })
  } catch (error: any) {
    console.error('❌ Quiz creation failed:', error)
    console.error('Error details:', {
      message: error.message,
      data: error.data,
      statusCode: error.statusCode
    })
    alert(error?.data?.detail || error?.message || 'Failed to create quiz')
  } finally {
    isCreating.value = false
  }
}
</script>
