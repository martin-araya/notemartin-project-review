// composables/useProfile.ts
// Composable que expone los datos del modulo correspondiente y un
// computed reactivo sobre el rol.
import { computed } from 'vue';
import { useProfileStore } from '~/stores/profile';

export function useProfile(usuarioId?: string) {
  const store = useProfileStore();
  if (usuarioId && !store.current) {
    // Carga lazy al primer uso; no se invoca desde setup
    // para no generar warnings en SSR si la cookie no existe.
  }
  return {
    current: computed(() => store.current),
    isPremium: computed(() => store.isPremium),
    role: computed(() => store.role),
    update: (patch: any) => store.update(patch),
    logout: () => store.logout()
  };
}
