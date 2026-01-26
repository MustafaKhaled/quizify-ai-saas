export default eventHandler(async (event) => {
  const session = await getUserSession(event)
  const config = useRuntimeConfig()

  if (!session.token) {
    throw createError({
      statusCode: 401,
      message: 'Unauthorized'
    })
  }

  try {
    // Fetch all users from the backend
    const users = await $fetch(`${config.public.apiBase}/admin/allusers`, {
      headers: {
        Authorization: `Bearer ${session.token}`
      }
    })

    // Calculate stats
    const totalUsers = users.length
    const proUsers = users.filter((u: any) => u.is_pro || (u.subscription && (u.subscription.status === 'active_monthly' || u.subscription.status === 'active_yearly'))).length
    const trialUsers = users.filter((u: any) => u.subscription && u.subscription.status === 'trial').length
    const totalQuizzes = users.reduce((sum: number, u: any) => sum + (u.quizzes_count || 0), 0)
    const totalSources = users.reduce((sum: number, u: any) => sum + (u.sources_count || 0), 0)

    // Calculate variations (mock for now, could be based on previous period)
    const previousUsers = Math.max(1, totalUsers - 5) // Mock previous value
    const usersVariation = Math.round(((totalUsers - previousUsers) / previousUsers) * 100)

    return {
      totalUsers: {
        value: totalUsers,
        variation: usersVariation
      },
      proUsers: {
        value: proUsers,
        variation: Math.round((proUsers / Math.max(1, totalUsers)) * 100)
      },
      totalQuizzes: {
        value: totalQuizzes,
        variation: 0 // Could calculate based on previous period
      },
      totalSources: {
        value: totalSources,
        variation: 0 // Could calculate based on previous period
      }
    }
  } catch (err: any) {
    throw createError({
      statusCode: err?.response?.status || 500,
      message: err?.response?._data?.detail || 'Failed to fetch stats'
    })
  }
})
