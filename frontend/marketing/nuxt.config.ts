// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/ui',
    '@nuxt/content',
    '@vueuse/nuxt',
    'nuxt-og-image'
  ],

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  routeRules: {
    '/docs': { redirect: '/docs/getting-started', prerender: false }
  },

  compatibilityDate: '2024-07-11',

  nitro: {
    prerender: {
      routes: [
        '/'
      ],
      crawlLinks: true
    }
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE_URL,
      dashboardUrl: process.env.NUXT_PUBLIC_DASHBOARD_URL || 'http://localhost:3001'
    }
  },

  // Google Analytics 4 (gtag.js). Loaded async on every page.
  // The dataLayer initializer is inlined to match Google's recommended snippet
  // exactly — running it in the head ensures gtag() is available before any
  // page-level code tries to fire events.
  app: {
    head: {
      script: [
        {
          async: true,
          src: 'https://www.googletagmanager.com/gtag/js?id=G-MEYRZZ5FXG'
        },
        {
          innerHTML: "window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-MEYRZZ5FXG');"
        }
      ]
    }
  }
})
