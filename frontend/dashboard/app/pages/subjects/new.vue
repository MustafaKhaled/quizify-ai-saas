<template>
  <UDashboardPanel grow>
    <UDashboardPanelContent class="p-6 overflow-y-auto">
      <div>
        <div class="mb-8">
          <NuxtLink to="/subjects" class="text-sm text-blue-600 hover:underline">← Back to Subjects</NuxtLink>
          <h1 class="text-4xl font-bold text-gray-900 dark:text-white mt-2">New Subject</h1>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-6">
          <form @submit.prevent="createSubject" class="space-y-6">
            <!-- Name -->
            <div>
              <label class="block text-sm font-medium text-gray-900 dark:text-white mb-2">Subject Name *</label>
              <input
                v-model="name"
                type="text"
                placeholder="e.g. Organic Chemistry, World History"
                required
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <!-- Color -->
            <div>
              <label class="block text-sm font-medium text-gray-900 dark:text-white mb-2">Color</label>
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
            <div class="rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700">
              <div class="h-2" :style="{ backgroundColor: color }"></div>
              <div class="p-4 bg-gray-50 dark:bg-gray-700/50">
                <p class="font-bold text-gray-900 dark:text-white">{{ name || 'Subject Name' }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">0 sources • 0 quizzes</p>
              </div>
            </div>

            <button
              type="submit"
              :disabled="isSaving || !name.trim()"
              class="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
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
