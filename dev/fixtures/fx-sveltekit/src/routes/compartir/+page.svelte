<script lang="ts">
  import type { PageData } from './$types';
  import ShareButton from '$lib/components/ShareButton.svelte';
  export let data: PageData;
</script>

<svelte:head>
  <title>Compartir - fx-sveltekit</title>
</svelte:head>

<h1>Compartir</h1>

{#if data.tareas.length === 0}
  <p>Sin items para compartir.</p>
{:else}
  <ul class="fx-list">
    {#each data.tareas as t (t.id)}
      <li>
        {t.titulo}
        <ShareButton tareaId={t.id} />
      </li>
    {/each}
  </ul>
{/if}
