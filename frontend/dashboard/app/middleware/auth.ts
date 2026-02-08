export default defineNuxtRouteMiddleware((to, from) => {
  // Allow access to auth pages without token
  if (to.path.startsWith('/auth/')) {
    return
  }

  // Check for auth token
  const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
  
  if (!token) {
    return navigateTo('/auth/login')
  }
})
