<template>
  <UDashboardPanel grow>
    <UDashboardNavbar class="lg:hidden" title="Subject" />
    <UDashboardPanelContent class="p-4 sm:p-6 overflow-y-auto bg-mesh min-h-full">
      <div v-if="isLoading" class="flex items-center justify-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <template v-else-if="subject">
        <!-- ── Subject Header ─────────────────────────────── -->
        <div class="flex items-start justify-between mb-6 sm:mb-8 gap-3 flex-wrap">
          <div class="flex items-center gap-3 sm:gap-4 min-w-0">
            <NuxtLink to="/subjects" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors flex-shrink-0">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
            </NuxtLink>
            <div class="w-3 h-8 sm:w-4 sm:h-10 rounded-full flex-shrink-0" :style="{ backgroundColor: subject.color || '#3B82F6' }"></div>
            <div class="min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <h1 class="text-2xl sm:text-4xl font-bold gradient-text truncate">{{ subject.name }}</h1>
                <span v-if="isPMP" class="px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide rounded-full text-orange-700 dark:text-orange-300 bg-orange-500/10 border border-orange-500/20">Predefined</span>
              </div>
              <p class="text-slate-500 dark:text-slate-400 text-sm mt-1">
                <template v-if="isPMP">
                  {{ pmpChapters.length }} chapters • {{ allSourceQuizzes.length + subjectQuizzes.length }} {{ (allSourceQuizzes.length + subjectQuizzes.length) === 1 ? 'quiz' : 'quizzes' }}
                </template>
                <template v-else>
                  {{ sources.length }} {{ sources.length === 1 ? 'source' : 'sources' }} •
                  {{ allSourceQuizzes.length }} {{ allSourceQuizzes.length === 1 ? 'quiz' : 'quizzes' }}
                </template>
              </p>
            </div>
          </div>

          <div class="flex items-center gap-3 sm:gap-4 flex-wrap w-full sm:w-auto">
            <!-- Subject overall % -->
            <div v-if="subjectOverall !== null" class="text-center px-3 sm:px-4 py-1.5 sm:py-2 glass-card rounded-2xl">
              <p class="text-xs text-slate-500 dark:text-slate-400 mb-0.5">Overall</p>
              <span class="text-xl sm:text-2xl font-bold" :class="scoreColor(subjectOverall as number)">{{ subjectOverall }}%</span>
            </div>
            <div class="flex gap-2 flex-wrap">
              <template v-if="isPMP">
                <button
                  @click="guardAction(() => openPMPQuizModal())"
                  class="px-4 py-2 rounded-xl text-sm font-medium text-white transition-transform hover:-translate-y-0.5"
                  style="background: linear-gradient(135deg, #F97316, #FB923C); box-shadow: 0 8px 24px -8px rgba(249, 115, 22, 0.5)"
                >
                  <UIcon name="i-lucide-sparkles" class="w-4 h-4 inline-block mr-1" /> Generate PMP Quiz
                </button>
                <button
                  v-if="pmpWeakChapterSlugs.length > 0"
                  @click="guardAction(() => openPMPQuizModal(pmpWeakChapterSlugs))"
                  class="px-4 py-2 rounded-xl text-sm font-medium text-white bg-orange-600 hover:bg-orange-700 transition-colors"
                >
                  🎯 Practice Weak Chapters
                </button>
              </template>
              <template v-else>
                <button
                  @click="guardAction(() => navigateTo(`/quiz-new?subject_id=${subject.id}`))"
                  class="px-4 py-2 btn-gradient rounded-xl transition-colors text-sm font-medium"
                >
                  + Upload Source
                </button>
                <button
                  @click="guardAction(() => { showSubjectQuizModal = true })"
                  :disabled="sources.length === 0"
                  class="px-4 py-2 bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 shadow-lg shadow-purple-500/20 rounded-xl text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium"
                >
                  <UIcon name="i-lucide-sparkles" class="w-4 h-4 inline-block mr-1" /> Subject Quiz
                </button>
              </template>
              <button
                v-if="!isPMP"
                @click="confirmDelete"
                class="px-4 py-2 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/40 transition-colors text-sm"
              >
                Delete
              </button>
            </div>
          </div>
        </div>

        <!-- ── PMP Chapters Grid ──────────────────────────── -->
        <div v-if="isPMP && pmpChapters.length > 0" class="mb-8">
          <h2 class="text-lg font-bold text-gray-900 dark:text-white mb-3">PMBOK Chapters</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <div
              v-for="ch in pmpChapters"
              :key="ch.slug"
              class="glass-card rounded-2xl p-4 flex flex-col gap-3"
              :class="{ 'ring-2 ring-orange-500/40': pmpChapterStats[ch.name] && pmpChapterStats[ch.name].accuracy < 70 }"
            >
              <div class="flex items-start justify-between gap-2">
                <h3 class="font-semibold text-slate-900 dark:text-white text-sm leading-snug">{{ ch.name }}</h3>
                <span
                  v-if="pmpChapterStats[ch.name]"
                  class="px-2 py-0.5 rounded-full text-xs font-bold flex-shrink-0"
                  :class="scoreBadge(pmpChapterStats[ch.name].accuracy)"
                >{{ pmpChapterStats[ch.name].accuracy }}%</span>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 line-clamp-2 flex-1">{{ ch.summary }}</p>
              <button
                type="button"
                @click="guardAction(() => openPMPQuizModal([ch.slug]))"
                class="px-3 py-1.5 rounded-lg text-xs font-semibold text-white self-start transition-transform hover:-translate-y-0.5"
                style="background: linear-gradient(135deg, #F97316, #FB923C)"
              >
                Quiz this chapter
              </button>
            </div>
          </div>
        </div>

        <!-- ── Subject-Wide Quizzes ─────────────────────── -->
        <div v-if="subjectQuizzes.length > 0" class="mb-8">
          <h2 class="text-lg font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
            <span class="text-purple-500">✨</span> Subject-Wide Quizzes
          </h2>
          <div class="space-y-2">
            <div
              v-for="quiz in subjectQuizzes"
              :key="quiz.id"
              class="flex items-center justify-between p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-purple-100 dark:border-purple-900/30 hover:bg-purple-50 dark:hover:bg-purple-900/10 cursor-pointer transition-colors group"
              @click="quiz.latest_result_id ? navigateTo(`/results/${quiz.latest_result_id}`) : guardAction(() => navigateTo(`/quiz/${quiz.id}`))"
            >
              <div>
                <p class="font-semibold text-gray-900 dark:text-white">{{ quiz.title }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  {{ quiz.num_questions }} questions • {{ quizTypeLabel(quiz.quiz_type) }}
                </p>
              </div>
              <div class="flex items-center gap-3 flex-shrink-0">
                <span
                  v-if="quizLatestScore(quiz) !== null"
                  class="px-2.5 py-0.5 rounded-full text-sm font-bold"
                  :class="scoreBadge(quizLatestScore(quiz)!)"
                >{{ quizLatestScore(quiz) }}%</span>
                <span v-else class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-400 dark:text-gray-500">
                  Not taken
                </span>
                <span class="text-blue-500 text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                  {{ quiz.latest_result_id ? 'Review →' : 'Take →' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- ── No sources empty state ─────────────────────── -->
        <div v-if="!isPMP && sources.length === 0" class="text-center py-16 bg-white dark:bg-gray-800 rounded-xl shadow">
          <div class="text-5xl mb-3">📄</div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-2">No sources yet</h2>
          <p class="text-gray-600 dark:text-gray-400 mb-5">Upload your first PDF to start generating quizzes</p>
          <NuxtLink :to="`/quiz-new?subject_id=${subject.id}`">
            <button class="px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium">
              Upload PDF
            </button>
          </NuxtLink>
        </div>

        <!-- ── Sources ────────────────────────────────────── -->
        <div v-else-if="!isPMP" class="space-y-6">
          <div
            v-for="source in sources"
            :key="source.id"
            class="bg-white dark:bg-gray-800 rounded-xl shadow overflow-hidden"
          >
            <!-- Source header -->
            <div class="px-5 py-4 border-b border-gray-100 dark:border-gray-700">
              <div class="flex items-center justify-between gap-4 flex-wrap">
                <div class="flex items-center gap-3 min-w-0">
                  <svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zm4 18H6V4h7v5h5v11z"/>
                  </svg>
                  <div class="min-w-0">
                    <p class="font-semibold text-gray-900 dark:text-white truncate">{{ source.name || source.file_name }}</p>
                    <p class="text-xs text-gray-400 dark:text-gray-500 truncate">
                      {{ source.file_name }} • Uploaded {{ new Date(source.upload_date).toLocaleDateString() }}
                    </p>
                  </div>
                </div>

                <div class="flex items-center gap-3 flex-shrink-0">
                  <!-- Avg score -->
                  <div class="text-right min-w-[60px]">
                    <p class="text-xs text-gray-400 dark:text-gray-500 mb-0.5">Avg Score</p>
                    <span v-if="sourceAverage(source.id) !== null" class="text-lg font-bold" :class="scoreColor(sourceAverage(source.id)!)">
                      {{ sourceAverage(source.id) }}%
                    </span>
                    <span v-else class="text-lg font-bold text-gray-300 dark:text-gray-600">—</span>
                  </div>
                  <!-- Actions -->
                  <div class="flex gap-2">
                    <button
                      @click="guardAction(() => navigateTo(`/quiz-new?subject_id=${subject.id}&source_id=${source.id}&source_name=${encodeURIComponent(source.name || source.file_name)}`))"
                      class="px-3 py-1.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium whitespace-nowrap"
                    >
                      + New Quiz
                    </button>
                    <button
                      v-if="sourceWeakTopics(source.id).length > 0"
                      @click="guardAction(() => navigateTo(`/quiz-new?subject_id=${subject.id}&source_id=${source.id}&source_name=${encodeURIComponent(source.name || source.file_name)}&focus_topics=${sourceWeakTopics(source.id).join(',')}`))"
                      class="px-3 py-1.5 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors text-sm font-medium whitespace-nowrap"
                    >
                      🎯 Practice Weak Areas
                    </button>
                    <button
                      @click="deleteSource(source.id)"
                      class="px-3 py-1.5 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-100 transition-colors text-sm whitespace-nowrap"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Weak topics row -->
            <div v-if="sourceWeakTopics(source.id).length > 0" class="px-5 py-2.5 bg-orange-50 dark:bg-orange-900/10 border-b border-orange-100 dark:border-orange-900/20 flex flex-wrap gap-2 items-center">
              <span class="text-xs font-semibold text-orange-600 dark:text-orange-400 mr-1">Weak areas:</span>
              <span
                v-for="topic in sourceWeakTopics(source.id)"
                :key="topic"
                class="px-2 py-0.5 bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 rounded-full text-xs font-medium"
              >
                {{ topic }}
              </span>
            </div>

            <!-- Quiz rows -->
            <div v-if="quizzesForSource(source.id).length > 0" class="divide-y divide-gray-100 dark:divide-gray-700/50">
              <div
                v-for="quiz in quizzesForSource(source.id)"
                :key="quiz.id"
                class="flex items-center justify-between px-5 py-3 hover:bg-gray-50 dark:hover:bg-gray-700/40 cursor-pointer transition-colors group"
                @click="quiz.latest_result_id ? navigateTo(`/results/${quiz.latest_result_id}`) : guardAction(() => navigateTo(`/quiz/${quiz.id}`))"
              >
                <div class="min-w-0 mr-4">
                  <p class="font-medium text-gray-900 dark:text-white truncate">{{ quiz.title }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">
                    {{ quiz.num_questions }} questions • {{ quizTypeLabel(quiz.quiz_type) }}
                    <span v-if="quiz.time_limit"> • {{ quiz.time_limit }} min</span>
                  </p>
                </div>
                <div class="flex items-center gap-3 flex-shrink-0">
                  <span
                    v-if="quizLatestScore(quiz) !== null"
                    class="px-2.5 py-0.5 rounded-full text-sm font-bold"
                    :class="scoreBadge(quizLatestScore(quiz)!)"
                  >{{ quizLatestScore(quiz) }}%</span>
                  <span v-else class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-400 dark:text-gray-500">
                    Not taken
                  </span>
                  <span class="text-blue-500 text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                    {{ quiz.latest_result_id ? 'Review →' : 'Take →' }}
                  </span>
                </div>
              </div>
            </div>

            <div v-else class="px-5 py-4 text-sm text-gray-400 dark:text-gray-500 italic">
              No quizzes yet — click "+ New Quiz" to generate one from this source.
            </div>
          </div>
        </div>
      </template>

      <!-- ── PMP Quiz Modal ───────────────────────────────── -->
      <div
        v-if="showPMPQuizModal"
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
        @click.self="showPMPQuizModal = false"
      >
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-md p-6">
          <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-1">Generate PMP Quiz</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-5">
            <template v-if="pmpQuizForm.focus_chapters.length > 0">
              Focused on {{ pmpQuizForm.focus_chapters.length }} {{ pmpQuizForm.focus_chapters.length === 1 ? 'chapter' : 'chapters' }}.
            </template>
            <template v-else>
              Covers all {{ pmpChapters.length }} PMBOK knowledge areas (questions distributed evenly).
            </template>
          </p>
          <form @submit.prevent="createPMPQuiz" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-900 dark:text-white mb-1">Quiz Title</label>
              <input v-model="pmpQuizForm.quiz_name" type="text" placeholder="PMP — Practice Quiz"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-900 dark:text-white mb-1">Question Type</label>
              <select v-model="pmpQuizForm.quiz_type"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm">
                <option value="single_choice">Multiple Choice</option>
                <option value="multiple_select">Multiple Select</option>
                <option value="true_or_false">True or False</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-900 dark:text-white mb-1">
                Number of Questions
                <span class="text-xs text-gray-500 dark:text-gray-400 ml-1 font-normal">
                  (max {{ pmpMaxQuestions }})
                </span>
              </label>
              <input v-model.number="pmpQuizForm.num_questions" type="number" min="1" :max="pmpMaxQuestions"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm"/>
              <p v-if="pmpQuizForm.focus_chapters.length === 0" class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Full coverage uses chunked generation across all chapters — slightly slower, no truncation.
              </p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-900 dark:text-white mb-1">Time Limit (minutes, optional)</label>
              <input v-model.number="pmpQuizForm.time_limit" type="number" min="1" placeholder="Leave empty for unlimited"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm"/>
            </div>
            <div v-if="pmpQuizForm.focus_chapters.length > 0" class="flex flex-wrap gap-2 pt-1">
              <span
                v-for="slug in pmpQuizForm.focus_chapters"
                :key="slug"
                class="px-2 py-0.5 bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 rounded-full text-xs font-medium"
              >
                {{ pmpChapters.find(c => c.slug === slug)?.name || slug }}
              </span>
            </div>
            <div class="flex gap-3 pt-2">
              <button type="button" @click="showPMPQuizModal = false"
                class="flex-1 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm">
                Cancel
              </button>
              <button type="submit" :disabled="isGenerating"
                class="flex-1 py-2 rounded-lg text-white font-medium text-sm disabled:opacity-50"
                style="background: linear-gradient(135deg, #F97316, #FB923C)">
                {{ isGenerating ? 'Generating...' : 'Generate Quiz' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- ── Subject-Wide Quiz Modal ──────────────────────── -->
      <div
        v-if="showSubjectQuizModal"
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
        @click.self="showSubjectQuizModal = false"
      >
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-md p-6">
          <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Generate Subject-Wide Quiz</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-5">
            Covers all {{ sources.length }} sources in <strong>{{ subject?.name }}</strong>.
          </p>
          <form @submit.prevent="createSubjectQuiz" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-900 dark:text-white mb-1">Quiz Title</label>
              <input v-model="subjectQuizForm.quiz_name" type="text" :placeholder="`${subject?.name} — Full Subject Quiz`"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-900 dark:text-white mb-1">Question Type</label>
              <select v-model="subjectQuizForm.quiz_type"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
                <option value="single_choice">Multiple Choice</option>
                <option value="multiple_select">Multiple Select</option>
                <option value="true_or_false">True or False</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-900 dark:text-white mb-1">Number of Questions</label>
              <input v-model.number="subjectQuizForm.num_questions" type="number" min="1" max="30"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"/>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-900 dark:text-white mb-1">Time Limit (minutes, optional)</label>
              <input v-model.number="subjectQuizForm.time_limit" type="number" min="1" placeholder="Leave empty for unlimited"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"/>
            </div>
            <div class="flex gap-3 pt-2">
              <button type="button" @click="showSubjectQuizModal = false"
                class="flex-1 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm">
                Cancel
              </button>
              <button type="submit" :disabled="isGenerating"
                class="flex-1 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors text-sm font-medium">
                {{ isGenerating ? 'Generating...' : 'Generate Quiz' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </UDashboardPanelContent>

    <SubscriptionModal v-model="showSubscriptionModal" />
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })

const route = useRoute()
const config = useRuntimeConfig()

const subject = ref<any>(null)
const sources = ref<any[]>([])
const quizzes = ref<any[]>([])
const myResults = ref<any[]>([])
const isLoading = ref(true)
const showSubjectQuizModal = ref(false)
const showPMPQuizModal = ref(false)
const showSubscriptionModal = ref(false)
const isGenerating = ref(false)

type PMPChapter = { slug: string; name: string; summary: string }
const pmpChapters = ref<PMPChapter[]>([])

const isPMP = computed(() => subject.value?.name === 'PMP')

const PMP_MAX_FOCUSED = 30
const PMP_MAX_FULL = 60

const pmpQuizForm = ref({
  quiz_name: '',
  quiz_type: 'single_choice',
  num_questions: 10,
  time_limit: null as number | null,
  focus_chapters: [] as string[],
})

const pmpMaxQuestions = computed(() =>
  pmpQuizForm.value.focus_chapters.length > 0 ? PMP_MAX_FOCUSED : PMP_MAX_FULL
)

const { isEligible, fetchUser } = useSubscription()

function guardAction(action: () => void) {
  if (isEligible.value) {
    action()
  } else {
    showSubscriptionModal.value = true
  }
}

const subjectQuizForm = ref({
  quiz_name: '',
  quiz_type: 'single_choice',
  num_questions: 10,
  time_limit: null as number | null,
})

const subjectQuizzes = computed(() =>
  quizzes.value.filter(q => !q.source_id)
)

const allSourceQuizzes = computed(() =>
  quizzes.value.filter(q => q.source_id)
)

const quizzesForSource = (sourceId: string) =>
  quizzes.value.filter(q => q.source_id === sourceId)

const quizTypeLabel = (type: string) => {
  if (type === 'multiple_select') return 'Multiple Select'
  if (type === 'true_or_false') return 'True or False'
  return 'Multiple Choice'
}

// Latest score comes directly from the quiz object (set by the backend)
const quizLatestScore = (quiz: any): number | null => {
  if (quiz.latest_score === null || quiz.latest_score === undefined) return null
  return Math.round(Number(quiz.latest_score))
}

// Average score across all quizzes for a source
const sourceAverage = (sourceId: string): number | null => {
  const sourceQuizzes = quizzesForSource(sourceId)
  const scores = sourceQuizzes
    .map(q => quizLatestScore(q))
    .filter(s => s !== null) as number[]
  if (!scores.length) return null
  return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length)
}

// Subject overall: average of all source averages (or all subject quizzes for PMP)
const subjectOverall = computed<number | null>(() => {
  if (isPMP.value) {
    const scores = quizzes.value
      .map((q: any) => quizLatestScore(q))
      .filter((s): s is number => s !== null)
    if (!scores.length) return null
    return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length)
  }
  const avgs: number[] = sources.value
    .map((s: any) => sourceAverage(s.id))
    .filter((s): s is number => s !== null)
  if (!avgs.length) return null
  return Math.round(avgs.reduce((a, b) => a + b, 0) / avgs.length)
})

// Per-chapter accuracy for PMP, derived from all quiz attempts in this subject
const pmpChapterStats = computed<Record<string, { total: number; correct: number; accuracy: number }>>(() => {
  if (!isPMP.value) return {}
  const subjectQuizIds = new Set(quizzes.value.map((q: any) => q.id))
  const stats: Record<string, { total: number; correct: number }> = {}
  for (const result of myResults.value) {
    if (!subjectQuizIds.has(result.quiz_id)) continue
    for (const ans of (result.user_answers || [])) {
      const topic: string = ans.topic || 'Unknown'
      if (!stats[topic]) stats[topic] = { total: 0, correct: 0 }
      stats[topic].total++
      if (ans.is_correct) stats[topic].correct++
    }
  }
  const out: Record<string, { total: number; correct: number; accuracy: number }> = {}
  for (const [topic, s] of Object.entries(stats)) {
    out[topic] = { ...s, accuracy: Math.round((s.correct / s.total) * 100) }
  }
  return out
})

const pmpWeakChapterSlugs = computed<string[]>(() => {
  if (!isPMP.value) return []
  const stats = pmpChapterStats.value
  return pmpChapters.value
    .filter(ch => stats[ch.name] && stats[ch.name].total >= 1 && stats[ch.name].accuracy < 70)
    .sort((a, b) => stats[a.name].accuracy - stats[b.name].accuracy)
    .map(ch => ch.slug)
})

// Weak topics for a source: topics with < 70% accuracy across all quiz attempts
const sourceWeakTopics = (sourceId: string): string[] => {
  const sourceQuizIds = new Set(quizzesForSource(sourceId).map((q: any) => q.id))
  const stats: Record<string, { total: number; correct: number }> = {}
  for (const result of myResults.value) {
    if (!sourceQuizIds.has(result.quiz_id)) continue
    for (const answer of (result.user_answers || [])) {
      const topic: string = answer.topic || 'Unknown'
      if (!stats[topic]) stats[topic] = { total: 0, correct: 0 }
      stats[topic].total++
      if (answer.is_correct) stats[topic].correct++
    }
  }
  return Object.entries(stats)
    .filter(([, s]) => s.total >= 1 && s.correct / s.total < 0.7)
    .sort((a, b) => (a[1].correct / a[1].total) - (b[1].correct / b[1].total))
    .map(([topic]) => topic)
}

const scoreColor = (score: number) => {
  if (score >= 70) return 'text-green-600 dark:text-green-400'
  if (score >= 50) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-red-600 dark:text-red-400'
}

const scoreBadge = (score: number) => {
  if (score >= 70) return 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300'
  if (score >= 50) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300'
  return 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
}

const loadData = async () => {
  const api = config.public.apiBase
  const id = route.params.id as string
  isLoading.value = true
  try {
    const [subjectRes, sourcesRes, quizzesRes, resultsRes] = await Promise.allSettled([
      fetch(`${api}/subjects/${id}`, { credentials: 'include' }),
      fetch(`${api}/subjects/${id}/sources`, { credentials: 'include' }),
      fetch(`${api}/subjects/${id}/quizzes`, { credentials: 'include' }),
      fetch(`${api}/quizzes/my_results`, { credentials: 'include' }),
    ])
    if (subjectRes.status === 'fulfilled' && subjectRes.value.ok) subject.value = await subjectRes.value.json()
    if (sourcesRes.status === 'fulfilled' && sourcesRes.value.ok) sources.value = await sourcesRes.value.json()
    if (quizzesRes.status === 'fulfilled' && quizzesRes.value.ok) quizzes.value = await quizzesRes.value.json()
    if (resultsRes.status === 'fulfilled' && resultsRes.value.ok) myResults.value = await resultsRes.value.json()
  } catch (e) {
    console.error('Failed to load subject data:', e)
  } finally {
    isLoading.value = false
  }
}

const deleteSource = async (sourceId: string) => {
  if (!confirm('Delete this source and all its quizzes?')) return
  const res = await fetch(`${config.public.apiBase}/quizzes/sources/${sourceId}`, {
    method: 'DELETE',
    credentials: 'include',
  })
  if (res.ok || res.status === 204) await loadData()
  else alert('Failed to delete source')
}

const confirmDelete = async () => {
  if (!confirm(`Delete subject "${subject.value?.name}"? Sources will be unassigned, not deleted.`)) return
  const res = await fetch(`${config.public.apiBase}/subjects/${route.params.id}`, {
    method: 'DELETE',
    credentials: 'include',
  })
  if (res.ok || res.status === 204) await navigateTo('/subjects', { replace: true })
  else alert('Failed to delete subject')
}

const openPMPQuizModal = (focusSlugs: string[] = []) => {
  pmpQuizForm.value = {
    quiz_name: '',
    quiz_type: 'single_choice',
    num_questions: 10,
    time_limit: null,
    focus_chapters: [...focusSlugs],
  }
  showPMPQuizModal.value = true
}

const createPMPQuiz = async () => {
  pmpQuizForm.value.num_questions = Math.min(
    Math.max(Number(pmpQuizForm.value.num_questions) || 1, 1),
    pmpMaxQuestions.value,
  )
  isGenerating.value = true
  try {
    const body: Record<string, any> = {
      quiz_type: pmpQuizForm.value.quiz_type,
      num_questions: pmpQuizForm.value.num_questions,
    }
    if (pmpQuizForm.value.quiz_name) body.quiz_name = pmpQuizForm.value.quiz_name
    if (pmpQuizForm.value.time_limit) body.time_limit = pmpQuizForm.value.time_limit
    if (pmpQuizForm.value.focus_chapters.length > 0) body.focus_chapters = pmpQuizForm.value.focus_chapters

    const res = await fetch(`${config.public.apiBase}/predefined/pmp/quiz`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    if (!res.ok) {
      if (res.status === 403) {
        showPMPQuizModal.value = false
        showSubscriptionModal.value = true
        return
      }
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `HTTP ${res.status}`)
    }
    const quiz = await res.json()
    showPMPQuizModal.value = false
    await navigateTo(`/quiz/${quiz.id}`, { replace: true })
  } catch (e: any) {
    alert(e?.message || 'Failed to generate PMP quiz')
  } finally {
    isGenerating.value = false
  }
}

const createSubjectQuiz = async () => {
  isGenerating.value = true
  try {
    const formData = new FormData()
    formData.append('quiz_type', subjectQuizForm.value.quiz_type)
    formData.append('num_questions', String(subjectQuizForm.value.num_questions))
    if (subjectQuizForm.value.quiz_name) formData.append('quiz_name', subjectQuizForm.value.quiz_name)
    if (subjectQuizForm.value.time_limit) formData.append('time_limit', String(subjectQuizForm.value.time_limit))

    const res = await fetch(`${config.public.apiBase}/subjects/${route.params.id}/quiz`, {
      method: 'POST',
      credentials: 'include',
      body: formData,
    })
    if (!res.ok) {
      if (res.status === 403) {
        showSubjectQuizModal.value = false
        showSubscriptionModal.value = true
        return
      }
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `HTTP ${res.status}`)
    }
    const quiz = await res.json()
    showSubjectQuizModal.value = false
    await navigateTo(`/quiz/${quiz.id}`, { replace: true })
  } catch (e: any) {
    alert(e?.message || 'Failed to generate subject quiz')
  } finally {
    isGenerating.value = false
  }
}

onMounted(async () => {
  fetchUser()
  await loadData()
  if (isPMP.value) {
    try {
      const res = await fetch(`${config.public.apiBase}/predefined/pmp/chapters`, { credentials: 'include' })
      if (res.ok) pmpChapters.value = await res.json()
    } catch (e) {
      console.error('Failed to load PMP chapters:', e)
    }
    const focus = route.query.focus_chapter
    if (typeof focus === 'string' && focus) {
      openPMPQuizModal([focus])
    }
  }
})
</script>
