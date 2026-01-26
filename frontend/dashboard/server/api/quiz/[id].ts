export default eventHandler(async (event) => {
  const session = await getUserSession(event)
  const config = useRuntimeConfig()
  const quizId = getRouterParam(event, 'id')

  if (!session.token) {
    throw createError({
      statusCode: 401,
      message: 'Unauthorized'
    })
  }

  try {
    const quizzes = await $fetch(`${config.public.apiBase}/quizzes/${quizId}`, {
      headers: {
        Authorization: `Bearer ${session.token}`
      }
    })

    // Backend returns an array, get first item
    return Array.isArray(quizzes) ? quizzes[0] : quizzes
  } catch (err: any) {
    throw createError({
      statusCode: err?.response?.status || 500,
      message: err?.response?._data?.detail || 'Failed to fetch quiz'
    })
  }
})
