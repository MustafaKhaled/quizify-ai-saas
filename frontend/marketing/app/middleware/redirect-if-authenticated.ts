export default defineNuxtRouteMiddleware(async (to, from) => {
  // Only run on client side
  if (process.server) {
    return
  }

  // Pages that should redirect if user is already authenticated
  const authPages = ['/', '/login', '/signup']

  if (!authPages.includes(to.path)) {
    return
  }

  // Check for auth token
  const token = localStorage.getItem('auth_token')

  if (!token) {
    return // No token, allow access
  }

  // Validate token with API
  const config = useRuntimeConfig()
  try {
    await $fetch(`${config.public.apiBase}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    // Token is valid, redirect to dashboard with token
    const dashboardUrl = config.public.dashboardUrl || 'http://localhost:3001'
    window.location.href = `${dashboardUrl}?token=${token}`

  } catch (error) {
    // Token is invalid, remove it and allow access to auth pages
    localStorage.removeItem('auth_token')
  }
})
