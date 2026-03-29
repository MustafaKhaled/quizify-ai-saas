export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase || 'http://localhost:8000'
  const marketingUrl = config.public.marketingUrl || 'http://localhost:3000'

  const $apiFetch = $fetch.create({
    credentials: 'include',
    onResponseError: async ({ request, response, options }) => {
      if (response.status !== 401) return

      // Try to refresh the access token
      try {
        await $fetch(`${apiBase}/auth/refresh`, {
          method: 'POST',
          credentials: 'include'
        })
        // Retry the original request once after refresh
        await $fetch(request, options)
      } catch {
        // Refresh failed — send to login
        window.location.href = `${marketingUrl}/login`
      }
    }
  })

  return {
    provide: {
      apiFetch: $apiFetch
    }
  }
})
