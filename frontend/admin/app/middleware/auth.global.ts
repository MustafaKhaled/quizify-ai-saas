// frontend/admin/app/middleware/auth.global.ts
export default defineNuxtRouteMiddleware(async (to) => {
  // Allow login & API routes
  if (to.path === '/login' || to.path.startsWith('/api/')) return

  const { loggedIn, fetch } = useUserSession()

  // Sync session ONCE
  await fetch()

  // Protect route
  if (!loggedIn.value) {
    console.log('User not logged in, redirecting...')
    return navigateTo('/login')
  }
})
