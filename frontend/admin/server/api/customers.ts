import type { User } from '~/types'

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
    // Fetch all users from the backend admin API
    const users = await $fetch(`${config.public.apiBase}/admin/allusers`, {
      headers: {
        Authorization: `Bearer ${session.token}`
      }
    })

    // Transform backend users to match frontend User type
    const customers: User[] = users.map((user: any, index: number) => {
      // Determine status based on subscription info
      let status: 'subscribed' | 'unsubscribed' | 'bounced' = 'unsubscribed'
      if (user.subscription) {
        if (user.subscription.status === 'active_monthly' || user.subscription.status === 'active_yearly') {
          status = 'subscribed'
        } else if (user.subscription.status === 'expired') {
          status = 'bounced'
        }
      }

      return {
        id: user.id,
        name: user.name || user.email.split('@')[0],
        email: user.email,
        avatar: {
          src: `https://i.pravatar.cc/128?u=${user.id}`
        },
        status,
        location: user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'
      }
    })

    return customers
  } catch (err: any) {
    throw createError({
      statusCode: err?.response?.status || 500,
      message: err?.response?._data?.detail || 'Failed to fetch users'
    })
  }
})
