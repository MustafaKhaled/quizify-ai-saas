<script setup lang="ts">
const route = useRoute()
const quizId = route.params.id as string

definePageMeta({
  title: 'Take Quiz',
  description: 'Answer the quiz questions'
})

const { data: quiz } = await useFetch(`/api/quiz/${quizId}`, {
  lazy: true
})

const toast = useToast()
const loading = ref(false)
const timeRemaining = ref<number | null>(null)
const startTime = ref<number | null>(null)
const answers = ref<Record<number, number | number[]>>({})
const submitted = ref(false)
const result = ref<any>(null)

// Initialize timer if quiz has time limit
watch(quiz, (q) => {
  if (q?.time_limit && !startTime.value) {
    timeRemaining.value = q.time_limit * 60 // Convert to seconds
    startTime.value = Date.now()
    
    const interval = setInterval(() => {
      if (timeRemaining.value && startTime.value) {
        const elapsed = Math.floor((Date.now() - startTime.value) / 1000)
        timeRemaining.value = (q.time_limit * 60) - elapsed
        
        if (timeRemaining.value <= 0) {
          clearInterval(interval)
          submitQuiz()
        }
      }
    }, 1000)
  }
}, { immediate: true })

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

function selectAnswer(questionIndex: number, optionIndex: number, isMultiple: boolean) {
  if (submitted.value) return

  if (isMultiple) {
    if (!answers.value[questionIndex]) {
      answers.value[questionIndex] = []
    }
    const current = answers.value[questionIndex] as number[]
    const index = current.indexOf(optionIndex)
    if (index > -1) {
      current.splice(index, 1)
    } else {
      current.push(optionIndex)
    }
  } else {
    answers.value[questionIndex] = optionIndex
  }
}

function isSelected(questionIndex: number, optionIndex: number, isMultiple: boolean): boolean {
  if (isMultiple) {
    return (answers.value[questionIndex] as number[] || []).includes(optionIndex)
  }
  return answers.value[questionIndex] === optionIndex
}

async function submitQuiz() {
  if (submitted.value) return

  loading.value = true
  try {
    const timeTaken = startTime.value ? Math.floor((Date.now() - startTime.value) / 1000) : null

    const submission = {
      quiz_id: quizId,
      answers: Object.entries(answers.value).map(([index, selected]) => ({
        question_index: parseInt(index),
        selected_options: selected
      })),
      time_taken_seconds: timeTaken
    }

    result.value = await $fetch('/api/quiz/submit', {
      method: 'POST',
      body: submission
    })

    submitted.value = true
  } catch (err: any) {
    toast.add({
      title: 'Error',
      description: err?.data?.message || 'Failed to submit quiz',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}

const questions = computed(() => quiz.value?.content?.questions || [])
const isMultiple = computed(() => quiz.value?.quiz_type === 'multiple_select')
</script>

<template>
  <div v-if="!quiz" class="text-center py-12">
    <p class="text-gray-500">Loading quiz...</p>
  </div>

  <div v-else class="max-w-4xl mx-auto space-y-6">
    <!-- Quiz Header -->
    <UCard>
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold">{{ quiz.title }}</h1>
          <p class="text-gray-500 mt-1">
            {{ quiz.num_questions }} questions • {{ isMultiple ? 'Multiple Select' : 'Single Choice' }}
          </p>
        </div>
        <div v-if="timeRemaining !== null" class="text-right">
          <div class="text-sm text-gray-500">Time Remaining</div>
          <div class="text-2xl font-bold" :class="timeRemaining < 60 ? 'text-red-500' : ''">
            {{ formatTime(timeRemaining) }}
          </div>
        </div>
      </div>
    </UCard>

    <!-- Questions -->
    <div v-if="!submitted" class="space-y-6">
      <UCard
        v-for="(question, qIndex) in questions"
        :key="qIndex"
      >
        <template #header>
          <h3 class="text-lg font-semibold">
            Question {{ qIndex + 1 }}: {{ question.question_text }}
          </h3>
        </template>

        <div class="space-y-2">
          <div
            v-for="(option, oIndex) in question.options"
            :key="oIndex"
            :class="[
              'p-4 border rounded-lg cursor-pointer transition-colors',
              isSelected(qIndex, oIndex, isMultiple)
                ? 'border-primary bg-primary/10'
                : 'border-gray-200 dark:border-gray-700 hover:border-primary/50'
            ]"
            @click="selectAnswer(qIndex, oIndex, isMultiple)"
          >
            <div class="flex items-center gap-3">
              <input
                :type="isMultiple ? 'checkbox' : 'radio'"
                :checked="isSelected(qIndex, oIndex, isMultiple)"
                class="w-4 h-4"
                @change="selectAnswer(qIndex, oIndex, isMultiple)"
              />
              <span>{{ option }}</span>
            </div>
          </div>
        </div>
      </UCard>

      <!-- Submit Button -->
      <div class="flex justify-end">
        <UButton
          size="lg"
          :loading="loading"
          @click="submitQuiz"
        >
          Submit Quiz
        </UButton>
      </div>
    </div>

    <!-- Results -->
    <UCard v-if="submitted && result">
      <template #header>
        <h2 class="text-2xl font-bold">Quiz Results</h2>
      </template>

      <div class="text-center py-8">
        <div class="text-6xl font-bold mb-4" :class="result.is_passed ? 'text-green-500' : 'text-red-500'">
          {{ (result.score || result.score_percentage || 0).toFixed(1) }}%
        </div>
        <p class="text-xl mb-2">
          {{ result.is_passed ? 'Passed!' : 'Not Passed' }}
        </p>
        <p class="text-gray-500">
          You answered correctly on {{ (result.breakdown || []).filter((b: any) => b.is_correct).length || 0 }} out of {{ questions.length }} questions
        </p>
      </div>

      <!-- Detailed Breakdown -->
      <div class="mt-8 space-y-4">
        <h3 class="font-semibold text-lg">Question Review</h3>
        <div
          v-for="(item, index) in result.breakdown"
          :key="index"
          class="p-4 border rounded-lg"
          :class="item.is_correct ? 'border-green-200 bg-green-50 dark:bg-green-900/20' : 'border-red-200 bg-red-50 dark:bg-red-900/20'"
        >
          <div class="flex items-start gap-2 mb-2">
            <UIcon
              :name="item.is_correct ? 'i-lucide-check-circle' : 'i-lucide-x-circle'"
              :class="item.is_correct ? 'text-green-500' : 'text-red-500'"
              class="w-5 h-5 mt-0.5"
            />
            <div class="flex-1">
              <p class="font-medium">{{ questions[index]?.question_text }}</p>
              <p class="text-sm text-gray-500 mt-1">
                Your answer: {{ Array.isArray(item.user_choice) ? item.user_choice.join(', ') : item.user_choice }}
              </p>
              <p class="text-sm text-gray-500">
                Correct answer: {{ Array.isArray(item.correct_answer) ? item.correct_answer.join(', ') : item.correct_answer }}
              </p>
              <p v-if="item.explanation" class="text-sm mt-2">
                <strong>Explanation:</strong> {{ item.explanation }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <UButton to="/quizzes" variant="outline">
            Back to Quizzes
          </UButton>
          <UButton to="/">
            Go to Dashboard
          </UButton>
        </div>
      </template>
    </UCard>
  </div>
</template>
