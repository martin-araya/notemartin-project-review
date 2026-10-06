// nuxt.config.ts
// Configuracion de Nuxt: modulos, css, runtimeConfig, payload
// extraction deshabilitado para que el state de Pinia viaje inline.
export default defineNuxtConfig({
  modules: ['@pinia/nuxt'],
  css: ['~/assets/css/main.scss'],
  imports: {
    dirs: ['stores']
  },
  experimental: {
    payloadExtraction: false
  },
  runtimeConfig: {
    public: {
      apiBase: '/api'
    }
  },
  app: {
    head: {
      title: 'fx-vue-nuxt',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  }
});
