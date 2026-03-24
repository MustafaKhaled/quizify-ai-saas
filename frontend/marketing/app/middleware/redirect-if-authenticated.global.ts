export default defineNuxtRouteMiddleware(async (to, from) => {
  // Only run on client side
  if (process.server) {
    return
  }

  // Check for auth token
  const token = localStorage.getItem('auth_token')

  if (!token) {
    return // No token, allow access to marketing site
  }

  // Validate token with API
  const config = useRuntimeConfig()
  try {
    await $fetch(`${config.public.apiBase}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    // Token is valid, redirect to dashboard
    const dashboardUrl = config.public.dashboardUrl || 'http://localhost:3001'
    window.location.href = `${dashboardUrl}?token=${token}`

  } catch (error) {
    // Token is invalid, remove it and allow access to marketing site
    localStorage.removeItem('auth_token')
  }
})
