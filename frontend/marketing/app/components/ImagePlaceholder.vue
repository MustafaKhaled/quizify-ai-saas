<script setup lang="ts">
defineProps<{
  // Optional path to a real screenshot. When set, the image renders on top of
  // the dashed placeholder so a missing file degrades gracefully to the pattern.
  src?: string
  // Optional caption shown inside the placeholder when no image is set.
  caption?: string
  alt?: string
}>()
</script>

<template>
  <UPageCard variant="subtle">
    <div class="relative overflow-hidden rounded-sm border border-dashed border-accented opacity-75 px-4 flex items-center justify-center aspect-video">
      <svg
        class="absolute inset-0 h-full w-full stroke-inverted/10"
        fill="none"
      >
        <defs>
          <pattern
            id="pattern-5c1e4f0e-62d5-498b-8ff0-cf77bb448c8e"
            x="0"
            y="0"
            width="10"
            height="10"
            patternUnits="userSpaceOnUse"
          >
            <path d="M-3 13 15-5M-5 5l18-18M-1 21 17 3" />
          </pattern>
        </defs>
        <rect
          stroke="none"
          fill="url(#pattern-5c1e4f0e-62d5-498b-8ff0-cf77bb448c8e)"
          width="100%"
          height="100%"
        />
      </svg>

      <NuxtImg
        v-if="src"
        :src="src"
        :alt="alt || caption || 'Product screenshot'"
        class="relative z-10 max-h-full max-w-full object-contain rounded-sm"
        loading="lazy"
      />
      <span
        v-else-if="caption"
        class="relative z-10 text-xs text-muted text-center px-2"
      >{{ caption }}</span>

      <slot />
    </div>
  </UPageCard>
</template>
