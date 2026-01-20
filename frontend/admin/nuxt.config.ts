export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@vueuse/nuxt',
    'nuxt-auth-utils'
  ],

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  routeRules: {
    '/api/**': {
      cors: true
    }
  },

  compatibilityDate: '2024-07-11',

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
      apiBase: process.env.NUXT_PUBLIC_API_BASE_URL
    },
    session: {
      name: 'nuxt-session',
      password: process.env.NUXT_SESSION_PASSWORD,
      cookie: {
        sameSite: 'lax', 
        secure: true, // Railway is HTTPS, so this should be true
        httpOnly: true,
        path: '/', // Ensure it's available for all routes
      }
    }
  },
  future: { compatibilityVersion: 4 }
})