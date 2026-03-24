export default defineNuxtRouteMiddleware((to, from) => {
  // Only run on client side
  if (process.server) {
    return
  }

  // If a token exists, redirect to the dashboard immediately
  const token = localStorage.getItem('auth_token')
  if (!token) {
    return
  }

  const config = useRuntimeConfig()
  const dashboardUrl = config.public.dashboardUrl || 'http://localhost:3001'
  window.location.href = `${dashboardUrl}?token=${token}`
})
