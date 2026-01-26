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
    const quizzes = await $fetch(`${config.public.apiBase}/quizzes/my_quizzes`, {
      headers: {
        Authorization: `Bearer ${session.token}`
      }
    })

    return quizzes
  } catch (err: any) {
    throw createError({
      statusCode: err?.response?.status || 500,
      message: err?.response?._data?.detail || 'Failed to fetch quizzes'
    })
  }
})
