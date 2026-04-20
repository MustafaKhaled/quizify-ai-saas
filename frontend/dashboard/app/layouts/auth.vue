<script setup lang="ts">
const isDark = ref(false)

const toggleDarkMode = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme', 'dark')
    }
  } else {
    document.documentElement.classList.remove('dark')
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme', 'light')
    }
  }
}

onMounted(() => {
  const savedTheme = typeof window !== 'undefined' ? localStorage.getItem('theme') : null
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  isDark.value = savedTheme === 'dark' || (savedTheme === null && prefersDark)
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  }
})
</script>

<template>
  <div :class="isDark ? 'dark' : ''" class="min-h-screen bg-mesh transition-colors">
    <div class="min-h-screen flex items-center justify-center px-4 py-6">
      <div class="w-full">
        <!-- Header with Logo and Dark Mode Toggle -->
        <div class="flex justify-between items-center mb-12">
          <NuxtLink to="/" class="text-2xl font-bold gradient-text">
            Quizify AI
          </NuxtLink>
          <button
            @click="toggleDarkMode"
            class="p-2 glass-card rounded-xl text-slate-600 dark:text-slate-300 hover:shadow-lg transition-all"
          >
            <UIcon :name="isDark ? 'i-lucide-sun' : 'i-lucide-moon'" class="w-5 h-5" />
          </button>
        </div>

        <!-- Content -->
        <slot />

        <!-- Footer -->
        <div class="mt-12 text-center text-slate-500 dark:text-slate-400 text-sm">
          <p>&copy; 2024 Quizify AI. All rights reserved.</p>
        </div>
      </div>
    </div>
  </div>
</template>
