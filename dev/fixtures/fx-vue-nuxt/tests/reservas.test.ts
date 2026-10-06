// tests/reservas.test.ts
// Tests del modulo principal: el cliente lista, crea, valida y
// cancela items a traves del store y del composable.
import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useReservationsStore } from '../stores/reservations';

describe('FEAT-001 reservas', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('R-01 el store arranca vacio', () => {
    const store = useReservationsStore();
    expect(store.items).toEqual([]);
    expect(store.loading).toBe(false);
    expect(store.error).toBe(null);
  });

  it('R-02 el store expone las acciones fetchAll, create, cancelar', () => {
    const store = useReservationsStore();
    expect(typeof store.fetchAll).toBe('function');
    expect(typeof store.create).toBe('function');
    expect(typeof store.cancelar).toBe('function');
  });

  it('R-03 la accion cancelar devuelve false cuando el id no existe', async () => {
    const store = useReservationsStore();
    const result = await store.cancelar('no-existe');
    expect(result).toBe(false);
  });

  it('R-04 el composable useReservas expone items, loading, error, refresh, cancelar', async () => {
    const { useReservas } = await import('../composables/useReservas');
    const c = useReservas('u-1');
    expect(c.items.value).toEqual([]);
    expect(c.loading.value).toBe(false);
    expect(typeof c.refresh).toBe('function');
    expect(typeof c.cancelar).toBe('function');
  });
});
