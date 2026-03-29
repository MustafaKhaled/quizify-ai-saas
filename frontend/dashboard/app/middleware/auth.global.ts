export default defineNuxtRouteMiddleware(async (to) => {
  if (import.meta.server) return

  const publicPages = ['/auth/login', '/auth/register']
  if (publicPages.includes(to.path)) return

  const config = useRuntimeConfig()
  const marketingUrl = config.public.marketingUrl || 'http://localhost:3000'
  const apiBase = config.public.apiBase || 'http://localhost:8000'

  // Exchange Google OAuth handoff code for a cookie via credentialed fetch
  const code = to.query.code as string | undefined
  if (code) {
    try {
      await $fetch(`${apiBase}/auth/exchange`, {
        method: 'POST',
        credentials: 'include',
        body: { code }
      })
    } catch {
      window.location.href = `${marketingUrl}/login`
      return
    }
    return navigateTo({ path: to.path, query: {} }, { replace: true })
  }

  try {
    await $fetch(`${apiBase}/auth/verify`, {
      credentials: 'include'
    })
  } catch {
    window.location.href = `${marketingUrl}/login`
  }
})
