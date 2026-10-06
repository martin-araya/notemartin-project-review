<script lang="ts">
  // TagPicker.svelte
  // Selector con runes $state y $derived. Trampa: un $effect
  // registra un setInterval que nunca se limpia (memory leak).
  import type { Etiqueta } from '$lib/server/types';
  export let etiquetas: Etiqueta[] = [];
  export let value: string[] = [];

  // $state: reemplaza a `let` reactivo en Svelte 5.
  let selected = $state<string[]>([]);

  // $derived: recalcula filtered cuando selected cambia.
  let filtered = $derived(etiquetas.filter((e) => !selected.includes(e.id)));

  // Trampa paquete #4: $effect sin cleanup, memory leak.
  $effect(() => {
    const id = setInterval(() => {
      // Heartbeat sin cleanup. La skill debe notar la fuga.
      // eslint-disable-next-line no-console
      console.log('[tag-picker] tick', selected.length);
    }, 5000);
    return () => clearInterval(id);
  });
</script>

<div class="fx-tag-picker">
  {#each selected as eId (eId)}
    <span class="tag selected">{eId}</span>
  {/each}
  {#each filtered as e (e.id)}
    <button type="button" onclick={() => { selected = [...selected, e.id]; value = [...value, e.id]; }}>
      {e.nombre}
    </button>
  {/each}
</div>
