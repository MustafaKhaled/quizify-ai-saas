// frontend/admin/app/middleware/auth.global.ts
export default defineNuxtRouteMiddleware(async (to) => {
  const { loggedIn, session, clear, fetch } = useUserSession()
  const config = useRuntimeConfig()

  // 1. ALLOW API and Login page to bypass entirely
  if (to.path.startsWith('/api/') || to.path === '/login') {
    return
  }

  // 2. Allow the login page itself
  if (to.path === '/login') {
    return
  }

  // 2. Sync session state
  await fetch()

  // 3. PROTECT: If not logged in, redirect to login
  if (!loggedIn.value || !session.value?.token) {
    console.log('User not logged in, redirecting...')
    return navigateTo('/login')
  }

  // 4. VERIFY: If logged in, check token with FastAPI
  try {
    await $fetch(`${config.public.apiBase}/auth/verify`, {
      headers: { Authorization: `Bearer ${session.value.token}` }
    })
  } catch (error) {
    console.error('FastAPI verification failed')
    await clear()
    return navigateTo('/login')
  }
})