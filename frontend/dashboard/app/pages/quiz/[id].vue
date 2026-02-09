<template>
  <UDashboardPanel grow>
    <UDashboardPanelContent class="p-6 overflow-y-auto">
      <!-- Quiz Header -->
      <div v-if="quiz" class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-2">{{ quiz.title }}</h1>
        <p class="text-gray-600 dark:text-gray-400">Question {{ currentQuestionIndex + 1 }} of {{ quiz.num_questions }}</p>
      </div>

      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <div v-else-if="quiz && currentQuestion" class="space-y-6">
        <!-- Progress Bar -->
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div
            class="bg-blue-600 h-2 rounded-full transition-all"
            :style="{ width: `${((currentQuestionIndex + 1) / quiz.num_questions) * 100}%` }"
          ></div>
        </div>

        <!-- Question Card -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-8">
          <h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-6">{{ currentQuestion.question_text }}</h2>

          <!-- Answer Options -->
          <div class="space-y-3 mb-8">
            <label
              v-for="(option, idx) of currentQuestion.options"
              :key="idx"
              class="flex items-center p-4 border-2 border-gray-200 dark:border-gray-600 rounded-lg hover:border-blue-500 dark:hover:border-blue-400 cursor-pointer transition-colors"
              :class="isAnswerSelected(idx) ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : ''"
            >
              <input
                v-if="quiz.quiz_type === 'single_choice'"
                type="radio"
                :name="`question-${currentQuestionIndex}`"
                :checked="isAnswerSelected(idx)"
                @change="selectAnswer(idx)"
                class="mr-3"
              />
              <input
                v-else
                type="checkbox"
                :checked="isAnswerSelected(idx)"
                @change="toggleAnswer(idx)"
                class="mr-3"
              />
              <span class="text-gray-900 dark:text-white">{{ option }}</span>
            </label>
          </div>

          <!-- Navigation Buttons -->
          <div class="flex justify-between items-center">
            <button
              @click="previousQuestion"
              :disabled="currentQuestionIndex === 0"
              class="px-6 py-2 bg-gray-300 dark:bg-gray-600 text-gray-900 dark:text-white rounded-lg disabled:opacity-50 transition-colors"
            >
              ← Previous
            </button>

            <div class="flex gap-2">
              <button
                v-if="currentQuestionIndex < quiz.num_questions - 1"
                @click="nextQuestion"
                class="px-6 py-2 bg-gray-300 dark:bg-gray-600 text-gray-900 dark:text-white rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors"
              >
                Next →
              </button>
              <button
                v-else
                @click="submitQuiz"
                :disabled="isSubmitting"
                class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
              >
                {{ isSubmitting ? 'Submitting...' : 'Submit Quiz' }}
              </button>
            </div>

            <div class="text-sm text-gray-600 dark:text-gray-400">
              {{ Object.keys(userAnswers).length }} of {{ quiz.num_questions }} answered
            </div>
          </div>
        </div>
      </div>
    </UDashboardPanelContent>
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const route = useRoute()
const config = useRuntimeConfig()

const quiz = ref<any>(null)
const isLoading = ref(true)
const isSubmitting = ref(false)
const currentQuestionIndex = ref(0)
const userAnswers = ref<Record<number, number | number[]>>({})

const getToken = () => typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null

const currentQuestion = computed(() => {
  if (!quiz.value?.content?.questions) return null
  return quiz.value.content.questions[currentQuestionIndex.value]
})

const isAnswerSelected = (optionIdx: number) => {
  const answer = userAnswers.value[currentQuestionIndex.value]
  if (quiz.value?.quiz_type === 'single_choice') {
    return answer === optionIdx
  } else {
    return Array.isArray(answer) && answer.includes(optionIdx)
  }
}

const selectAnswer = (optionIdx: number) => {
  userAnswers.value[currentQuestionIndex.value] = optionIdx
}

const toggleAnswer = (optionIdx: number) => {
  const answer = userAnswers.value[currentQuestionIndex.value] as number[] || []
  if (!Array.isArray(answer)) {
    userAnswers.value[currentQuestionIndex.value] = [optionIdx]
  } else {
    const idx = answer.indexOf(optionIdx)
    if (idx > -1) {
      answer.splice(idx, 1)
    } else {
      answer.push(optionIdx)
    }
    userAnswers.value[currentQuestionIndex.value] = answer
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < (quiz.value?.num_questions || 0) - 1) {
    currentQuestionIndex.value++
  }
}

const submitQuiz = async () => {
  try {
    isSubmitting.value = true
    const token = getToken()

    // Transform answers from Record<number, number | number[]> to AnswerSubmission[]
    const answersArray = Object.entries(userAnswers.value).map(([questionIndex, selectedOptions]) => ({
      question_index: parseInt(questionIndex),
      selected_options: selectedOptions
    }))

    const submission = {
      quiz_id: route.params.id,
      answers: answersArray,
      time_taken_seconds: null
    }

    const response = await fetch(`${config.public.apiBase}/quizzes/submit/${route.params.id}`, {
      method: 'POST',
      body: JSON.stringify(submission),
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
      }
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const result = await response.json()
    await navigateTo(`/results/${result.result_id}`)
  } catch (error) {
    console.error('Submit failed:', error)
    alert('Failed to submit quiz')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(async () => {
  try {
    const token = getToken()
    const response = await fetch(`${config.public.apiBase}/quizzes/${route.params.id}`, {
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      }
    })

    if (response.ok) {
      const data = await response.json()
      // Backend returns an array, get the first element
      quiz.value = Array.isArray(data) ? data[0] : data
    } else {
      console.error('Failed to load quiz:', response.status)
    }
  } catch (error) {
    console.error('Failed to load quiz:', error)
  } finally {
    isLoading.value = false
  }
})
</script>
