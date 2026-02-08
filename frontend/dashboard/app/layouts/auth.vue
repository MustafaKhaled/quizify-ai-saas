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
  <div :class="isDark ? 'dark' : ''" class="min-h-screen bg-white dark:bg-gray-900 transition-colors">
    <div class="min-h-screen flex items-center justify-center px-4 py-6">
      <div class="w-full">
        <!-- Header with Logo and Dark Mode Toggle -->
        <div class="flex justify-between items-center mb-12">
          <NuxtLink to="/" class="text-2xl font-bold text-blue-600 dark:text-blue-400">
            Quizify AI
          </NuxtLink>
          <button
            @click="toggleDarkMode"
            class="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
          >
            {{ isDark ? '☀️' : '🌙' }}
          </button>
        </div>

        <!-- Content -->
        <slot />

        <!-- Footer -->
        <div class="mt-12 text-center text-gray-600 dark:text-gray-400 text-sm">
          <p>© 2024 Quizify AI. All rights reserved.</p>
        </div>
      </div>
    </div>
  </div>
</template>
