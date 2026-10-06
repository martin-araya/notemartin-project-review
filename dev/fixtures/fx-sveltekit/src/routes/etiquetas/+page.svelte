<script lang="ts">
  import type { PageData } from './$types';
  import TagPicker from '$lib/components/TagPicker.svelte';
  export let data: PageData;

  let filtro = '';
  let tareasFiltradas = $derived(
    filtro
      ? data.tareas.filter((t) => t.titulo.toLowerCase().includes(filtro.toLowerCase()))
      : data.tareas
  );
</script>

<svelte:head>
  <title>Etiquetas - fx-sveltekit</title>
</svelte:head>

<h1>Etiquetas</h1>

<label>Buscar
  <input type="text" bind:value={filtro} />
</label>

<TagPicker etiquetas={data.etiquetas} value={[]} />

<ul class="fx-list">
  {#each tareasFiltradas as t (t.id)}
    <li>{t.titulo}</li>
  {/each}
</ul>
