export default defineNuxtRouteMiddleware(async (to) => {
  // Allow login & API routes
  if (to.path === '/login' || to.path.startsWith('/api/')) return

  const { loggedIn, fetch } = useUserSession()

  // Sync session ONCE
  await fetch()

  // Protect route
  if (!loggedIn.value) {
    return navigateTo('/login')
  }
})
