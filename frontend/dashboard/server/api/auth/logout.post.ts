export default defineEventHandler(async (event) => {
  const session = await getUserSession(event)
  const config = useRuntimeConfig()

  if (session.token) {
    try {
      await $fetch(`${config.public.apiBase}/auth/logout`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${session.token}` }
      })
    } catch (err) {
      console.error('FastAPI logout failed, but clearing local session anyway.')
    }
  }

  await clearUserSession(event)
  return { success: true }
})
