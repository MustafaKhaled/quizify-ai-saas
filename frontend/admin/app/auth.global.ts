// middleware/auth.global.ts
export default defineNuxtRouteMiddleware(async (to, from) => {
    // Get the real login status from nuxt-auth-utils
    const { loggedIn, fetch } = useUserSession()
    
    // Ensure we have the latest session state
    await fetch()
  
    // 1. If user is NOT logged in and trying to access a protected page
    if (!loggedIn.value && to.path !== '/login') {
      return navigateTo('/login')
    }
  
    // 2. If user IS logged in and trying to go to the login page
    if (loggedIn.value && to.path === '/login') {
      return navigateTo('/')
    }
  })