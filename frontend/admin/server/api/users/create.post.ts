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

  if (!body.email || !body.name) {
    throw createError({
      statusCode: 400,
      message: 'Email and name are required'
    })
  }

  try {
    const user = await $fetch(`${config.public.apiBase}/auth/register`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${session.token}`
      },
      body: {
        email: body.email,
        name: body.name,
        password: body.password || `TempPass${Math.random().toString(36).slice(-8)}`,
        is_admin: body.is_admin || false
      }
    })

    return { success: true, user }
  } catch (err: any) {
    throw createError({
      statusCode: err?.response?.status || 500,
      message: err?.response?._data?.detail || 'Failed to create user'
    })
  }
})
