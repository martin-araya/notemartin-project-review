// composables/useSession.ts
// Composable auxiliar para el middleware global. En este fixture
// no hay sesion real: el store se inicializa como no autenticado.
import { ref, computed } from 'vue';

const _isAuth = ref(false);

export function useSession() {
  return {
    isAuthenticated: computed(() => _isAuth.value),
    login() { _isAuth.value = true; },
    logout() { _isAuth.value = false; }
  };
}
