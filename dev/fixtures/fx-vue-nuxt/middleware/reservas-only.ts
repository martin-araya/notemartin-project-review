// Middleware named (no global) que se aplica via definePageMeta.
// Bloquea el acceso a paginas que requieren rol premium.
export default defineNuxtRouteMiddleware((to, from) => {
  const profile = useProfileStore();
  if (!profile.isPremium) {
    return navigateTo('/');
  }
});
