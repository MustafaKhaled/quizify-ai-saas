// frontend/admin/server/api/auth/login.post.ts
export default defineEventHandler(async (event) => {
  console.log('🔥 NUXT LOGIN API HIT')
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

console.log('✅ FastAPI Response received')

    // 1. Only check for the token, since 'user' doesn't exist as a separate key
    if (!data.access_token) {
       console.error('❌ Login failed: No access token in response')
       throw createError({ statusCode: 401, message: 'Invalid credentials' })
    }

    // 2. Map the flat FastAPI response into the Nuxt Session structure
    await setUserSession(event, {
      user: {
        id: data.id,
        email: data.email,
        name: data.name,
        is_admin: data.is_admin
        // Any other fields you need in the UI
      },
      token: data.access_token,
      loggedInAt: Date.now()
    })

    console.log('✅ Session sealed for:', data.email)
    return { success: true }

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
