export default defineNuxtRouteMiddleware(async (to) => {
  if (import.meta.server) return

  const publicPages = ['/auth/login', '/auth/register', '/verify-email']
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
    const user = await $fetch<{ is_verified?: boolean }>(`${apiBase}/auth/verify`, {
      credentials: 'include'
    })

    if (user && user.is_verified === false) {
      return navigateTo('/verify-email', { replace: true })
    }
  } catch {
    window.location.href = `${marketingUrl}/login`
  }
})
