export default defineNuxtRouteMiddleware((to, from) => {
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
  const dashboardUrl = config.public.dashboardUrl || 'http://localhost:3001'
  window.location.href = `${dashboardUrl}?token=${token}`
})
