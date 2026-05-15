<script setup lang="ts">
definePageMeta({
  layout: 'auth'
})

useSeoMeta({
  title: 'Unsubscribe',
  description: 'Manage your Quizify email preferences'
})

const config = useRuntimeConfig()

// Token comes from the email footer link. Marketing site is statically
// generated, so the query string isn't reliable during SSR — defer to mount.
type LoadState = 'loading' | 'ready' | 'invalid_token' | 'unsubscribed' | 'resubscribed' | 'error'

const state = ref<LoadState>('loading')
const token = ref('')
const email = ref('')
const errorDetail = ref('')
const submitting = ref(false)

async function loadInfo() {
  if (!token.value) {
    state.value = 'invalid_token'
    return
  }
  try {
    const info = await $fetch<{ email: string; is_unsubscribed: boolean }>(
      `${config.public.apiBase}/unsubscribe/info`,
      { query: { token: token.value } }
    )
    email.value = info.email
    state.value = info.is_unsubscribed ? 'unsubscribed' : 'ready'
  } catch (e: any) {
    if (e?.status === 400 || e?.statusCode === 400) {
      state.value = 'invalid_token'
    } else {
      errorDetail.value = e?.data?.detail || e?.message || 'Could not load your subscription status.'
      state.value = 'error'
    }
  }
}

async function confirmUnsubscribe() {
  if (submitting.value) return
  submitting.value = true
  try {
    await $fetch(`${config.public.apiBase}/unsubscribe`, {
      method: 'POST',
      query: { token: token.value }
    })
    state.value = 'unsubscribed'
  } catch (e: any) {
    errorDetail.value = e?.data?.detail || e?.message || 'Could not unsubscribe. Please try again.'
    state.value = 'error'
  } finally {
    submitting.value = false
  }
}

async function resubscribe() {
  if (submitting.value) return
  submitting.value = true
  try {
    await $fetch(`${config.public.apiBase}/unsubscribe/resubscribe`, {
      method: 'POST',
      query: { token: token.value }
    })
    state.value = 'resubscribed'
  } catch (e: any) {
    errorDetail.value = e?.data?.detail || e?.message || 'Could not resubscribe. Please try again.'
    state.value = 'error'
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  const params = new URLSearchParams(window.location.search)
  token.value = params.get('token') || ''
  loadInfo()
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-md">
      <div class="bg-default border border-default rounded-2xl shadow-lg p-8">

        <!-- Loading -->
        <div v-if="state === 'loading'" class="text-center py-6">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-3" />
          <p class="text-sm text-muted">Loading…</p>
        </div>

        <!-- Confirm screen -->
        <div v-else-if="state === 'ready'" class="text-center">
          <UIcon name="i-lucide-mail-x" class="w-12 h-12 text-muted mx-auto mb-3" />
          <h1 class="text-xl font-bold text-highlighted mb-2">Unsubscribe from Quizify</h1>
          <p class="text-sm text-muted mb-1">You're about to unsubscribe</p>
          <p class="text-base font-semibold text-highlighted mb-5 break-all">{{ email }}</p>
          <p class="text-xs text-muted mb-6 leading-relaxed">
            You'll stop receiving product announcements and tips. Transactional
            emails — verification and password resets — will still be delivered
            so you can keep using your account.
          </p>
          <UButton
            color="error"
            block
            size="lg"
            :loading="submitting"
            @click="confirmUnsubscribe"
          >
            Confirm unsubscribe
          </UButton>
          <NuxtLink to="/" class="block mt-3 text-xs text-muted hover:underline">
            Cancel and return to the homepage
          </NuxtLink>
        </div>

        <!-- Already unsubscribed (or just succeeded) -->
        <div v-else-if="state === 'unsubscribed'" class="text-center">
          <UIcon name="i-lucide-check-circle-2" class="w-12 h-12 text-success mx-auto mb-3" />
          <h1 class="text-xl font-bold text-highlighted mb-2">You're unsubscribed</h1>
          <p class="text-sm text-muted mb-1">No more announcements will be sent to</p>
          <p class="text-base font-semibold text-highlighted mb-6 break-all">{{ email }}</p>
          <p class="text-xs text-muted mb-6 leading-relaxed">
            Changed your mind? You can resubscribe anytime — we won't backfill
            anything you missed.
          </p>
          <UButton
            color="primary"
            variant="outline"
            block
            size="lg"
            :loading="submitting"
            @click="resubscribe"
          >
            Resubscribe
          </UButton>
        </div>

        <!-- Resubscribed -->
        <div v-else-if="state === 'resubscribed'" class="text-center">
          <UIcon name="i-lucide-mail-check" class="w-12 h-12 text-success mx-auto mb-3" />
          <h1 class="text-xl font-bold text-highlighted mb-2">Welcome back</h1>
          <p class="text-sm text-muted mb-1">Re-subscribed</p>
          <p class="text-base font-semibold text-highlighted mb-6 break-all">{{ email }}</p>
          <NuxtLink to="/">
            <UButton color="primary" block size="lg">Return to Quizify</UButton>
          </NuxtLink>
        </div>

        <!-- Invalid / expired token -->
        <div v-else-if="state === 'invalid_token'" class="text-center">
          <UIcon name="i-lucide-link-2-off" class="w-12 h-12 text-warning mx-auto mb-3" />
          <h1 class="text-xl font-bold text-highlighted mb-2">Link expired or invalid</h1>
          <p class="text-sm text-muted mb-6 leading-relaxed">
            The unsubscribe link in this email may be too old or has already
            been used. To stop receiving emails, reply to any Quizify email
            with "unsubscribe" and we'll handle it manually.
          </p>
          <NuxtLink to="/">
            <UButton color="primary" variant="outline" block size="lg">Back to Quizify</UButton>
          </NuxtLink>
        </div>

        <!-- Generic error -->
        <div v-else-if="state === 'error'" class="text-center">
          <UIcon name="i-lucide-alert-circle" class="w-12 h-12 text-error mx-auto mb-3" />
          <h1 class="text-xl font-bold text-highlighted mb-2">Something went wrong</h1>
          <p class="text-sm text-muted mb-6">{{ errorDetail }}</p>
          <UButton color="primary" variant="outline" block size="lg" @click="loadInfo">
            Try again
          </UButton>
        </div>

      </div>
    </div>
  </div>
</template>
