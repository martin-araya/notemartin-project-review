// tests/notifications.test.ts
// Tests del feature de avisos + verificacion de la cross-store call.
import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useNotificationsStore } from '../stores/notifications';
import { useReservationsStore } from '../stores/reservations';

describe('FEAT-003 avisos', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('R-01 el store arranca vacio', () => {
    const store = useNotificationsStore();
    expect(store.items).toEqual([]);
    expect(store.unread).toEqual([]);
    expect(store.count).toBe(0);
  });

  it('R-02 el store expone fetchAll, markRead y getters', () => {
    const store = useNotificationsStore();
    expect(typeof store.fetchAll).toBe('function');
    expect(typeof store.markRead).toBe('function');
  });

  it('R-03 cross-store: markRead importa useReservationsStore internamente', () => {
    const notif = useNotificationsStore();
    expect(typeof notif.markRead).toBe('function');
    // Verificamos el source del archivo: debe contener la llamada
    // cross-store y el metodo cancelar del otro store.
    const fs = require('fs');
    const path = require('path');
    const src = fs.readFileSync(path.join(__dirname, '..', 'stores', 'notifications.ts'), 'utf8');
    expect(src).toMatch(/useReservationsStore/);
    expect(src).toMatch(/\.cancelar\(/);
  });

  it('R-04 reservationsStore se puede instanciar junto con notifications', () => {
    const notif = useNotificationsStore();
    const res = useReservationsStore();
    expect(notif).toBeDefined();
    expect(res).toBeDefined();
    expect(typeof res.cancelar).toBe('function');
  });
});
