// middleware/auth.global.ts
// Middleware global de Nuxt. Redirige a /login siempre que no haya
// sesion, sin comprobar la ruta destino. Esto provoca un bucle de
// redireccion cuando el usuario navega a /login sin sesion.
export default defineNuxtRouteMiddleware((to, from) => {
  const session = useSession();
  if (!session.isAuthenticated) {
    // Bug: incluso si el destino es /login, redirige a /login
    // y vuelve a ejecutar el middleware.
    return navigateTo('/login');
  }
});
