interface QuizAttempt {
  id: string
  score_percentage: number
  is_passed: boolean
  time_taken_seconds: number | null
  time_remaining_seconds: number | null
  started_at: string | null
  ended_at: string | null
  attempt_date: string | null
  user_answers: any
}

interface QuizResultsResponse {
  quiz_id: string
  quiz_title: string
  num_questions: number
  attempts: QuizAttempt[]
}

export default eventHandler(async (event) => {
  const session = await getUserSession(event)

  if (!session || !session.token) {
    throw createError({
      statusCode: 401,
      statusMessage: 'Unauthorized: No session token found'
    })
  }

  const quizId = getRouterParam(event, 'id')
  const backendUrl = process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

  try {
    const response = await $fetch<QuizResultsResponse>(
      `${backendUrl}/admin/quizzes/${quizId}/results`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${session.token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    return response
  } catch (error: any) {
    console.error('Error fetching quiz results:', error.data || error.message)
    throw createError({
      statusCode: error.response?.status || 500,
      statusMessage: error.data?.detail || 'Failed to fetch quiz results'
    })
  }
})
