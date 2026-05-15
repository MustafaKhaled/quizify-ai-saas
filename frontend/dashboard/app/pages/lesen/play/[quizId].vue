<template>
  <UDashboardPanel grow>
    <UDashboardNavbar class="lg:hidden" :title="quiz?.title || 'Lesen'" />
    <UDashboardPanelContent class="p-4 sm:p-6 overflow-y-auto bg-mesh min-h-full">

      <div v-if="loading" class="text-center py-16">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-violet-500 mx-auto mb-4"></div>
        <p class="text-sm text-slate-500 dark:text-slate-400">Lädt…</p>
      </div>

      <div v-else-if="error" class="text-center py-16">
        <p class="text-red-600 dark:text-red-400 font-medium mb-3">{{ error }}</p>
        <NuxtLink to="/lesen/deutsch_b1_lesen" class="text-sm gradient-text font-medium hover:opacity-80">
          ← Zurück zur Übersicht
        </NuxtLink>
      </div>

      <!-- RUNNER: walk through one Teil at a time -->
      <div v-else-if="mode === 'play' && currentTeil">
        <div class="mb-6 flex items-start justify-between flex-wrap gap-2">
          <div>
            <NuxtLink
              to="/lesen/deutsch_b1_lesen"
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
                ? 'bg-violet-600 text-white'
                : (idx < currentTeilIndex
                    ? 'bg-violet-500/20 text-violet-700 dark:text-violet-300'
                    : 'bg-slate-200 dark:bg-slate-700 text-slate-500')"
            >
              {{ t.teil }}
            </span>
          </div>
        </div>

        <div class="glass-card rounded-2xl p-4 mb-6 text-sm text-slate-700 dark:text-slate-300">
          {{ currentTeil.instructions }}
        </div>

        <!-- ─── LAYOUT: passage_questions ───────────────────────────────
             One passage (article / blog / email / directory / institutional doc) +
             N questions with radio options. Used by B1 Teil 1 (R/F), B1 Teil 5 (MCQ),
             A2 Teil 1/2/3 (newspaper / directory / email MCQ). The radio option
             text differs per question via the `options` array on each question. -->
        <div v-if="currentTeil.layout === 'passage_questions'" class="space-y-6">
          <div class="glass-card rounded-2xl p-6">
            <p v-if="currentTeil.context" class="text-xs uppercase tracking-wide font-semibold text-slate-500 dark:text-slate-400 mb-2">
              {{ currentTeil.context }}
            </p>
            <h2 v-if="currentTeil.passage_title" class="text-base font-bold text-slate-900 dark:text-white mb-3">
              {{ currentTeil.passage_title }}
            </h2>
            <p class="text-sm text-slate-800 dark:text-slate-200 leading-relaxed whitespace-pre-line">
              {{ currentTeil.passage }}
            </p>
          </div>

          <div class="glass-card rounded-2xl p-6 space-y-6">
            <div v-for="q in currentTeilQuestions" :key="q.globalIndex" class="border-t border-slate-200 dark:border-slate-700 pt-4 first:border-t-0 first:pt-0">
              <p class="font-semibold text-sm text-slate-900 dark:text-white mb-3">
                <span class="text-violet-700 dark:text-violet-300 mr-1">{{ q.localIndex + 1 }}.</span>
                {{ q.stem }}
              </p>
              <RadioOptions :q="q" :answers="answers" :submitted="teilSubmitted[currentTeilIndex]" />
              <ExplanationBlock :q="q" :answers="answers" :submitted="teilSubmitted[currentTeilIndex]" />
            </div>
          </div>
        </div>

        <!-- ─── LAYOUT: two_passages_questions (B1 Teil 2 only) ───────── -->
        <div v-else-if="currentTeil.layout === 'two_passages_questions'" class="space-y-6">
          <div
            v-for="passage in currentTeil.passages || []"
            :key="passage.passage_id"
            class="space-y-4"
          >
            <div class="glass-card rounded-2xl p-6">
              <p v-if="passage.context" class="text-xs uppercase tracking-wide font-semibold text-slate-500 dark:text-slate-400 mb-2">
                {{ passage.context }}
              </p>
              <h2 class="text-base font-bold text-slate-900 dark:text-white mb-3">
                {{ passage.title }}
              </h2>
              <p class="text-sm text-slate-800 dark:text-slate-200 leading-relaxed whitespace-pre-line">
                {{ passage.text }}
              </p>
            </div>

            <div class="glass-card rounded-2xl p-6 space-y-6">
              <div
                v-for="q in questionsForPassage(passage.passage_id)"
                :key="q.globalIndex"
                class="border-t border-slate-200 dark:border-slate-700 pt-4 first:border-t-0 first:pt-0"
              >
                <p class="font-semibold text-sm text-slate-900 dark:text-white mb-3">
                  <span class="text-violet-700 dark:text-violet-300 mr-1">{{ q.localIndex + 1 }}.</span>
                  {{ q.stem }}
                </p>
                <RadioOptions :q="q" :answers="answers" :submitted="teilSubmitted[currentTeilIndex]" />
                <ExplanationBlock :q="q" :answers="answers" :submitted="teilSubmitted[currentTeilIndex]" />
              </div>
            </div>
          </div>
        </div>

        <!-- ─── LAYOUT: letter_matching ─────────────────────────────────
             Ad pool + situations. The pool size, situations count, and no-match
             marker come from the manifest so this template works for both A2
             (6 ads, 5 situations, 'X' no-match) and B1 (10 ads, 7 situations,
             '0' no-match). -->
        <div v-else-if="currentTeil.layout === 'letter_matching'" class="space-y-6">
          <!-- How-to panel: makes the task explicit. Numbers + marker come from
               the manifest so this works at both B1 (10 ads/7 situations/'0') and
               A2 (6 ads/5 situations/'X'). -->
          <div class="rounded-2xl p-5 bg-violet-50 dark:bg-violet-950/40 border border-violet-200 dark:border-violet-800">
            <p class="text-sm font-semibold text-violet-900 dark:text-violet-100 mb-2 flex items-center gap-2">
              <UIcon name="i-lucide-info" class="w-4 h-4" />
              So funktioniert dieser Teil
            </p>
            <ol class="text-xs text-violet-900/80 dark:text-violet-100/80 space-y-1 list-decimal list-inside">
              <li>Lies die <strong>{{ poolSize }} Anzeigen ({{ letterRange }})</strong> im oberen Block.</li>
              <li>Lies dann die <strong>{{ currentTeilQuestions.length }} Situationen</strong> darunter.</li>
              <li>Trage in das Feld jeder Situation den passenden Buchstaben ein — z.&nbsp;B. <code class="px-1 py-0.5 rounded bg-violet-200 dark:bg-violet-900 font-mono">{{ exampleLetter }}</code>.</li>
              <li>Wenn keine Anzeige passt, schreib eine <code class="px-1 py-0.5 rounded bg-violet-200 dark:bg-violet-900 font-mono">{{ noMatchMarker }}</code>.</li>
              <li>Jede Anzeige passt höchstens zu einer Situation. {{ distractorAdsLabel }} passen zu keiner Situation.</li>
            </ol>
          </div>

          <!-- Mobile-only scroll hint: tells the user the questions are below
               the (long) ad pool so they don't think the page is ad-only. -->
          <a
            href="#lesen-teil3-situationen"
            class="lg:hidden flex items-center justify-between gap-2 rounded-xl bg-violet-100 dark:bg-violet-900/40 border border-violet-300 dark:border-violet-700 px-4 py-2.5 text-sm font-semibold text-violet-900 dark:text-violet-100"
          >
            <span>↓ Direkt zu den {{ currentTeilQuestions.length }} Situationen</span>
            <UIcon name="i-lucide-arrow-down" class="w-4 h-4" />
          </a>

          <!-- 2-column layout on lg+: ads on the left (sticky, scrollable
               internally if taller than the viewport), situations on the right
               in normal page flow. On smaller screens, stack with ads first
               then situations (the scroll hint above lets users skip ahead). -->
          <div class="lg:grid lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)] lg:gap-6 lg:items-start">
            <!-- Ad pool column -->
            <div class="glass-card rounded-2xl p-5 mb-6 lg:mb-0 lg:sticky lg:top-2 lg:max-h-[calc(100vh-1rem)] lg:overflow-y-auto">
              <p class="text-xs uppercase tracking-wide font-semibold text-slate-500 dark:text-slate-400 mb-3">
                Anzeigen {{ letterRange }}
              </p>
              <div class="grid sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2 gap-3">
                <div
                  v-for="ad in (currentTeil.ad_pool?.ads || [])"
                  :key="ad.letter"
                  class="border border-slate-200 dark:border-slate-700 rounded-xl p-3 text-xs"
                  :class="usedLetterClass(ad.letter)"
                >
                  <p class="font-bold text-violet-700 dark:text-violet-300 mb-1">
                    <span class="inline-block w-5 h-5 rounded-full bg-violet-100 dark:bg-violet-900/50 text-center leading-5 mr-1">
                      {{ ad.letter }}
                    </span>
                    {{ ad.title }}
                  </p>
                  <p class="text-slate-700 dark:text-slate-300 leading-relaxed">{{ ad.text }}</p>
                </div>
              </div>
            </div>

            <!-- Situations column -->
            <div id="lesen-teil3-situationen" class="glass-card rounded-2xl p-6 space-y-5 scroll-mt-4">
              <p class="text-xs uppercase tracking-wide font-semibold text-slate-500 dark:text-slate-400 -mt-2 mb-1">
                Situationen 1–{{ currentTeilQuestions.length }}
              </p>
              <div
                v-for="q in currentTeilQuestions"
                :key="q.globalIndex"
                class="border-t border-slate-200 dark:border-slate-700 pt-4 first:border-t-0 first:pt-0"
              >
                <div class="flex items-start gap-3 mb-2">
                  <span class="font-semibold text-violet-700 dark:text-violet-300">{{ q.localIndex + 1 }}.</span>
                  <p class="font-medium text-sm text-slate-900 dark:text-white flex-1">{{ q.stem }}</p>
                </div>
                <div class="flex items-center gap-3 ml-7">
                  <input
                    type="text"
                    maxlength="1"
                    :value="answers[q.globalIndex]"
                    @input="(e) => handleLetterInput(q.globalIndex, (e.target as HTMLInputElement).value)"
                    :disabled="teilSubmitted[currentTeilIndex]"
                    class="w-14 h-12 text-center font-bold text-lg uppercase rounded-xl border-2 focus:outline-none focus:ring-2 focus:ring-violet-500"
                    :class="letterInputClass(q)"
                    placeholder="?"
                  />
                  <span class="text-xs text-slate-500 dark:text-slate-400">
                    Buchstabe {{ letterRange }} oder „{{ noMatchMarker }}" wenn keine Anzeige passt.
                  </span>
                </div>
                <p
                  v-if="!teilSubmitted[currentTeilIndex] && duplicateWarningFor(q.globalIndex)"
                  class="ml-7 mt-2 text-xs text-amber-700 dark:text-amber-300 flex items-center gap-1.5"
                >
                  <UIcon name="i-lucide-alert-triangle" class="w-3.5 h-3.5" />
                  {{ duplicateWarningFor(q.globalIndex) }}
                </p>
                <ExplanationBlock :q="q" :answers="answers" :submitted="teilSubmitted[currentTeilIndex]" />
              </div>
            </div>
          </div>
        </div>

        <!-- ─── TEIL 4 (Reader comments + Ja/Nein) ────────────────────── -->
        <!-- ─── LAYOUT: comments_questions (B1 Teil 4 only) ─────────────
             One prompt + N reader comments + Ja/Nein per comment. -->
        <div v-else-if="currentTeil.layout === 'comments_questions'" class="space-y-6">
          <div class="glass-card rounded-2xl p-6">
            <p v-if="currentTeil.context" class="text-xs uppercase tracking-wide font-semibold text-slate-500 dark:text-slate-400 mb-2">
              {{ currentTeil.context }}
            </p>
            <p class="text-sm text-slate-800 dark:text-slate-200 leading-relaxed">
              {{ currentTeil.prompt_de }}
            </p>
          </div>

          <div class="space-y-4">
            <div
              v-for="comment in currentTeil.comments || []"
              :key="comment.comment_id"
              class="space-y-3"
            >
              <div class="glass-card rounded-2xl p-5">
                <p class="text-xs uppercase tracking-wide font-semibold text-violet-700 dark:text-violet-300 mb-2">
                  {{ comment.author }}
                </p>
                <p class="text-sm text-slate-800 dark:text-slate-200 leading-relaxed whitespace-pre-line">
                  {{ comment.text }}
                </p>
              </div>
              <div
                v-for="q in questionsForComment(comment.comment_id)"
                :key="q.globalIndex"
                class="glass-card rounded-2xl p-5 ml-0 sm:ml-6"
              >
                <p class="font-semibold text-sm text-slate-900 dark:text-white mb-3">
                  <span class="text-violet-700 dark:text-violet-300 mr-1">{{ q.localIndex + 1 }}.</span>
                  {{ q.stem }}
                </p>
                <RadioOptions :q="q" :answers="answers" :submitted="teilSubmitted[currentTeilIndex]" />
                <ExplanationBlock :q="q" :answers="answers" :submitted="teilSubmitted[currentTeilIndex]" />
              </div>
            </div>
          </div>
        </div>

        <!-- Confirm/Next bar.
             The confirm button stays enabled even when items are unanswered —
             unanswered ones are scored wrong, but the user is never trapped on
             a Teil. The unanswered count is shown inline as a soft warning. -->
        <div class="flex items-center justify-between gap-3 my-8 max-w-3xl">
          <div class="text-xs text-slate-500 dark:text-slate-400">
            <p>{{ answeredInTeil }} / {{ currentTeilQuestions.length }} Aufgaben beantwortet</p>
            <p
              v-if="!teilSubmitted[currentTeilIndex] && answeredInTeil < currentTeilQuestions.length"
              class="text-amber-700 dark:text-amber-300 mt-1"
            >
              {{ currentTeilQuestions.length - answeredInTeil }} {{ currentTeilQuestions.length - answeredInTeil === 1 ? 'Aufgabe ist' : 'Aufgaben sind' }} noch leer und {{ currentTeilQuestions.length - answeredInTeil === 1 ? 'wird' : 'werden' }} als falsch gewertet.
            </p>
          </div>
          <div class="flex gap-2 shrink-0">
            <button
              v-if="!teilSubmitted[currentTeilIndex]"
              type="button"
              @click="confirmTeil"
              class="px-4 py-2 btn-gradient rounded-xl text-sm font-semibold"
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
            to="/lesen/deutsch_b1_lesen"
            class="flex-1 px-4 py-2.5 rounded-xl font-semibold text-sm border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition text-center"
          >Zurück zur Übersicht</NuxtLink>
        </div>
      </div>

    </UDashboardPanelContent>
  </UDashboardPanel>
</template>

<script setup lang="ts">
import { defineComponent, h, type PropType } from 'vue'

definePageMeta({ layout: 'default' })

const route = useRoute()
const config = useRuntimeConfig()
const quizId = route.params.quizId as string

// Per-question answer types: int for single_choice / true_false (Teil 1, 2, 4, 5)
// or string for letter_matching (Teil 3 — 'a'–'j' or '0').
type AnswerValue = number | string | undefined

type LesenQuestion = {
  question_type: 'true_false' | 'single_choice' | 'letter_matching' | 'true_false_ja_nein'
  topic?: string
  stem: string
  options?: string[]
  correct_option_index?: number
  correct_letter?: string
  explanation: string
  passage_id?: string
  comment_id?: string
  pool_id?: string
  teil: number
}

type Ad = { letter: string; title: string; text: string }
type Passage = { passage_id: string; title: string; context?: string; text: string }
type Comment = { comment_id: string; author: string; text: string }

// Layout discriminator written by the backend per Teil. The play page
// dispatches on this so both A2 (4 Teile) and B1 (5 Teile) render with the
// same templates without level-specific branching.
type LesenLayout =
  | 'passage_questions'
  | 'two_passages_questions'
  | 'letter_matching'
  | 'comments_questions'

type LesenTeil = {
  teil: number
  teil_name: string
  layout?: LesenLayout
  instructions: string
  context?: string
  passage_title?: string
  passage?: string
  passages?: Passage[]
  ad_pool?: {
    pool_id: string
    ads: Ad[]
    valid_letters?: string[]   // a–j for B1, a–f for A2
    no_match_marker?: string   // '0' for B1, 'X' for A2
  }
  prompt_de?: string
  comments?: Comment[]
  questions: LesenQuestion[]
}

type LesenContent = {
  kind: 'full_lesen_exam'
  teile: LesenTeil[]
  questions: LesenQuestion[]
}

type Quiz = {
  id: string
  title: string
  quiz_type: string
  num_questions: number
  content: LesenContent
}

const mode = ref<'play' | 'done'>('play')
const loading = ref(true)
const error = ref<string | null>(null)
const quiz = ref<Quiz | null>(null)

const teile = computed<LesenTeil[]>(() => quiz.value?.content?.teile || [])

// Flat list across all Teile, with each question's globalIndex into this array
// as the answer-key. We also tag each with its localIndex inside its Teil so
// the UI can show "1.", "2.", ... per Teil instead of per-exam numbering.
type QuestionWithIndex = LesenQuestion & { globalIndex: number; localIndex: number }
const allQuestions = computed<QuestionWithIndex[]>(() => {
  const out: QuestionWithIndex[] = []
  let g = 0
  for (const t of teile.value) {
    let local = 0
    for (const q of t.questions) {
      out.push({ ...q, globalIndex: g, localIndex: local, teil: t.teil })
      g++
      local++
    }
  }
  return out
})

const answers = ref<Record<number, AnswerValue>>({})
const teilSubmitted = ref<Record<number, boolean>>({})
const currentTeilIndex = ref(0)
const currentTeil = computed<LesenTeil | null>(() => teile.value[currentTeilIndex.value] || null)

// Questions belonging to the current Teil, with their global + local indices.
const currentTeilQuestions = computed<QuestionWithIndex[]>(() => {
  const t = currentTeil.value
  if (!t) return []
  const offset = teile.value.slice(0, currentTeilIndex.value).reduce((sum, x) => sum + x.questions.length, 0)
  return t.questions.map((q, i) => ({ ...q, globalIndex: offset + i, localIndex: i, teil: t.teil }))
})

function questionsForPassage(passage_id: string): QuestionWithIndex[] {
  return currentTeilQuestions.value.filter((q) => q.passage_id === passage_id)
}
function questionsForComment(comment_id: string): QuestionWithIndex[] {
  return currentTeilQuestions.value.filter((q) => q.comment_id === comment_id)
}

const answeredInTeil = computed<number>(() => {
  return currentTeilQuestions.value.filter((q) => isAnswered(answers.value[q.globalIndex])).length
})

function isAnswered(v: AnswerValue): boolean {
  if (v === undefined || v === null) return false
  if (typeof v === 'string') return v.trim().length > 0
  return true  // number — includes 0 (Richtig / Ja)
}

// ── Letter input for letter_matching layout ─────────────────────────────────
// Letter set + no-match marker come from the manifest's ad_pool so this page
// works for both A2 (a–f, 'X' no-match) and B1 (a–j, '0' no-match). Falls
// back to B1 defaults for older quizzes generated before the layout refactor.

const adPoolLetters = computed<string[]>(() => {
  const pool = currentTeil.value?.ad_pool
  if (pool?.valid_letters?.length) return pool.valid_letters.map((l) => l.toLowerCase())
  // Legacy quizzes (pre-refactor) used the B1 letter set unconditionally.
  return ['a','b','c','d','e','f','g','h','i','j']
})

const noMatchMarker = computed<string>(() => {
  const pool = currentTeil.value?.ad_pool
  return (pool?.no_match_marker || '0').toUpperCase()
})

const validLetters = computed<Set<string>>(() => {
  const set = new Set(adPoolLetters.value)
  set.add(noMatchMarker.value.toLowerCase())
  return set
})

const poolSize = computed<number>(() => currentTeil.value?.ad_pool?.ads?.length || 0)
const exampleLetter = computed<string>(() => adPoolLetters.value[2] || 'c')
const letterRange = computed<string>(() => {
  const letters = adPoolLetters.value
  if (letters.length === 0) return ''
  return `${letters[0]}–${letters[letters.length - 1]}`
})

// Distractor count = ads not matched by any situation. The exam guarantees
// exactly one situation has the no-match marker, so winners = situations - 1
// and distractors = poolSize - winners.
const distractorAdsLabel = computed<string>(() => {
  const ads = poolSize.value
  const sits = currentTeilQuestions.value.length
  if (!ads || !sits) return ''
  const distractors = Math.max(ads - (sits - 1), 0)
  if (distractors === 0) return 'Keine Anzeige bleibt übrig'
  if (distractors === 1) return 'Eine Anzeige bleibt übrig und passt zu keiner Situation. Sie'
  const wordsByCount: Record<number, string> = { 2: 'Zwei', 3: 'Drei', 4: 'Vier', 5: 'Fünf', 6: 'Sechs' }
  const word = wordsByCount[distractors] || `${distractors}`
  return `${word} Anzeigen`
})

function handleLetterInput(globalIndex: number, raw: string) {
  const v = (raw || '').toLowerCase().trim()
  if (!v) {
    delete answers.value[globalIndex]
    return
  }
  // Only accept a single valid character (a–<last>, or the no-match marker).
  // Anything else is silently rejected so the input visibly clears next render.
  if (!validLetters.value.has(v)) {
    delete answers.value[globalIndex]
    return
  }
  answers.value[globalIndex] = v
}

// Soft-warn if the user reuses a letter across situations. Skip the warning
// for the no-match marker — it doesn't even appear twice in a valid exam, but
// users sometimes type it more than once while puzzling out which situation
// has no match, and the warning would be noise.
function duplicateWarningFor(globalIndex: number): string | null {
  const v = answers.value[globalIndex]
  if (typeof v !== 'string' || !v) return null
  if (v.toLowerCase() === noMatchMarker.value.toLowerCase()) return null
  const others = currentTeilQuestions.value
    .filter((q) => q.globalIndex !== globalIndex)
    .map((q) => answers.value[q.globalIndex])
    .filter((a): a is string => typeof a === 'string' && a === v)
  if (others.length === 0) return null
  return `Du hast „${v.toUpperCase()}" auch bei einer anderen Situation gewählt. Jede Anzeige kann nur einmal passen — bist du sicher?`
}

function letterInputClass(q: QuestionWithIndex): string {
  const v = answers.value[q.globalIndex]
  const submitted = teilSubmitted.value[currentTeilIndex.value]
  if (submitted) {
    const correct = (q.correct_letter || '').toLowerCase()
    const userLetter = typeof v === 'string' ? v.toLowerCase() : ''
    if (userLetter === correct) {
      return 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-900 dark:text-emerald-100'
    }
    return 'border-red-500 bg-red-50 dark:bg-red-950/30 text-red-900 dark:text-red-100'
  }
  if (typeof v === 'string' && v.length > 0) {
    return 'border-violet-500 bg-violet-50 dark:bg-violet-950/30 text-violet-900 dark:text-violet-100'
  }
  return 'border-slate-300 dark:border-slate-700'
}

// Visual hint on each ad in the pool: which letters are already used by THIS
// user across the situations. Helps the user notice their own conflicts at a
// glance without enforcing the single-use rule.
function usedLetterClass(letter: string): string {
  if (currentTeil.value?.layout !== 'letter_matching') return ''
  const usedCount = currentTeilQuestions.value.filter((q) => answers.value[q.globalIndex] === letter).length
  if (usedCount === 0) return 'bg-slate-50/40 dark:bg-slate-900/40'
  if (usedCount === 1) return 'bg-violet-50 dark:bg-violet-950/40 border-violet-300 dark:border-violet-700'
  return 'bg-amber-50 dark:bg-amber-950/40 border-amber-400 dark:border-amber-600'
}

// ── Scoring helpers (match backend logic) ───────────────────────────────────

function isCorrect(q: QuestionWithIndex): boolean {
  const v = answers.value[q.globalIndex]
  if (q.question_type === 'letter_matching') {
    return typeof v === 'string' && v.toLowerCase() === (q.correct_letter || '').toLowerCase()
  }
  return v === q.correct_option_index
}

const summaryCorrect = computed(() => allQuestions.value.filter(isCorrect).length)
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
    const q = { ...t.questions[i], globalIndex, localIndex: i, teil: t.teil } as QuestionWithIndex
    if (isCorrect(q)) correct++
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

// ── Flow control + persistence ──────────────────────────────────────────────

const submitting = ref(false)
const submitted = ref(false)
const submissionError = ref<string | null>(null)
const startedAt = ref<string>(new Date().toISOString())

function confirmTeil() {
  // Always allow confirm — unanswered items are scored wrong, but the user
  // is never trapped on a Teil. The UI surfaces the unanswered count inline.
  teilSubmitted.value[currentTeilIndex.value] = true
}

async function goToNextTeil() {
  if (currentTeilIndex.value + 1 < teile.value.length) {
    currentTeilIndex.value += 1
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
    // For unanswered questions, send a sentinel (-1) so the backend records a
    // wrong-answer entry rather than skipping the question. Letter-matching
    // unanswered → empty string. The scorer treats neither as correct.
    const payload = allQuestions.value.map((q) => {
      const a = answers.value[q.globalIndex]
      let value: number | string | number[] = -1
      if (q.question_type === 'letter_matching') {
        value = typeof a === 'string' ? a : ''
      } else if (typeof a === 'number') {
        value = a
      }
      return { question_index: q.globalIndex, selected_options: value }
    })
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
    if (row.quiz_type !== 'reading') {
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

// Two small inline components keep the per-Teil templates readable. Defined
// inside <script setup> so they auto-expose to the template by name.

const RadioOptions = defineComponent({
  props: {
    q: { type: Object, required: true },
    answers: { type: Object as PropType<Record<number, any>>, required: true },
    submitted: { type: Boolean, default: false }
  },
  setup(props) {
    return () => {
      const q = props.q as { globalIndex: number; options: string[]; correct_option_index: number }
      const sel = props.answers[q.globalIndex]
      return h('div', { class: 'space-y-2' }, q.options.map((opt: string, oi: number) => {
        let cls = 'border-slate-300 dark:border-slate-700 hover:border-slate-400 dark:hover:border-slate-600'
        if (props.submitted) {
          if (oi === q.correct_option_index) {
            cls = 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/30'
          } else if (oi === sel) {
            cls = 'border-red-500 bg-red-50 dark:bg-red-950/30'
          } else {
            cls = 'border-slate-300 dark:border-slate-700 opacity-60'
          }
        } else if (sel === oi) {
          cls = 'border-violet-500 bg-violet-50 dark:bg-violet-950/30'
        }
        return h('label', {
          key: oi,
          class: `block p-3 rounded-xl border cursor-pointer transition text-sm ${cls}`
        }, [
          h('input', {
            type: 'radio',
            value: oi,
            checked: sel === oi,
            disabled: props.submitted,
            class: 'mr-3 align-middle',
            onChange: () => { props.answers[q.globalIndex] = oi }
          }),
          h('span', { class: 'align-middle' }, opt)
        ])
      }))
    }
  }
})

const ExplanationBlock = defineComponent({
  props: {
    q: { type: Object, required: true },
    answers: { type: Object as PropType<Record<number, any>>, required: true },
    submitted: { type: Boolean, default: false }
  },
  setup(props) {
    return () => {
      if (!props.submitted) return null
      const q = props.q as {
        globalIndex: number
        question_type: string
        correct_option_index?: number
        correct_letter?: string
        explanation: string
      }
      const v = props.answers[q.globalIndex]
      let isOk = false
      if (q.question_type === 'letter_matching') {
        isOk = typeof v === 'string' && v.toLowerCase() === (q.correct_letter || '').toLowerCase()
      } else {
        isOk = v === q.correct_option_index
      }
      return h('div', {
        class: `mt-3 p-3 rounded-lg text-xs ${
          isOk
            ? 'bg-emerald-50 dark:bg-emerald-950/30 text-emerald-800 dark:text-emerald-200'
            : 'bg-red-50 dark:bg-red-950/30 text-red-800 dark:text-red-200'
        }`
      }, [
        h('span', { class: 'font-semibold mr-1' }, isOk ? '✓ Richtig.' : '✗ Falsch.'),
        h('span', null, q.explanation)
      ])
    }
  }
})

onMounted(() => {
  loadQuiz()
})
</script>
