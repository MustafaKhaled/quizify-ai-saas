interface SubscriptionInfo {
  status: string
  label: string
  is_eligible: boolean
  ends_at: string | null
  trial_ends_at: string | null
  status_label: string | null
}

interface QuizSourceInfo {
  id: string
  file_name: string
  upload_date: string
  start_page: number | null
  end_page: number | null
}

interface QuizInfo {
  id: string
  source_id: string
  title: string
  quiz_type: string
  num_questions: number
  time_limit: number | null
  content: any
  generation_date: string
}

interface UserDetail {
  id: string
  email: string
  name: string | null
  created_at: string
  is_admin: boolean
  is_pro: boolean
  quizzes_count: number
  sources_count: number
  subscription: SubscriptionInfo | null
  quiz_sources: QuizSourceInfo[]
  quizzes: QuizInfo[]
}

export default eventHandler(async (event) => {
  const session = await getUserSession(event)

  if (!session || !session.token) {
    throw createError({
      statusCode: 401,
      statusMessage: 'Unauthorized: No session token found'
    })
  }

  const userId = getRouterParam(event, 'id')

  const backendUrl = process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

  try {
    const response = await $fetch<UserDetail>(`${backendUrl}/admin/user/${userId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${session.token}`,
        'Content-Type': 'application/json'
      }
    })

    return response
  } catch (error: any) {
    console.error('Error fetching user details:', error.data || error.message)
    throw createError({
      statusCode: error.response?.status || 500,
      statusMessage: error.data?.detail || 'Failed to fetch user details'
    })
  }
})
