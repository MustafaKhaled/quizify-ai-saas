export default eventHandler(async (event) => {
  const session = await getUserSession(event)
  const config = useRuntimeConfig()

  if (!session.token) {
    throw createError({
      statusCode: 401,
      message: 'Unauthorized'
    })
  }

  try {
    const sources = await $fetch(`${config.public.apiBase}/quizzes/sources`, {
      headers: {
        Authorization: `Bearer ${session.token}`
      }
    })

    return sources
  } catch (err: any) {
    throw createError({
      statusCode: err?.response?.status || 500,
      message: err?.response?._data?.detail || 'Failed to fetch sources'
    })
  }
})
