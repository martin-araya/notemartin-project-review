// src/lib/stores/tags.svelte.ts
// Store Svelte 5 (rune $state) para el catalogo de clasificacion.
// Solo lectura en cliente; las asignaciones a items se hacen via
// cross-store desde el modulo de notificaciones.
import type { Etiqueta } from '$lib/server/types';

interface State {
  items: Etiqueta[];
}

export function createTagsStore() {
  let items = $state<Etiqueta[]>([]);
  return {
    get items() { return items; },
    set(next: Etiqueta[]) { items = next; },
    findByName(name: string): Etiqueta | undefined {
      return items.find((e) => e.nombre === name);
    }
  };
}

export type TagsStore = ReturnType<typeof createTagsStore>;
