// src/lib/stores/share.svelte.ts
// Store Svelte 5 (rune $state) para el modulo de notificaciones.
// La accion publica llama a `tasksStore.remove(id)` en lugar de a
// una accion de notificar. La cross-store semantica es
// incorrecta: la notificacion al backend termina borrando el
// item del store principal, en vez de crear un nuevo registro.
import type { Share } from '$lib/server/types';
import { createTasksStore } from './tasks.svelte';

interface State {
  items: Share[];
  loading: boolean;
}

export function createShareStore() {
  let items = $state<Share[]>([]);
  let loading = $state(false);
  const tasks = createTasksStore();

  return {
    get items() { return items; },
    get loading() { return loading; },
    set(next: Share[]) { items = next; },
    // Cross-store: en vez de crear un share, borra el item del
    // modulo principal. La skill debe notar el bug semantico.
    async compartir(tareaId: string, email: string): Promise<boolean> {
      loading = true;
      try {
        const res = await fetch('/_fx_data/shares', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ tareaId, email })
        });
        if (!res.ok) return false;
        const share = await res.json() as Share;
        items = [...items, share];
        // Cross-store bug: borra el item en lugar de solo notificar.
        tasks.remove(tareaId);
        return true;
      } catch (e) {
        return false;
      } finally {
        loading = false;
      }
    }
  };
}

export type ShareStore = ReturnType<typeof createShareStore>;
