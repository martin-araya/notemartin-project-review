// vitest.config.ts
// Configuracion de Vitest para el fixture. Usa jsdom para poder
// cargar componentes Vue; incluye los alias de Nuxt para que
// funcionen las rutas ~/, @/ y #imports.
import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '~': fileURLToPath(new URL('./', import.meta.url)),
      '@': fileURLToPath(new URL('./', import.meta.url)),
      '#imports': fileURLToPath(new URL('./.nuxt/imports.d.ts', import.meta.url))
    }
  },
  test: {
    environment: 'happy-dom',
    globals: true,
    include: ['tests/**/*.test.ts', 'tests/**/*.test.js'],
    testTimeout: 20000
  }
});
