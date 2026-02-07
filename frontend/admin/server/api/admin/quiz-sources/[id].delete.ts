export default eventHandler(async (event) => {
  const session = await getUserSession(event)

  if (!session || !session.token) {
    throw createError({
      statusCode: 401,
      statusMessage: 'Unauthorized: No session token found'
    })
  }

  const id = getRouterParam(event, 'id')
  const backendUrl = process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

  try {
    const response = await $fetch(`${backendUrl}/quizzes/sources/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${session.token}`,
        'Content-Type': 'application/json'
      }
    })

    return response
  } catch (error: any) {
    console.error('Error deleting quiz source:', error.data || error.message)
    throw createError({
      statusCode: error.response?.status || 500,
      statusMessage: error.data?.detail || 'Failed to delete quiz source'
    })
  }
})
