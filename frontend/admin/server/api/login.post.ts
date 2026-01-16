export default defineEventHandler(async (event) => {
    try {
      const body = await readBody(event)
      const config = useRuntimeConfig()
  
      // 1. Verify token / session with FastAPI
      const data: any = await $fetch(
        `${config.public.apiBase}/auth/verify`,
        {
          method: 'POST',
          body,
        }
      )
  
      if (!data?.access_token || !data?.user) {
        throw createError({
          statusCode: 401,
          statusMessage: 'Invalid session data',
        })
      }
  
      // 2. Persist session (Nuxt server-side cookies)
      await setUserSession(event, {
        user: data.user,
        token: data.access_token,
        loggedInAt: new Date()
      })
  
      return {
        success: true,
        user: data.user,
      }
    } catch (error) {
      throw createError({
        statusCode: 401,
        statusMessage: 'Session verification failed',
      })
    }
  })
  