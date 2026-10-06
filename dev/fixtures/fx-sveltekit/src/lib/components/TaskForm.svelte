<script lang="ts">
  // TaskForm.svelte
  // Formulario de creacion. Usa use:enhance para interceptar el
  // submit y hacer la peticion fetch en lugar de recargar la pagina.
  import { enhance } from '$app/forms';
  let titulo = '';
</script>

<form method="POST" action="?/create" use:enhance class="fx-form">
  <label>Titulo <input name="titulo" bind:value={titulo} required /></label>
  <button type="submit">Crear</button>
</form>
