<script lang="ts">
  // Listado con TaskCard y TaskForm. El form action '?/create' y
  // '?/delete' viven en +page.server.ts.
  import type { PageData } from './$types';
  import TaskCard from '$lib/components/TaskCard.svelte';
  import TaskForm from '$lib/components/TaskForm.svelte';
  export let data: PageData;
</script>

<svelte:head>
  <title>Tareas - fx-sveltekit</title>
</svelte:head>

<h1>Tareas</h1>
{#if data.tareas.length === 0}
  <p>Sin items. Crea uno con el formulario de abajo.</p>
{:else}
  <ul class="fx-list">
    {#each data.tareas as t (t.id)}
      <TaskCard tarea={t} />
    {/each}
  </ul>
{/if}

<h2>Nueva</h2>
<TaskForm />
