<template>
  <UDashboardPanel grow>
    <UDashboardNavbar class="lg:hidden" title="New Subject" />
    <UDashboardPanelContent class="p-4 sm:p-6 overflow-y-auto bg-mesh min-h-full">
      <div>
        <div class="mb-6 sm:mb-8">
          <NuxtLink to="/subjects" class="text-sm text-blue-600 hover:underline">← Back to Subjects</NuxtLink>
          <h1 class="text-2xl sm:text-4xl font-bold gradient-text mt-2">New Subject</h1>
        </div>

        <div class="glass-card rounded-2xl p-4 sm:p-6">
          <form @submit.prevent="createSubject" class="space-y-6">
            <!-- Quick Pick -->
            <div>
              <label class="block text-sm font-medium text-slate-900 dark:text-white mb-2">Quick pick</label>
              <div class="flex flex-wrap gap-3">
                <button
                  v-for="preset in presets"
                  :key="preset.name"
                  type="button"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl border-2 transition-all hover:scale-[1.02]"
                  :class="name.trim() === preset.name
                    ? 'border-transparent text-white shadow-lg'
                    : 'border-white/30 dark:border-white/10 bg-white/40 dark:bg-white/5 text-slate-900 dark:text-white'"
                  :style="name.trim() === preset.name ? { backgroundColor: preset.color } : {}"
                  @click="applyPreset(preset)"
                >
                  <span class="text-lg">{{ preset.icon }}</span>
                  <span class="font-semibold text-sm">{{ preset.name }}</span>
                </button>
                <button
                  type="button"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl border-2 border-dashed transition-all hover:scale-[1.02]"
                  :class="isCustom
                    ? 'border-blue-500 bg-blue-500/10 text-blue-700 dark:text-blue-300'
                    : 'border-white/30 dark:border-white/10 text-slate-600 dark:text-slate-300'"
                  @click="clearPreset"
                >
                  <UIcon name="i-lucide-pencil" class="w-4 h-4" />
                  <span class="font-semibold text-sm">Custom</span>
                </button>
              </div>
            </div>

            <!-- Name -->
            <div>
              <label class="block text-sm font-medium text-slate-900 dark:text-white mb-2">Subject Name *</label>
              <input
                v-model="name"
                type="text"
                placeholder="e.g. Organic Chemistry, World History"
                required
                class="w-full px-4 py-2 glass-input rounded-xl text-slate-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <!-- Color -->
            <div>
              <label class="block text-sm font-medium text-slate-900 dark:text-white mb-2">Color</label>
              <div class="flex gap-3 flex-wrap">
                <button
                  v-for="c in palette"
                  :key="c"
                  type="button"
                  class="w-8 h-8 rounded-full border-2 transition-transform hover:scale-110"
                  :style="{ backgroundColor: c }"
                  :class="color === c ? 'border-gray-900 dark:border-white scale-110' : 'border-transparent'"
                  @click="color = c"
                ></button>
              </div>
            </div>

            <!-- Preview -->
            <div class="rounded-xl overflow-hidden border border-white/20 dark:border-white/10">
              <div class="h-2" :style="{ backgroundColor: color }"></div>
              <div class="p-4 bg-gray-50 dark:bg-gray-700/50">
                <p class="font-bold text-slate-900 dark:text-white">{{ name || 'Subject Name' }}</p>
                <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">0 sources • 0 quizzes</p>
              </div>
            </div>

            <button
              type="submit"
              :disabled="isSaving || !name.trim()"
              class="w-full py-2 btn-gradient rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {{ isSaving ? 'Creating...' : 'Create Subject' }}
            </button>
          </form>
        </div>
      </div>
    </UDashboardPanelContent>
  </UDashboardPanel>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })

const config = useRuntimeConfig()

const name = ref('')
const color = ref('#3B82F6')
const isSaving = ref(false)

const palette = [
  '#3B82F6', '#8B5CF6', '#EC4899', '#EF4444',
  '#F97316', '#EAB308', '#22C55E', '#14B8A6',
  '#06B6D4', '#6366F1',
]

const presets = [
  { name: 'PMP', color: '#F97316', icon: '📋' }
]

const isCustom = computed(() => !presets.some(p => p.name === name.value.trim()))

function applyPreset(preset: { name: string, color: string }) {
  name.value = preset.name
  color.value = preset.color
}

function clearPreset() {
  if (presets.some(p => p.name === name.value.trim())) {
    name.value = ''
  }
}

const createSubject = async () => {
  if (!name.value.trim()) return
  isSaving.value = true
  try {
    const res = await fetch(`${config.public.apiBase}/subjects`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name.value.trim(), color: color.value }),
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const subject = await res.json()
    await navigateTo(`/subjects/${subject.id}`, { replace: true })
  } catch (e: any) {
    alert(e?.message || 'Failed to create subject')
  } finally {
    isSaving.value = false
  }
}
</script>
