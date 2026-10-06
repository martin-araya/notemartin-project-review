// composables/useReservas.ts
// Composable que envuelve la store correspondiente. Hace $fetch
// directo sin reintento: si el servidor cuelga, el cliente espera
// indefinidamente. La pagina que lo usa se auto-registra sin
// import explicito.
import { computed } from 'vue';
import { useReservationsStore } from '~/stores/reservations';

export function useReservas(usuarioId?: string) {
  const store = useReservationsStore();
  return {
    items: computed(() => store.items),
    loading: computed(() => store.loading),
    error: computed(() => store.error),
    refresh: () => store.fetchAll(usuarioId),
    cancelar: (id: string) => store.cancelar(id)
  };
}
