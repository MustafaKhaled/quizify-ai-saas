export default defineNuxtRouteMiddleware(async (to) => {
  // Only run on client side
  if (process.server) {
    return
  }

  // Only redirect away from login/signup if already authenticated
  const authOnlyPages = ['/login', '/signup']
  if (!authOnlyPages.includes(to.path)) {
    return
  }

  const token = localStorage.getItem('auth_token')
  if (!token) {
    return
  }

  const config = useRuntimeConfig()

  try {
    await $fetch(`${config.public.apiBase}/auth/verify`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    // Token is valid — redirect to dashboard
    const dashboardUrl = config.public.dashboardUrl || 'http://localhost:3001'
    window.location.href = `${dashboardUrl}?token=${token}`
  } catch {
    // Token is invalid or blacklisted — clean up and stay on page
    localStorage.removeItem('auth_token')
  }
})
