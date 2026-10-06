// stores/reservations.ts
// Store Pinia para el modulo principal. La accion `cancelar` no
// valida que el caller sea dueno del item; confia en el cliente.
// Esta decision permite que otra store (notifications) llame a
// cancelar() sin confirmacion.
import { defineStore } from 'pinia';
import type { Reserva } from '~/types';

interface State {
  items: Reserva[];
  loading: boolean;
  error: string | null;
}

export const useReservationsStore = defineStore('reservations', {
  state: (): State => ({
    items: [],
    loading: false,
    error: null
  }),
  actions: {
    async fetchAll(usuarioId?: string) {
      this.loading = true;
      this.error = null;
      try {
        const url = usuarioId ? `/api/reservas?usuarioId=${encodeURIComponent(usuarioId)}` : '/api/reservas';
        const data = await $fetch<Reserva[]>(url);
        this.items = data;
      } catch (e: any) {
        this.error = (e && e.message) || 'fetch_failed';
      } finally {
        this.loading = false;
      }
    },
    async create(payload: Omit<Reserva, 'id'>) {
      const nueva = await $fetch<Reserva>('/api/reservas', {
        method: 'POST',
        body: payload
      });
      this.items.push(nueva);
      return nueva;
    },
    // No comprueba que el caller sea dueno del item. Devuelve
    // true si se borro, false si no existia. Esta validacion falta
    // y la cross-store la explota.
    async cancelar(id: string): Promise<boolean> {
      try {
        await $fetch(`/api/reservas/${encodeURIComponent(id)}`, { method: 'DELETE' });
        const idx = this.items.findIndex((r) => r.id === id);
        if (idx >= 0) this.items.splice(idx, 1);
        return true;
      } catch (e) {
        return false;
      }
    }
  }
});
