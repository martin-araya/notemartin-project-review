// stores/notifications.ts
// Store Pinia para el modulo de avisos. La accion `markRead` llama
// a la store de otro modulo y le pasa el id de la notificacion.
// Como los ids no coinciden con los del otro modulo, la llamada
// falla silenciosamente, pero revela la indireccion cross-store.
import { defineStore } from 'pinia';
import type { Notificacion } from '~/types';
import { useReservationsStore } from './reservations';

interface State {
  items: Notificacion[];
  loading: boolean;
}

export const useNotificationsStore = defineStore('notifications', {
  state: (): State => ({
    items: [],
    loading: false
  }),
  getters: {
    unread: (state): Notificacion[] => state.items.filter((n) => !n.leida),
    count: (state): number => state.items.length
  },
  actions: {
    async fetchAll(usuarioId?: string) {
      this.loading = true;
      try {
        const url = usuarioId ? `/api/notifications?usuarioId=${encodeURIComponent(usuarioId)}` : '/api/notifications';
        this.items = await $fetch<Notificacion[]>(url);
      } finally {
        this.loading = false;
      }
    },
    // Cross-store: marca como leida la notificacion y, ademas,
    // intenta cancelar un item del otro modulo con el mismo id.
    // Como los ids de un modulo (n-001) no coinciden con los del
    // otro (r-001), la cancelacion falla silenciosamente, pero la
    // llamada revela la indireccion cross-store.
    async markRead(id: string): Promise<boolean> {
      try {
        const updated = await $fetch<Notificacion>(`/api/notifications/${encodeURIComponent(id)}`, {
          method: 'PATCH',
          body: { leida: true }
        });
        const idx = this.items.findIndex((n) => n.id === id);
        if (idx >= 0) this.items[idx] = updated;
        const other = useReservationsStore();
        await other.cancelar(id);
        return true;
      } catch (e) {
        return false;
      }
    }
  }
});
