export default defineNuxtRouteMiddleware(async (to, from) => {
  // Only run on client side
  if (process.server) {
    return
  }

  // Check for auth token
  const token = localStorage.getItem('auth_token')
  const config = useRuntimeConfig()
  const marketingUrl = config.public.marketingUrl || 'http://localhost:3000'

  if (!token) {
    // No token, redirect to marketing login
    window.location.href = `${marketingUrl}/login`
    return
  }

  // Validate token with API
  try {
    await $fetch(`${config.public.apiBase}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    // Token is valid, allow access
  } catch (error) {
    // Token is invalid or expired, clear it and redirect to login
    localStorage.removeItem('auth_token')
    window.location.href = `${marketingUrl}/login`
  }
})
