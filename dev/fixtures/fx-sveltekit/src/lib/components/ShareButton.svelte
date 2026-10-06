<script lang="ts">
  // ShareButton.svelte
  // Boton que emite el form al padre. El padre lo engancha al
  // form action que llama al store del modulo de notificaciones
  // (cross-store).
  export let tareaId: string;
  export let email = '';
</script>

<form method="POST" action="?/compartir" class="fx-form">
  <input type="hidden" name="tareaId" value={tareaId} />
  <label>Email <input name="email" type="email" bind:value={email} required /></label>
  <button type="submit">Compartir</button>
</form>
