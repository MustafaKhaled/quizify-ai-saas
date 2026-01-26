export default eventHandler(async (event) => {
  const session = await getUserSession(event)
  const config = useRuntimeConfig()

  if (!session.token) {
    throw createError({
      statusCode: 401,
      message: 'Unauthorized'
    })
  }

  const body = await readBody(event)
  const quizId = body.quiz_id

  if (!quizId) {
    throw createError({
      statusCode: 400,
      message: 'Quiz ID is required'
    })
  }

  try {
    const result = await $fetch(`${config.public.apiBase}/quizzes/submit/${quizId}`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${session.token}`
      },
      body: {
        quiz_id: quizId,
        answers: body.answers,
        time_taken_seconds: body.time_taken_seconds
      }
    })

    return result
  } catch (err: any) {
    throw createError({
      statusCode: err?.response?.status || 500,
      message: err?.response?._data?.detail || 'Failed to submit quiz'
    })
  }
})
