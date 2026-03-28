export default defineNuxtRouteMiddleware(async (to) => {
  // Only run on client side
  if (import.meta.server) {
    return
  }

  // Skip auth check for auth pages
  const publicPages = ['/auth/login', '/auth/register']
  if (publicPages.includes(to.path)) {
    return
  }

  const token = localStorage.getItem('auth_token')
  const config = useRuntimeConfig()
  const marketingUrl = config.public.marketingUrl || 'http://localhost:3000'

  if (!token) {
    window.location.href = `${marketingUrl}/login`
    return
  }

  try {
    await $fetch(`${config.public.apiBase}/auth/verify`, {
      headers: { Authorization: `Bearer ${token}` }
    })
  } catch {
    localStorage.removeItem('auth_token')
    window.location.href = `${marketingUrl}/login`
  }
})
