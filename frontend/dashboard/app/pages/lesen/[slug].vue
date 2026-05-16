<template>
  <UDashboardPanel grow>
    <UDashboardNavbar class="lg:hidden" :title="`${levelMeta.shortLabel} Lesen`" />
    <UDashboardPanelContent class="p-4 sm:p-6 overflow-y-auto bg-mesh min-h-full">

      <h1 class="text-2xl sm:text-3xl font-bold mb-1">
        <span class="gradient-text">{{ levelMeta.title }}</span>
      </h1>
      <p class="text-sm text-slate-500 dark:text-slate-400 mb-8">
        Generate a fresh full Goethe-Zertifikat {{ levelMeta.shortLabel }} reading exam (all five Teile),
        or replay a previous exam.
      </p>

      <!-- Generate new exam -->
      <div class="mb-10">
        <h2 class="text-lg font-bold text-slate-900 dark:text-white mb-3">Neue Prüfung generieren</h2>
        <p class="text-xs text-slate-500 dark:text-slate-400 mb-4">
          Eine vollständige Leseprüfung enthält alle fünf Teile.
          Die Generierung dauert etwa 10–20 Sekunden (Gemini-Texte für jeden Teil parallel).
        </p>

        <div class="glass-card rounded-2xl p-5 mb-3 max-w-3xl">
          <ul class="text-xs text-slate-600 dark:text-slate-400 space-y-1.5 mb-4">
            <li v-for="t in TEILE_META" :key="t.teil" class="flex items-start gap-2">
              <UIcon name="i-lucide-book-open" class="w-3.5 h-3.5 mt-0.5 text-violet-600" />
              <span>
                <span class="font-semibold text-slate-700 dark:text-slate-300">Teil {{ t.teil }}</span>
                — {{ t.name }} · {{ t.format_hint }}
              </span>
            </li>
          </ul>

          <div v-if="quota" class="mb-3 flex items-center justify-between gap-2">
            <span
              :class="quotaBadgeClass"
              class="px-2.5 py-1 rounded-full text-xs font-semibold inline-flex items-center gap-1.5"
            >
              <UIcon name="i-lucide-gauge" class="w-3.5 h-3.5" />
              {{ quotaLabel }}
            </span>
          </div>
          <p v-if="generateDisabledReason" class="text-xs text-red-700 dark:text-red-300 mb-3">
            {{ generateDisabledReason }}
          </p>

          <button
            @click="generateExam"
            :disabled="generating || !quota?.can_generate"
            class="w-full px-4 py-3 btn-gradient rounded-xl font-semibold text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <template v-if="generating">
              Generiert… {{ generationElapsed }}s
            </template>
            <template v-else-if="quota && !quota.can_generate">
              Limit erreicht
            </template>
            <template v-else>
              Vollständige Prüfung generieren ({{ levelMeta.durationLabel }})
            </template>
          </button>

          <!-- Upgrade CTA — only shown when the limit is something an upgrade
               would fix (trial limit, no subscription). Pro users at their
               weekly cap see the wait-time message above instead. -->
          <button
            v-if="canUpgradeFromHere"
            @click="showSubscriptionModal = true"
            class="mt-3 w-full px-4 py-2.5 rounded-xl text-sm font-semibold border-2 border-violet-500 text-violet-700 dark:text-violet-300 hover:bg-violet-50 dark:hover:bg-violet-950/30 transition"
          >
            Upgrade auf Pro für mehr Prüfungen →
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
                <span class="text-xs uppercase tracking-wide font-semibold text-violet-700 dark:text-violet-300">
                  {{ s.num_teile }} Teile
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
              :to="`/lesen/play/${s.quiz_id}`"
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
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-violet-500 mx-auto mb-4"></div>
          <h3 class="text-lg font-bold mb-2">Generiere Prüfung…</h3>
          <p class="text-sm text-slate-500 dark:text-slate-400 mb-2">
            Gemini schreibt die Texte und Aufgaben für alle fünf Teile.
          </p>
          <p class="text-xs text-slate-400">~15 Sekunden · {{ generationElapsed }}s</p>
        </div>
      </div>

    </UDashboardPanelContent>

    <!-- Subscription modal: opened by the "Upgrade auf Pro" CTA when the
         user has hit a trial cap or has no active subscription. -->
    <SubscriptionModal v-model="showSubscriptionModal" />
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })

const route = useRoute()
const config = useRuntimeConfig()
const slug = route.params.slug as string

const LEVEL_META = {
  deutsch_b1_lesen: {
    title: 'German B1 — Lesen',
    shortLabel: 'B1',
    durationLabel: '~15 Sek.',
    teile: [
      { teil: 1, name: 'Blogeintrag', format_hint: 'Blog-Text · 6 Richtig/Falsch-Aufgaben' },
      { teil: 2, name: 'Zeitungsartikel', format_hint: '2 Artikel · 6 Aufgaben (3+3)' },
      { teil: 3, name: 'Anzeigen-Zuordnung', format_hint: '10 Anzeigen · 7 Situationen (Buchstabe a–j oder 0)' },
      { teil: 4, name: 'Leserkommentare', format_hint: '7 Kommentare · 7 Ja/Nein-Aufgaben' },
      { teil: 5, name: 'Anweisungen', format_hint: 'Hausordnung o.ä. · 4 Aufgaben' }
    ]
  },
  deutsch_a2_lesen: {
    title: 'German A2 — Lesen',
    shortLabel: 'A2',
    durationLabel: '~10 Sek.',
    teile: [
      { teil: 1, name: 'Zeitungstext', format_hint: 'Kurzer Artikel · 5 Aufgaben (a/b/c)' },
      { teil: 2, name: 'Wegweiser', format_hint: 'Kaufhaus o.ä. · 5 Stockwerk-Aufgaben' },
      { teil: 3, name: 'E-Mail', format_hint: 'Persönliche E-Mail · 5 Aufgaben (a/b/c)' },
      { teil: 4, name: 'Anzeigen-Zuordnung', format_hint: '6 Anzeigen · 5 Situationen (Buchstabe a–f oder X)' }
    ]
  }
} as const

type LevelKey = keyof typeof LEVEL_META
const levelMeta = computed(() => LEVEL_META[slug as LevelKey] ?? LEVEL_META.deutsch_b1_lesen)
const TEILE_META = computed(() => levelMeta.value.teile)

type SessionRow = {
  quiz_id: string
  title: string
  num_teile: number
  num_questions: number
  generated_at: string | null
  latest_score: number | null
  taken_at: string | null
}

type LesenQuota = {
  tier: 'pro' | 'trial' | 'expired'
  limit: number
  used: number
  remaining: number
  period: 'week' | 'trial' | 'none'
  can_generate: boolean
  reason: 'weekly_limit_reached' | 'trial_limit_reached' | 'subscription_required' | null
  next_available_at: string | null
}

const sessions = ref<SessionRow[]>([])
const loadingSessions = ref(false)
const generating = ref(false)
const generationStartedAt = ref<number>(0)
const generationElapsed = ref(0)
const generationError = ref<string | null>(null)
const quota = ref<LesenQuota | null>(null)
const showSubscriptionModal = ref(false)
let elapsedTimer: ReturnType<typeof setInterval> | null = null

// Show upgrade CTA when an upgrade would fix the limit (trial / no-sub).
// Pro users at the weekly cap see only the wait-time message above.
const canUpgradeFromHere = computed(() => {
  const q = quota.value
  if (!q) return false
  return q.reason === 'trial_limit_reached' || q.reason === 'subscription_required'
})

const quotaLabel = computed<string>(() => {
  const q = quota.value
  if (!q) return ''
  if (q.tier === 'expired') return 'Pro-Abo erforderlich'
  const periodWord = q.period === 'week' ? 'in den letzten 7 Tagen' : 'in der Probezeit'
  return `${q.remaining} von ${q.limit} ${q.limit === 1 ? 'Prüfung' : 'Prüfungen'} ${periodWord} übrig`
})

const quotaBadgeClass = computed<string>(() => {
  const q = quota.value
  if (!q) return 'bg-slate-500/10 text-slate-700 dark:text-slate-300'
  if (!q.can_generate) return 'bg-red-500/10 text-red-700 dark:text-red-300'
  if (q.remaining <= 2) return 'bg-amber-500/10 text-amber-800 dark:text-amber-300'
  return 'bg-violet-500/10 text-violet-700 dark:text-violet-300'
})

function formatNextAvailable(iso: string | null): string {
  if (!iso) return ''
  const target = new Date(iso)
  const diffMs = target.getTime() - Date.now()
  if (diffMs <= 0) return 'jetzt'
  const hours = Math.floor(diffMs / 3600_000)
  if (hours >= 24) {
    const days = Math.floor(hours / 24)
    const remainHours = hours % 24
    return remainHours > 0 ? `in ${days}d ${remainHours}h` : `in ${days} Tag${days === 1 ? '' : 'en'}`
  }
  if (hours >= 1) return `in ${hours} Stunde${hours === 1 ? '' : 'n'}`
  const minutes = Math.max(1, Math.floor(diffMs / 60_000))
  return `in ${minutes} Minute${minutes === 1 ? '' : 'n'}`
}

const generateDisabledReason = computed<string | null>(() => {
  const q = quota.value
  if (!q || q.can_generate) return null
  if (q.reason === 'weekly_limit_reached') {
    const when = formatNextAvailable(q.next_available_at)
    const suffix = when ? ` Nächste Prüfung wieder verfügbar ${when}.` : ''
    return `Wochenlimit erreicht (${q.limit} Prüfungen in 7 Tagen).${suffix}`
  }
  if (q.reason === 'trial_limit_reached') {
    return 'Probezeit-Limit erreicht. Upgrade auf Pro für 10 Lese-Prüfungen pro Woche.'
  }
  if (q.reason === 'subscription_required') {
    return 'Lesen erfordert ein aktives Abo. Upgrade auf Pro, um Prüfungen zu generieren.'
  }
  return null
})

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
      `${config.public.apiBase}/lesen/${slug}/sessions`,
      { credentials: 'include' }
    )
    sessions.value = data.sessions
  } catch (e) {
    sessions.value = []
  } finally {
    loadingSessions.value = false
  }
}

async function loadQuota() {
  try {
    quota.value = await $fetch<LesenQuota>(
      `${config.public.apiBase}/lesen/${slug}/quota`,
      { credentials: 'include' }
    )
  } catch (e) {
    quota.value = null
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
      `${config.public.apiBase}/lesen/${slug}/quiz`,
      {
        method: 'POST',
        credentials: 'include',
        body: {}
      }
    )
    if (elapsedTimer) clearInterval(elapsedTimer)
    await navigateTo(`/lesen/play/${created.id}`)
  } catch (e: any) {
    generationError.value = e?.data?.detail || e?.message || 'Generierung fehlgeschlagen. Bitte erneut versuchen.'
    generating.value = false
    if (elapsedTimer) clearInterval(elapsedTimer)
  }
}

onMounted(() => {
  loadSessions()
  loadQuota()
})

onUnmounted(() => {
  if (elapsedTimer) clearInterval(elapsedTimer)
})
</script>
