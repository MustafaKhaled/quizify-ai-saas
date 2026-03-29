export default defineNuxtRouteMiddleware(async (to) => {
  if (import.meta.server) return

  const authOnlyPages = ['/login', '/signup']
  if (!authOnlyPages.includes(to.path)) return

  const config = useRuntimeConfig()

  try {
    await $fetch(`${config.public.apiBase || 'http://localhost:8000'}/auth/verify`, {
      credentials: 'include'
    })
    // Cookie is valid — redirect to dashboard
    const dashboardUrl = config.public.dashboardUrl || 'http://localhost:3001'
    window.location.href = dashboardUrl
  } catch {
    // No valid session — stay on page
  }
})
