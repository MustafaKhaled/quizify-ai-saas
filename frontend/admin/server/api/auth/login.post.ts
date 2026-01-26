// frontend/admin/server/api/auth/login.post.ts
export default defineEventHandler(async (event) => {
  console.log('🔥 NUXT LOGIN API HIT')
  console.log('Password check:', process.env.NUXT_SESSION_PASSWORD?.length)
  const body = await readBody(event)
  console.log('📦 BODY:', body)
  const config = useRuntimeConfig()

  if (!body?.email || !body?.password) {
    throw createError({
      statusCode: 400,
      message: 'Email and password are required'
    })
  }

  console.log('config url is ', config.public.apiBase)

  try {
    // 1️⃣ FastAPI OAuth2 login
    const formData = new URLSearchParams()
    formData.append('username', body.email)
    formData.append('password', body.password)

    const data: any = await $fetch(`${config.public.apiBase}/auth/login`, {
      method: 'POST',
      body: formData
    })

    console.log('✅ FastAPI Response:', data)

    // 1. Check for the token and user in the response
    if (!data.access_token || !data.user) {
       console.error('❌ Login failed: No access token or user in response')
       throw createError({ statusCode: 401, message: 'Invalid credentials' })
    }

    // 2. Check if user is admin
    if (!data.user.is_admin) {
      throw createError({ statusCode: 403, message: 'Admin access required' })
    }

    // 3. Map the FastAPI response into the Nuxt Session structure
    await setUserSession(event, {
      user: {
        id: data.user.id,
        email: data.user.email,
        name: data.user.name,
        is_admin: data.user.is_admin
      },
      token: data.access_token,
      loggedInAt: Date.now()
    })

    console.log('✅ Session sealed for:', data.user.email)
    return { success: true }
  } catch (err: any) {
    // Forward FastAPI error if available
    console.log("catch error", err)
    throw createError({
      statusCode: err?.response?.status || 401,
      message: err?.response?._data?.detail || 'Invalid email or password'
    })
  }
})
