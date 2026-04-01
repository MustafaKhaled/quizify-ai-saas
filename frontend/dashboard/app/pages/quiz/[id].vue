<template>
  <UDashboardPanel grow>
    <UDashboardPanelContent class="p-6 overflow-y-auto">
      <!-- Quiz Header -->
      <div v-if="quiz" class="mb-8 flex items-start justify-between gap-4">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-2">{{ quiz.title }}</h1>
          <p class="text-gray-600 dark:text-gray-400">Question {{ currentQuestionIndex + 1 }} of {{ totalQuestions }}</p>
        </div>

        <!-- Countdown Timer -->
        <div
          v-if="quiz.time_limit"
          class="flex-shrink-0 flex flex-col items-center justify-center rounded-xl px-5 py-3 min-w-[120px] text-center font-mono font-bold text-2xl shadow"
          :class="timerUrgent ? 'bg-red-100 dark:bg-red-900/40 text-red-600 dark:text-red-400 ring-2 ring-red-500 animate-pulse' : 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300'"
        >
          <span class="text-xs font-sans font-medium mb-1 opacity-70">Time left</span>
          {{ formattedTimeLeft }}
        </div>
      </div>

      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <div v-else-if="quiz && currentQuestion" class="space-y-6">
        <!-- Progress Bar -->
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div
            class="bg-blue-600 h-2 rounded-full transition-all"
            :style="{ width: `${totalQuestions ? ((currentQuestionIndex + 1) / totalQuestions) * 100 : 0}%` }"
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
              :class="isAnswerSelected(Number(idx)) ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : ''"
            >
              <input
                v-if="quiz.quiz_type === 'single_choice' || quiz.quiz_type === 'true_or_false'"
                type="radio"
                :name="`question-${currentQuestionIndex}`"
                :checked="isAnswerSelected(Number(idx))"
                @change="selectAnswer(Number(idx))"
                class="mr-3"
              />
              <input
                v-else
                type="checkbox"
                :checked="isAnswerSelected(Number(idx))"
                @change="toggleAnswer(Number(idx))"
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

// Always derive count from the actual questions array, not the stored num_questions
const totalQuestions = computed<number>(() => quiz.value?.content?.questions?.length ?? 0)

// Guard: prevent accidental navigation away mid-quiz
const quizDone = ref(false)
const LEAVE_MESSAGE = 'Leaving now will finish the quiz and your progress won\'t be recorded. Are you sure?'

const beforeUnloadHandler = (e: BeforeUnloadEvent) => {
  if (quizDone.value) return
  e.preventDefault()
  e.returnValue = LEAVE_MESSAGE
}

onBeforeRouteLeave(() => {
  if (quizDone.value) return true
  return window.confirm(LEAVE_MESSAGE)
})

// Timing
const startedAt = ref<Date | null>(null)
const timeLeftSeconds = ref(0)
let countdownInterval: ReturnType<typeof setInterval> | null = null

const timerUrgent = computed(() => timeLeftSeconds.value > 0 && timeLeftSeconds.value <= 60)

const formattedTimeLeft = computed(() => {
  const total = timeLeftSeconds.value
  const m = Math.floor(total / 60)
  const s = total % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})

const startTimer = (timeLimitMinutes: number) => {
  timeLeftSeconds.value = timeLimitMinutes * 60
  countdownInterval = setInterval(() => {
    timeLeftSeconds.value--
    if (timeLeftSeconds.value <= 0) {
      clearInterval(countdownInterval!)
      countdownInterval = null
      submitQuiz()
    }
  }, 1000)
}

const currentQuestion = computed(() => {
  if (!quiz.value?.content?.questions) return null
  return quiz.value.content.questions[currentQuestionIndex.value]
})

const isAnswerSelected = (optionIdx: number) => {
  const answer = userAnswers.value[currentQuestionIndex.value]
  if (quiz.value?.quiz_type === 'single_choice' || quiz.value?.quiz_type === 'true_or_false') {
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
  if (currentQuestionIndex.value < totalQuestions.value - 1) {
    currentQuestionIndex.value++
  }
}

const submitQuiz = async () => {
  if (isSubmitting.value) return
  try {
    quizDone.value = true
    isSubmitting.value = true

    if (countdownInterval) {
      clearInterval(countdownInterval)
      countdownInterval = null
    }

    const answersArray = Object.entries(userAnswers.value).map(([questionIndex, selectedOptions]) => ({
      question_index: parseInt(questionIndex),
      selected_options: selectedOptions
    }))

    const submission = {
      quiz_id: route.params.id,
      answers: answersArray,
      started_at: startedAt.value?.toISOString() ?? null
    }

    const response = await fetch(`${config.public.apiBase}/quizzes/submit/${route.params.id}`, {
      method: 'POST',
      body: JSON.stringify(submission),
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const result = await response.json()
    await navigateTo(`/results/${result.result_id}`)
  } catch (error) {
    console.error('Submit failed:', error)
    alert('Failed to submit quiz')
    quizDone.value = false
    isSubmitting.value = false
  }
}

onMounted(async () => {
  window.addEventListener('beforeunload', beforeUnloadHandler)

  try {
    const response = await fetch(`${config.public.apiBase}/quizzes/${route.params.id}`, {
      credentials: 'include'
    })

    if (response.ok) {
      const data = await response.json()
      quiz.value = Array.isArray(data) ? data[0] : data

      // Record start time and begin countdown after quiz loads
      startedAt.value = new Date()
      if (quiz.value?.time_limit) {
        startTimer(quiz.value.time_limit)
      }
    } else {
      console.error('Failed to load quiz:', response.status)
    }
  } catch (error) {
    console.error('Failed to load quiz:', error)
  } finally {
    isLoading.value = false
  }
})

onUnmounted(() => {
  window.removeEventListener('beforeunload', beforeUnloadHandler)
  if (countdownInterval) {
    clearInterval(countdownInterval)
  }
})
</script>
