<script lang="ts">
  // Detalle de un item por route param dinamico.
  import type { PageData } from './$types';
  export let data: PageData;
</script>

<svelte:head>
  <title>Item {data.tarea.id}</title>
</svelte:head>

<h1>Item {data.tarea.id}</h1>
<p>Titulo: {data.tarea.titulo}</p>
<p>Completada: {data.tarea.completada ? 'si' : 'no'}</p>
{#if data.tarea.premium}
  <p class="info">Premium</p>
{/if}
