// stores/profile.ts
// Store Pinia para el modulo de cuenta. role y premium son
// derivados en getters; premium=true activa la clase CSS que
// oculta opciones correspondientes en el frontend.
import { defineStore } from 'pinia';
import type { Profile } from '~/types';

interface State {
  current: Profile | null;
  loading: boolean;
}

export const useProfileStore = defineStore('profile', {
  state: (): State => ({
    current: null,
    loading: false
  }),
  getters: {
    isPremium: (state): boolean => !!state.current && state.current.premium === true,
    role: (state): string => (state.current && state.current.role) || 'guest'
  },
  actions: {
    async fetch(id: string) {
      this.loading = true;
      try {
        this.current = await $fetch<Profile>(`/api/profile?id=${encodeURIComponent(id)}`);
      } finally {
        this.loading = false;
      }
    },
    async update(patch: Partial<Profile>) {
      if (!this.current) return null;
      const updated = await $fetch<Profile>('/api/profile', {
        method: 'PATCH',
        body: { id: this.current.id, ...patch }
      });
      this.current = updated;
      return updated;
    },
    logout() {
      this.current = null;
    }
  }
});
