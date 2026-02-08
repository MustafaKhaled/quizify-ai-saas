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
  auth: {
    session: {
      name: 'nuxt-session',
      password: process.env.NUXT_SESSION_PASSWORD,
      cookie: {
        sameSite: 'lax',
        secure: true,
        httpOnly: true,
        path: '/'
      }
    },
  cookie: {
  sameSite: 'lax',
  secure: true, 
  httpOnly: true,
  path: '/',
  // This allows the cookie to work even if Railway's proxy 
  // doesn't pass the 'secure' flag perfectly to the container
  partitioned: true 
}
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE_URL
    },
  },
  future: { compatibilityVersion: 4 }
})