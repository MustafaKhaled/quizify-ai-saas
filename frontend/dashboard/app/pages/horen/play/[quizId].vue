<template>
  <UDashboardPanel grow>
    <UDashboardNavbar class="lg:hidden" :title="quiz?.title || 'Hören'" />
    <UDashboardPanelContent class="p-4 sm:p-6 overflow-y-auto bg-mesh min-h-full">

      <div v-if="loading" class="text-center py-16">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emerald-500 mx-auto mb-4"></div>
        <p class="text-sm text-slate-500 dark:text-slate-400">Lädt…</p>
      </div>

      <div v-else-if="error" class="text-center py-16">
        <p class="text-red-600 dark:text-red-400 font-medium mb-3">{{ error }}</p>
        <NuxtLink to="/horen/deutsch_b1_horen" class="text-sm gradient-text font-medium hover:opacity-80">
          ← Zurück zur Übersicht
        </NuxtLink>
      </div>

      <!-- RUNNER: walk through one Teil at a time -->
      <div v-else-if="mode === 'play' && currentTeil">
        <div class="mb-6 flex items-start justify-between flex-wrap gap-2">
          <div>
            <NuxtLink
              to="/horen/deutsch_b1_horen"
              class="text-xs text-slate-500 dark:text-slate-400 hover:underline mb-2 inline-flex items-center gap-1"
            >
              <UIcon name="i-lucide-arrow-left" class="w-3 h-3" /> Übersicht
            </NuxtLink>
            <h1 class="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white">
              {{ currentTeil.teil_name }}
            </h1>
          </div>
          <div class="flex items-center gap-2">
            <span
              v-for="(t, idx) in teile"
              :key="t.teil"
              class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold transition"
              :class="idx === currentTeilIndex
                ? 'bg-emerald-600 text-white'
                : (idx < currentTeilIndex
                    ? 'bg-emerald-500/20 text-emerald-700 dark:text-emerald-300'
                    : 'bg-slate-200 dark:bg-slate-700 text-slate-500')"
            >
              {{ t.teil }}
            </span>
          </div>
        </div>

        <div class="glass-card rounded-2xl p-4 mb-6 text-sm text-slate-700 dark:text-slate-300">
          {{ currentTeil.instructions }}
        </div>

        <!-- One card per audio segment, all that segment's questions visible at once -->
        <div
          v-for="group in currentTeilGroups"
          :key="group.audio_url"
          class="glass-card rounded-2xl p-6 mb-6"
        >
          <p v-if="group.audio_context" class="text-xs uppercase tracking-wide font-semibold text-slate-500 dark:text-slate-400 mb-3">
            {{ group.audio_context }}
          </p>

          <!-- Audio player for this segment -->
          <div class="bg-slate-100 dark:bg-slate-800 rounded-xl p-4 mb-6 flex items-center gap-4">
            <button
              type="button"
              @click="playAudio(group.audio_url)"
              :disabled="playsForAudio(group.audio_url) >= currentTeil.play_limit || playingAudio === group.audio_url"
              class="w-12 h-12 rounded-full text-white flex items-center justify-center disabled:opacity-50 transition bg-emerald-700"
            >
              <UIcon
                :name="playingAudio === group.audio_url ? 'i-lucide-pause' : 'i-lucide-play'"
                class="w-6 h-6"
              />
            </button>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-slate-900 dark:text-white">
                <template v-if="playingAudio === group.audio_url">Wird abgespielt…</template>
                <template v-else-if="playsForAudio(group.audio_url) >= currentTeil.play_limit">Wiedergabe beendet</template>
                <template v-else-if="playsForAudio(group.audio_url) === 0">Klicken zum Abspielen</template>
                <template v-else>Erneut abspielen ({{ currentTeil.play_limit - playsForAudio(group.audio_url) }} verbleibend)</template>
              </p>
              <p class="text-xs text-slate-500 dark:text-slate-400">
                Wiedergabe {{ playsForAudio(group.audio_url) }} von {{ currentTeil.play_limit }}
              </p>
            </div>
          </div>

          <!-- All questions for this audio -->
          <div class="space-y-6">
            <div v-for="(q, qi) in group.questions" :key="`${group.audio_url}-${qi}`" class="border-t border-slate-200 dark:border-slate-700 pt-4 first:border-t-0 first:pt-0">
              <p class="font-semibold text-sm text-slate-900 dark:text-white mb-3">
                <span class="text-emerald-700 dark:text-emerald-300 mr-1">{{ q.globalIndex + 1 }}.</span>
                {{ q.stem }}
              </p>
              <div class="space-y-2">
                <label
                  v-for="(opt, oi) in q.options"
                  :key="oi"
                  class="block p-3 rounded-xl border cursor-pointer transition text-sm"
                  :class="optionClass(q, oi)"
                >
                  <input
                    type="radio"
                    :value="oi"
                    :checked="answers[q.globalIndex] === oi"
                    @change="answers[q.globalIndex] = oi"
                    :disabled="teilSubmitted[currentTeilIndex]"
                    class="mr-3 align-middle"
                  />
                  <span class="align-middle">{{ opt }}</span>
                </label>
              </div>
              <div
                v-if="teilSubmitted[currentTeilIndex]"
                class="mt-3 p-3 rounded-lg text-xs"
                :class="answers[q.globalIndex] === q.correct_option_index
                  ? 'bg-emerald-50 dark:bg-emerald-950/30 text-emerald-800 dark:text-emerald-200'
                  : 'bg-red-50 dark:bg-red-950/30 text-red-800 dark:text-red-200'"
              >
                <span class="font-semibold">
                  {{ answers[q.globalIndex] === q.correct_option_index ? '✓ Richtig.' : '✗ Falsch.' }}
                </span>
                {{ q.explanation }}
              </div>
            </div>
          </div>
        </div>

        <!-- Single shared audio element (re-targeted per click) -->
        <audio
          ref="audioEl"
          preload="auto"
          class="hidden"
          @ended="onAudioEnd"
          @pause="onAudioPause"
        />

        <div class="flex items-center justify-between gap-3 mb-12 max-w-3xl">
          <p class="text-xs text-slate-500 dark:text-slate-400">
            {{ answeredInTeil }} / {{ currentTeilQuestionCount }} Aufgaben beantwortet
          </p>
          <div class="flex gap-2">
            <button
              v-if="!teilSubmitted[currentTeilIndex]"
              type="button"
              @click="confirmTeil"
              :disabled="answeredInTeil < currentTeilQuestionCount"
              class="px-4 py-2 btn-gradient rounded-xl text-sm font-semibold disabled:opacity-50"
            >
              Teil bestätigen
            </button>
            <button
              v-else
              type="button"
              @click="goToNextTeil"
              class="px-4 py-2 btn-gradient rounded-xl text-sm font-semibold"
            >
              {{ currentTeilIndex + 1 < teile.length ? 'Nächster Teil →' : 'Ergebnis anzeigen' }}
            </button>
          </div>
        </div>
      </div>

      <!-- SUMMARY -->
      <div v-else-if="mode === 'done'">
        <h1 class="text-2xl sm:text-3xl font-bold mb-2">
          <span class="gradient-text">Ergebnis</span>
        </h1>
        <p class="text-sm text-slate-500 dark:text-slate-400 mb-6">{{ quiz?.title }}</p>

        <div class="glass-card rounded-2xl p-8 text-center mb-6 max-w-md">
          <p class="text-6xl font-bold gradient-text mb-2">
            {{ summaryCorrect }} / {{ allQuestions.length }}
          </p>
          <p class="text-base text-slate-600 dark:text-slate-400">{{ summaryPercent }}% richtig</p>
          <p v-if="submitting" class="text-xs text-slate-400 mt-3">Speichert…</p>
          <p v-else-if="submissionError" class="text-xs text-red-600 mt-3">
            Konnte das Ergebnis nicht speichern. {{ submissionError }}
          </p>
          <p v-else-if="submitted" class="text-xs text-emerald-600 mt-3">
            ✓ In deinem Verlauf gespeichert
          </p>
        </div>

        <!-- Per-Teil breakdown -->
        <div class="glass-card rounded-2xl p-5 mb-6 max-w-md">
          <h3 class="text-sm font-semibold text-slate-900 dark:text-white mb-3">Aufschlüsselung pro Teil</h3>
          <div class="space-y-2">
            <div
              v-for="(t, idx) in teile"
              :key="t.teil"
              class="flex items-center justify-between text-sm"
            >
              <span class="text-slate-700 dark:text-slate-300">{{ t.teil_name }}</span>
              <span class="font-semibold" :class="teilScoreClass(idx)">
                {{ teilCorrect(idx) }} / {{ t.questions.length }}
              </span>
            </div>
          </div>
        </div>

        <div class="flex gap-3 max-w-md">
          <NuxtLink
            to="/horen/deutsch_b1_horen"
            class="flex-1 px-4 py-2.5 rounded-xl font-semibold text-sm border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition text-center"
          >Zurück zur Übersicht</NuxtLink>
        </div>
      </div>

    </UDashboardPanelContent>
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })

const route = useRoute()
const config = useRuntimeConfig()
const quizId = route.params.quizId as string

type Question = {
  topic?: string
  stem: string
  options: string[]
  correct_option_index: number
  explanation: string
  audio_url: string
  audio_context?: string
}

type TeilSection = {
  teil: number
  teil_name: string
  instructions: string
  play_limit: number
  audio_segments: Array<{ audio_url: string; context: string; duration_seconds: number }>
  questions: Question[]
}

type FullExamContent = {
  kind: 'full_exam'
  teile: TeilSection[]
  questions: Array<Question & { teil: number }>
}

type LegacySingleTeilContent = {
  teil: number
  teil_name: string
  instructions: string
  play_limit: number
  audio_segments: Array<{ audio_url: string; context: string; duration_seconds: number }>
  questions: Question[]
}

type Quiz = {
  id: string
  title: string
  quiz_type: string
  num_questions: number
  content: FullExamContent | LegacySingleTeilContent
}

const mode = ref<'play' | 'done'>('play')
const loading = ref(true)
const error = ref<string | null>(null)

const quiz = ref<Quiz | null>(null)
const audioEl = ref<HTMLAudioElement | null>(null)

// Normalized list of Teile — wraps a legacy single-Teil quiz in a 1-element array
// so the rest of the runner can treat both shapes uniformly.
const teile = computed<TeilSection[]>(() => {
  const c = quiz.value?.content
  if (!c) return []
  if ('kind' in c && c.kind === 'full_exam') return c.teile
  // Legacy single-Teil shape
  return [{
    teil: c.teil,
    teil_name: c.teil_name,
    instructions: c.instructions,
    play_limit: c.play_limit,
    audio_segments: c.audio_segments,
    questions: c.questions
  }]
})

// Flat list across all Teile, with each question's index into this array as
// `globalIndex`. We use globalIndex as the answer key so the final POST to
// /quizzes/submit/{id} matches the question order in the saved Quiz.content.
type QuestionWithIndex = Question & { globalIndex: number; teil: number }
const allQuestions = computed<QuestionWithIndex[]>(() => {
  const out: QuestionWithIndex[] = []
  let i = 0
  for (const t of teile.value) {
    for (const q of t.questions) {
      out.push({ ...q, globalIndex: i, teil: t.teil })
      i++
    }
  }
  return out
})

// Per-question selected option, keyed by globalIndex. Sparse until answered.
const answers = ref<Record<number, number>>({})

// Per-Teil "submitted" lock — once confirmed, options become read-only and
// answers + explanations show.
const teilSubmitted = ref<Record<number, boolean>>({})

// Per-audio play counter — keyed by audio_url so users hear each audio at most
// `play_limit` times (the limit is per-Teil per the real exam).
const playsByAudio = ref<Record<string, number>>({})
const playingAudio = ref<string | null>(null)

const currentTeilIndex = ref(0)
const currentTeil = computed<TeilSection | null>(() => teile.value[currentTeilIndex.value] || null)

// Group the current Teil's questions by audio_url, preserving order, and tag
// each question with its globalIndex so the template can read/write answers.
type Group = { audio_url: string; audio_context: string; questions: QuestionWithIndex[] }
const currentTeilGroups = computed<Group[]>(() => {
  if (!currentTeil.value) return []
  const groupsByUrl = new Map<string, Group>()
  const order: string[] = []
  // Build a quick lookup from local question to globalIndex by walking
  // allQuestions and matching the current Teil's slice.
  const offset = teile.value.slice(0, currentTeilIndex.value).reduce((sum, t) => sum + t.questions.length, 0)
  currentTeil.value.questions.forEach((q, localIdx) => {
    const globalIndex = offset + localIdx
    const url = q.audio_url
    if (!groupsByUrl.has(url)) {
      groupsByUrl.set(url, { audio_url: url, audio_context: q.audio_context || '', questions: [] })
      order.push(url)
    }
    groupsByUrl.get(url)!.questions.push({ ...q, globalIndex, teil: currentTeil.value!.teil })
  })
  return order.map((url) => groupsByUrl.get(url)!)
})

const currentTeilQuestionCount = computed(() => currentTeil.value?.questions.length || 0)
const answeredInTeil = computed(() => {
  if (!currentTeil.value) return 0
  return currentTeilGroups.value.reduce((sum, g) => {
    return sum + g.questions.filter((q) => answers.value[q.globalIndex] !== undefined).length
  }, 0)
})

const submitting = ref(false)
const submitted = ref(false)
const submissionError = ref<string | null>(null)
const startedAt = ref<string>(new Date().toISOString())

const summaryCorrect = computed(() => {
  return allQuestions.value.filter((q) => answers.value[q.globalIndex] === q.correct_option_index).length
})
const summaryPercent = computed(() => {
  const total = allQuestions.value.length || 0
  return total > 0 ? Math.round((summaryCorrect.value / total) * 100) : 0
})

function teilCorrect(idx: number): number {
  const t = teile.value[idx]
  if (!t) return 0
  const offset = teile.value.slice(0, idx).reduce((sum, x) => sum + x.questions.length, 0)
  let correct = 0
  for (let i = 0; i < t.questions.length; i++) {
    const globalIndex = offset + i
    if (answers.value[globalIndex] === t.questions[i].correct_option_index) correct++
  }
  return correct
}

function teilScoreClass(idx: number): string {
  const t = teile.value[idx]
  if (!t || t.questions.length === 0) return 'text-slate-500'
  const pct = (teilCorrect(idx) / t.questions.length) * 100
  if (pct >= 80) return 'text-emerald-700 dark:text-emerald-300'
  if (pct >= 60) return 'text-amber-700 dark:text-amber-300'
  return 'text-red-700 dark:text-red-300'
}

function absoluteAudioUrl(path: string): string {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `${config.public.apiBase}${path}`
}

function playsForAudio(url: string): number {
  return playsByAudio.value[url] || 0
}

function optionClass(q: QuestionWithIndex, oi: number): string {
  const submitted = teilSubmitted.value[currentTeilIndex.value]
  const selected = answers.value[q.globalIndex]
  if (!submitted) {
    return selected === oi
      ? 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/30'
      : 'border-slate-300 dark:border-slate-700 hover:border-slate-400 dark:hover:border-slate-600'
  }
  if (oi === q.correct_option_index) return 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/30'
  if (oi === selected && selected !== q.correct_option_index) {
    return 'border-red-500 bg-red-50 dark:bg-red-950/30'
  }
  return 'border-slate-300 dark:border-slate-700 opacity-60'
}

function playAudio(url: string) {
  if (!audioEl.value) return
  if (!currentTeil.value) return
  if (playsByAudio.value[url] >= currentTeil.value.play_limit) return
  // If a different audio is currently playing, stop it first.
  if (playingAudio.value && playingAudio.value !== url) {
    audioEl.value.pause()
  }
  audioEl.value.src = absoluteAudioUrl(url)
  audioEl.value.currentTime = 0
  audioEl.value.play()
  playingAudio.value = url
}

function onAudioEnd() {
  if (playingAudio.value) {
    playsByAudio.value[playingAudio.value] = (playsByAudio.value[playingAudio.value] || 0) + 1
  }
  playingAudio.value = null
}

function onAudioPause() {
  // User-initiated pause shouldn't count toward play_limit; only `ended` counts.
  // But we do clear `playingAudio` so the UI returns to "play" state.
  if (audioEl.value && audioEl.value.ended) return
  playingAudio.value = null
}

function confirmTeil() {
  if (answeredInTeil.value < currentTeilQuestionCount.value) return
  teilSubmitted.value[currentTeilIndex.value] = true
}

async function goToNextTeil() {
  if (audioEl.value) {
    audioEl.value.pause()
    playingAudio.value = null
  }
  if (currentTeilIndex.value + 1 < teile.value.length) {
    currentTeilIndex.value += 1
    // Scroll to top of next Teil
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }
  mode.value = 'done'
  await persistResult()
}

async function persistResult() {
  if (!quiz.value) return
  submitting.value = true
  submissionError.value = null
  try {
    const payload = allQuestions.value.map((q) => ({
      question_index: q.globalIndex,
      selected_options: answers.value[q.globalIndex] ?? -1
    }))
    await $fetch(
      `${config.public.apiBase}/quizzes/submit/${quiz.value.id}`,
      {
        method: 'POST',
        credentials: 'include',
        body: {
          quiz_id: quiz.value.id,
          answers: payload,
          started_at: startedAt.value
        }
      }
    )
    submitted.value = true
  } catch (e: any) {
    submissionError.value = e?.data?.detail || e?.message || 'Unknown error'
  } finally {
    submitting.value = false
  }
}

async function loadQuiz() {
  loading.value = true
  error.value = null
  try {
    const rows = await $fetch<Quiz[] | Quiz>(
      `${config.public.apiBase}/quizzes/${quizId}`,
      { credentials: 'include' }
    )
    const row = Array.isArray(rows) ? rows[0] : rows
    if (!row) {
      error.value = 'Diese Sitzung wurde nicht gefunden.'
      return
    }
    if (row.quiz_type !== 'audio_listening') {
      error.value = 'Diese Quiz-Art kann hier nicht abgespielt werden.'
      return
    }
    if (!row.content) {
      error.value = 'Diese Sitzung enthält keine Inhalte.'
      return
    }
    quiz.value = row
    startedAt.value = new Date().toISOString()
  } catch (e: any) {
    error.value = e?.data?.detail || e?.message || 'Konnte die Sitzung nicht laden.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadQuiz()
})
</script>
