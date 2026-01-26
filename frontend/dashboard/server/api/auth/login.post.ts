export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const config = useRuntimeConfig()

  if (!body?.email || !body?.password) {
    throw createError({
      statusCode: 400,
      message: 'Email and password are required'
    })
  }

  try {
    // FastAPI OAuth2 login
    const formData = new URLSearchParams()
    formData.append('username', body.email)
    formData.append('password', body.password)

    const data: any = await $fetch(`${config.public.apiBase}/auth/login`, {
      method: 'POST',
      body: formData
    })

    if (!data.access_token || !data.user) {
      throw createError({ statusCode: 401, message: 'Invalid credentials' })
    }

    // Set user session
    await setUserSession(event, {
      user: {
        id: data.user.id,
        email: data.user.email,
        name: data.user.name,
        subscription: data.user.subscription
      },
      token: data.access_token,
      loggedInAt: Date.now()
    })

    return { success: true }
  } catch (err: any) {
    throw createError({
      statusCode: err?.response?.status || 401,
      message: err?.response?._data?.detail || 'Invalid email or password'
    })
  }
})
