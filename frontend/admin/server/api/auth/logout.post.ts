// server/api/auth/logout.post.ts
export default defineEventHandler(async (event) => {
  // 1. (Optional) Get the current token to tell FastAPI to revoke it
  const session = await getUserSession(event)
  const config = useRuntimeConfig()

  if (session.token) {
    try {
      // Notify FastAPI to invalidate the JWT
      await $fetch(`${config.public.apiBase}/auth/logout`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${session.token}` }
      })
    } catch (err) {
      // We don't block logout if the backend fails
      console.error('FastAPI logout failed, but clearing local session anyway.')
    }
  }

  // 2. This is the "Magic" line that deletes the cookie
  await clearUserSession(event)

  return { success: true }
})