<template>
  <UDashboardPanel grow>
    <UDashboardNavbar class="lg:hidden" :title="'B1 Hören'" />
    <UDashboardPanelContent class="p-4 sm:p-6 overflow-y-auto bg-mesh min-h-full">

      <h1 class="text-2xl sm:text-3xl font-bold mb-1">
        <span class="gradient-text">German B1 — Hören</span>
      </h1>
      <p class="text-sm text-slate-500 dark:text-slate-400 mb-8">
        Generate a fresh full Goethe-Zertifikat B1 listening exam (all four Teile),
        or replay a previous exam.
      </p>

      <!-- Generate new exam -->
      <div class="mb-10">
        <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-3">Neue Prüfung generieren</h2>
        <p class="text-xs text-slate-500 dark:text-slate-400 mb-4">
          Ein vollständiger Hörverstehenstest enthält alle vier Teile.
          Die Generierung dauert etwa zwei Minuten (Gemini-Skripte + Edge-TTS-Audio für jeden Teil).
        </p>

        <div class="glass-card rounded-2xl p-5 mb-3 max-w-3xl">
          <ul class="text-xs text-slate-600 dark:text-slate-400 space-y-1.5 mb-4">
            <li v-for="t in TEILE_META" :key="t.teil" class="flex items-start gap-2">
              <UIcon name="i-lucide-headphones" class="w-3.5 h-3.5 mt-0.5 text-emerald-600" />
              <span>
                <span class="font-semibold text-slate-700 dark:text-slate-300">Teil {{ t.teil }}</span>
                — {{ t.name }} · {{ t.format_hint }}
              </span>
            </li>
          </ul>
          <button
            @click="generateExam"
            :disabled="generating"
            class="w-full px-4 py-3 btn-gradient rounded-xl font-semibold text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <template v-if="generating">
              Generiert… {{ generationElapsed }}s
            </template>
            <template v-else>
              Vollständige Prüfung generieren (~2 Min.)
            </template>
          </button>
        </div>

        <p v-if="generationError" class="mt-3 text-sm text-red-600 dark:text-red-400">
          {{ generationError }}
        </p>
      </div>

      <!-- User's existing exams -->
      <div>
        <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-3">Meine Prüfungen</h2>
        <div v-if="loadingSessions" class="text-sm text-slate-500 dark:text-slate-400 py-6">
          Lädt…
        </div>
        <div v-else-if="sessions.length === 0" class="glass-card rounded-2xl p-6 text-sm text-slate-500 dark:text-slate-400">
          Noch keine Prüfungen. Generiere oben deine erste.
        </div>
        <div v-else class="space-y-2 max-w-3xl">
          <div
            v-for="s in sessions"
            :key="s.quiz_id"
            class="glass-card rounded-xl p-4 flex items-center justify-between gap-4 hover:shadow-md transition"
          >
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2 mb-0.5 flex-wrap">
                <span class="text-xs uppercase tracking-wide font-semibold text-emerald-700 dark:text-emerald-300">
                  {{ s.kind === 'full_exam' ? `${s.num_teile} Teile` : (s.teil_label || 'Einzel-Teil') }}
                </span>
                <span v-if="s.latest_score !== null" class="px-2 py-0.5 text-xs font-bold rounded-full" :class="scoreBadgeClass(s.latest_score)">
                  {{ Math.round(s.latest_score) }}%
                </span>
                <span v-else class="px-2 py-0.5 text-xs font-medium rounded-full text-slate-600 dark:text-slate-400 bg-slate-500/10">
                  Noch nicht versucht
                </span>
              </div>
              <p class="text-sm font-semibold text-slate-900 dark:text-white truncate">{{ s.title }}</p>
              <p class="text-xs text-slate-500 dark:text-slate-400">
                {{ s.num_questions }} {{ s.num_questions === 1 ? 'Aufgabe' : 'Aufgaben' }} ·
                Generiert {{ formatDate(s.generated_at) }}
              </p>
            </div>
            <NuxtLink
              :to="`/horen/play/${s.quiz_id}`"
              class="px-3 py-1.5 btn-gradient rounded-lg text-xs font-semibold whitespace-nowrap"
            >
              {{ s.latest_score !== null ? 'Nochmal üben' : 'Starten →' }}
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- Generation overlay -->
      <div v-if="generating" class="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
        <div class="glass-card rounded-2xl p-8 max-w-md text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500 mx-auto mb-4"></div>
          <h3 class="text-lg font-bold mb-2">Generiere Prüfung…</h3>
          <p class="text-sm text-slate-500 dark:text-slate-400 mb-2">
            Gemini schreibt vier Hörtexte, dann rendert Edge TTS das Audio für jeden Teil.
          </p>
          <p class="text-xs text-slate-400">~2 Minuten · {{ generationElapsed }}s</p>
        </div>
      </div>

    </UDashboardPanelContent>
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })

const route = useRoute()
const config = useRuntimeConfig()
const slug = route.params.slug as string

const TEILE_META = [
  { teil: 1, name: 'Kurze Texte', format_hint: '5 kurze Monologe · 5 Aufgaben' },
  { teil: 2, name: 'Vortrag', format_hint: 'Längerer Vortrag · 5 Aufgaben' },
  { teil: 3, name: 'Gespräch', format_hint: 'Dialog · 7 Richtig/Falsch-Aufgaben' },
  { teil: 4, name: 'Diskussion', format_hint: 'Panel-Diskussion · 8 Aufgaben' }
]

type SessionRow = {
  quiz_id: string
  title: string
  kind: 'full_exam' | 'single_teil'
  num_teile: number
  teil_label: string | null
  num_questions: number
  generated_at: string | null
  latest_score: number | null
  taken_at: string | null
}

const sessions = ref<SessionRow[]>([])
const loadingSessions = ref(false)
const generating = ref(false)
const generationStartedAt = ref<number>(0)
const generationElapsed = ref(0)
const generationError = ref<string | null>(null)
let elapsedTimer: ReturnType<typeof setInterval> | null = null

function scoreBadgeClass(score: number): string {
  if (score >= 80) return 'text-emerald-800 dark:text-emerald-200 bg-emerald-500/15'
  if (score >= 60) return 'text-amber-800 dark:text-amber-200 bg-amber-500/15'
  return 'text-red-800 dark:text-red-200 bg-red-500/15'
}

function formatDate(iso: string | null): string {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('de-DE', { year: 'numeric', month: 'short', day: 'numeric' })
}

async function loadSessions() {
  loadingSessions.value = true
  try {
    const data = await $fetch<{ sessions: SessionRow[] }>(
      `${config.public.apiBase}/horen/${slug}/sessions`,
      { credentials: 'include' }
    )
    sessions.value = data.sessions
  } catch (e) {
    sessions.value = []
  } finally {
    loadingSessions.value = false
  }
}

async function generateExam() {
  if (generating.value) return
  generating.value = true
  generationError.value = null
  generationStartedAt.value = Date.now()
  generationElapsed.value = 0
  elapsedTimer = setInterval(() => {
    generationElapsed.value = Math.floor((Date.now() - generationStartedAt.value) / 1000)
  }, 1000)

  try {
    const created = await $fetch<{ id: string; title: string; num_questions: number; num_teile: number }>(
      `${config.public.apiBase}/horen/${slug}/quiz`,
      {
        method: 'POST',
        credentials: 'include',
        body: {}
      }
    )
    if (elapsedTimer) clearInterval(elapsedTimer)
    await navigateTo(`/horen/play/${created.id}`)
  } catch (e: any) {
    generationError.value = e?.data?.detail || e?.message || 'Generierung fehlgeschlagen. Bitte erneut versuchen.'
    generating.value = false
    if (elapsedTimer) clearInterval(elapsedTimer)
  }
}

onMounted(() => {
  loadSessions()
})

onUnmounted(() => {
  if (elapsedTimer) clearInterval(elapsedTimer)
})
</script>
