// plugins/0.api-base.ts
// Plugin Nuxt que provee un cliente API minimo via $api. Las paginas
// lo usan indirectamente a traves de composables que invocan
// $fetch. Este plugin centraliza headers y baseUrl.
export default defineNuxtPlugin((nuxtApp) => {
  const api = {
    async get(path: string, query?: Record<string, string>) {
      const qs = query ? '?' + new URLSearchParams(query).toString() : '';
      return await $fetch('/api' + path + qs);
    },
    async post(path: string, body: any) {
      return await $fetch('/api' + path, { method: 'POST', body });
    },
    async patch(path: string, body: any) {
      return await $fetch('/api' + path, { method: 'PATCH', body });
    },
    async delete(path: string) {
      return await $fetch('/api' + path, { method: 'DELETE' });
    }
  };
  return {
    provide: { api }
  };
});
