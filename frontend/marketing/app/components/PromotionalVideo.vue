<script setup lang="ts">
// Demo video lives in /public/videos/. Until you record a real demo, the
// component falls back to the dashboard placeholder image so the hero never
// renders broken. See public/videos/DEMO_TODO.md for the swap workflow.
const POSTER = '/screenshots/dashboard.svg'
const VIDEO_MP4 = '/videos/quizify-demo.mp4'
const VIDEO_WEBM = '/videos/quizify-demo.webm'
</script>

<template>
  <div class="relative">
    <UPageCard
      variant="subtle"
      class="rounded-2xl"
    >
      <video
        class="rounded-xl w-full"
        preload="none"
        :poster="POSTER"
        controls
        playsinline
      >
        <source
          :src="VIDEO_WEBM"
          type="video/webm"
        >
        <source
          :src="VIDEO_MP4"
          type="video/mp4"
        >
      </video>
    </UPageCard>
  </div>
</template>
