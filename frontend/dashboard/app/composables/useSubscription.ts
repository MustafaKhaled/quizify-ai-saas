const user = ref<any>(null)
const loaded = ref(false)

export function useSubscription() {
  const config = useRuntimeConfig()

  const isEligible = computed(() => {
    if (!user.value) return false
    return user.value.subscription?.is_eligible === true
  })

  const subscriptionLabel = computed(() => {
    return user.value?.subscription?.label || ''
  })

  const isPro = computed(() => user.value?.is_pro === true)

  const fetchUser = async () => {
    if (loaded.value) return
    try {
      const res = await fetch(`${config.public.apiBase}/users/me`, { credentials: 'include' })
      if (res.ok) user.value = await res.json()
    } catch {}
    loaded.value = true
  }

  const refreshUser = async () => {
    loaded.value = false
    await fetchUser()
  }

  const startCheckout = async (priceId: string) => {
    try {
      if (!priceId || typeof priceId !== 'string' || !priceId.trim()) {
        throw new Error('Missing price ID — cannot start checkout')
      }
      const body = { price_id: priceId.trim() }
      const res = await fetch(`${config.public.apiBase}/subscription/create-checkout-session`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      if (!res.ok) {
        let detail = ''
        try { detail = (await res.json())?.detail || '' } catch {}
        throw new Error(detail || `Failed to create checkout (${res.status})`)
      }
      const { url } = await res.json()
      if (!url) throw new Error('Checkout URL missing in response')
      window.location.href = url
    } catch (e: any) {
      console.error('startCheckout failed:', e)
      alert(e?.message || 'Failed to start checkout')
    }
  }

  return { user, isEligible, isPro, subscriptionLabel, fetchUser, refreshUser, startCheckout }
}
