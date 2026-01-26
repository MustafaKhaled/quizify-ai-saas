export default eventHandler(async (event) => {
  const session = await getUserSession(event)
  const config = useRuntimeConfig()

  if (!session.token) {
    throw createError({
      statusCode: 401,
      message: 'Unauthorized'
    })
  }

  const formData = await readMultipartFormData(event)

  if (!formData) {
    throw createError({
      statusCode: 400,
      message: 'No form data provided'
    })
  }

  try {
    // Convert multipart form data to FormData for backend
    const backendFormData = new FormData()
    
    for (const part of formData) {
      if (part.name === 'file' && part.filename) {
        backendFormData.append('file', new Blob([part.data]), part.filename)
      } else if (part.data) {
        backendFormData.append(part.name, part.data.toString())
      }
    }

    const quiz = await $fetch(`${config.public.apiBase}/quizzes/create`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${session.token}`
      },
      body: backendFormData
    })

    return quiz
  } catch (err: any) {
    throw createError({
      statusCode: err?.response?.status || 500,
      message: err?.response?._data?.detail || 'Failed to create quiz'
    })
  }
})
