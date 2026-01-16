// app/middleware/auth.global.ts
export default defineNuxtRouteMiddleware(async (to) => {
  const { loggedIn, session, clear, fetch } = useUserSession()
  const config = useRuntimeConfig()

  console.log('Checking Auth for:', to.path)

  // 1. Refresh session from the server-side cookie
  await fetch()

  console.log('Current loggedIn status:', loggedIn.value)
  console.log('Current session data:', session.value)

  // 2. Scenario: User IS logged in
  if (loggedIn.value && session.value?.token) {
    try {
      // Verify token with FastAPI
      const user: any = await $fetch(`${config.public.apiBase}/auth/verify`, {
        headers: { Authorization: `Bearer ${session.value.token}` }
      })

      // If user is at /login but already verified, send to home
      if (to.path === '/login') {
        return navigateTo('/')
      }
    } catch (error) {
      console.error('Token expired or invalid. Clearing session.')
      await clear()
      if (to.path !== '/login') {
        return navigateTo('/login')
      }
    }
  } 
  
  // 3. Scenario: User is NOT logged in
  else {
    // Only redirect if they aren't already on the login page
    if (to.path !== '/login') {
      console.log('Redirecting guest to /login')
      return navigateTo('/login')
    }
  }
})