// Tests del modulo de cuenta: store + composable.
import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useProfileStore } from '../stores/profile';

describe('FEAT-002 cuenta', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('R-01 el store arranca con current null', () => {
    const store = useProfileStore();
    expect(store.current).toBe(null);
    expect(store.isPremium).toBe(false);
    expect(store.role).toBe('guest');
  });

  it('R-02 el store expone las acciones fetch, update, logout', () => {
    const store = useProfileStore();
    expect(typeof store.fetch).toBe('function');
    expect(typeof store.update).toBe('function');
    expect(typeof store.logout).toBe('function');
  });

  it('R-03 logout limpia current', () => {
    const store = useProfileStore();
    store.current = { id: 'u-1', nombre: 'A', email: 'a@b.c', role: 'user', premium: false };
    expect(store.current).not.toBe(null);
    store.logout();
    expect(store.current).toBe(null);
  });

  it('R-04 el composable useProfile expone current, isPremium, role, update, logout', async () => {
    const { useProfile } = await import('../composables/useProfile');
    const c = useProfile('u-1');
    expect(c.current.value).toBe(null);
    expect(c.isPremium.value).toBe(false);
    expect(c.role.value).toBe('guest');
    expect(typeof c.update).toBe('function');
    expect(typeof c.logout).toBe('function');
  });
});
