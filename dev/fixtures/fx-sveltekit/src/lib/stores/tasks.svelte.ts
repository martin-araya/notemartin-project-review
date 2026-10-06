// src/lib/stores/tasks.svelte.ts
// Store Svelte 5 (rune $state) para el modulo principal. La accion
// `completar` no valida que el caller sea dueno del item; confia
// en el cliente.
import type { Tarea } from '$lib/server/types';

interface State {
  items: Tarea[];
  loading: boolean;
}

export function createTasksStore() {
  let items = $state<Tarea[]>([]);
  let loading = $state(false);

  return {
    get items() { return items; },
    get loading() { return loading; },
    set(next: Tarea[]) { items = next; },
    add(t: Tarea) { items = [...items, t]; },
    // No comprueba que el caller sea dueno del item. Esta
    // validacion falta y el cross-store la explota.
    remove(id: string): boolean {
      const idx = items.findIndex((x) => x.id === id);
      if (idx === -1) return false;
      items = items.filter((x) => x.id !== id);
      return true;
    },
    async fetchAll(usuarioId?: string) {
      loading = true;
      try {
        const url = usuarioId
          ? '/_fx_data/tareas?usuarioId=' + encodeURIComponent(usuarioId)
          : '/_fx_data/tareas';
        const data = await fetch(url).then((r) => r.json());
        items = data as Tarea[];
      } finally {
        loading = false;
      }
    }
  };
}

export type TasksStore = ReturnType<typeof createTasksStore>;
