export default defineNuxtPlugin(() => {
  // Only run on client side
  if (typeof window === 'undefined') return

  // Check if there's a token in the URL
  const urlParams = new URLSearchParams(window.location.search)
  const token = urlParams.get('token')

  if (token) {
    // Save token to dashboard's localStorage
    localStorage.setItem('auth_token', token)

    // Remove token from URL for security
    const url = new URL(window.location.href)
    url.searchParams.delete('token')
    window.history.replaceState({}, '', url.pathname + url.hash)

    console.log('✅ Token received and saved to dashboard localStorage')
  }
})
