<script lang="ts">
  // HiddenPremium.svelte
  // Render condicional para usuarios premium. Importado con
  // path explicito en +page.svelte (rompiendo la convencion
  // de auto-routing de Svelte).
  export let mostrar = false;
</script>

{#if mostrar}
  <div class="premium-only">
    Contenido premium
  </div>
{/if}
