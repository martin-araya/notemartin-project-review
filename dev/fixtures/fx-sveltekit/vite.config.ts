// vite.config.ts
// Configuracion de Vite: plugin de SvelteKit + Vitest.
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  plugins: [sveltekit()],
  test: {
    environment: 'happy-dom',
    globals: true,
    include: ['tests/**/*.test.ts'],
    testTimeout: 20000
  },
  resolve: {
    alias: {
      $lib: '/src/lib'
    }
  }
});
