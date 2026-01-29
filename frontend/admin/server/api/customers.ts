interface SubscriptionInfo {
  status: string
  label: string
  is_eligible: boolean
  ends_at: string | null
  trial_ends_at: string | null
  status_label: string | null
}

interface AdminUser {
  id: string
  email: string
  name: string | null
  created_at: string
  is_admin: boolean
  is_pro: boolean
  quizzes_count: number
  sources_count: number
  subscription: SubscriptionInfo | null
}

// frontend/admin/server/api/customers.ts

export default eventHandler(async (event) => {
  // 1. Get the session data we sealed during login
  const session = await getUserSession(event)
  
  // 2. Check if the token exists
  if (!session || !session.token) {
    throw createError({
      statusCode: 401,
      statusMessage: 'Unauthorized: No session token found'
    })
  }

  const backendUrl = process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
  
  try {
    // 3. Use the token from the session to authorize the FastAPI request
    const response = await $fetch(`${backendUrl}/admin/allusers`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${session.token}`,
        'Content-Type': 'application/json'
      }
    })
    
    return response
  } catch (error: any) {
    console.error('Error fetching users from FastAPI:', error.data || error.message)
    throw createError({
      statusCode: error.response?.status || 500,
      statusMessage: 'Failed to fetch users from backend'
    })
  }
})
