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
  const { email } = body

  if (!email) {
    throw createError({
      statusCode: 400,
      message: 'Email is required'
    })
  }

  try {
    await $fetch(`${config.public.apiBase}/admin/user/email/${encodeURIComponent(email)}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${session.token}`
      }
    })

    return { success: true }
  } catch (err: any) {
    throw createError({
      statusCode: err?.response?.status || 500,
      message: err?.response?._data?.detail || 'Failed to delete user'
    })
  }
})
