/**
 * Loads the predefined-subjects registry from the backend and caches it
 * for the session. Used by the dashboard / subjects index to render the
 * predefined cards, and by subject detail pages to detect whether a subject
 * is a predefined one (and which slug it maps to).
 */

export type PredefinedAgent = {
  slug: string
  name: string
  color: string | null
  icon: string | null
}

const _cache = ref<PredefinedAgent[] | null>(null)
const _inflight = ref<Promise<PredefinedAgent[]> | null>(null)

export function usePredefinedSubjects() {
  const config = useRuntimeConfig()

  async function load(): Promise<PredefinedAgent[]> {
    if (_cache.value) return _cache.value
    if (_inflight.value) return _inflight.value
    _inflight.value = $fetch<PredefinedAgent[]>(`${config.public.apiBase}/predefined/registry`, {
      credentials: 'include',
    }).then((data) => {
      _cache.value = data
      return data
    }).finally(() => {
      _inflight.value = null
    })
    return _inflight.value
  }

  /** Look up an agent by its display name (matches Subject.name on provisioned rows). */
  function findByName(name: string | null | undefined): PredefinedAgent | undefined {
    if (!name || !_cache.value) return undefined
    return _cache.value.find((a) => a.name === name)
  }

  return {
    agents: _cache,
    load,
    findByName,
  }
}
