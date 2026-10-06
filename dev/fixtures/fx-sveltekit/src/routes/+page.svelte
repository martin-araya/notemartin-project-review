<script lang="ts">
  // src/routes/+page.svelte
  // Landing con links a las paginas principales. HiddenPremium
  // se importa con path explicito para mostrar el patron (no se
  // renderiza en el template; queda como dead-import).
  import HiddenPremium from '$lib/components/HiddenPremium.svelte';
</script>

<svelte:head>
  <title>Inicio - fx-sveltekit</title>
</svelte:head>

<h1>Bienvenido a fx-sveltekit</h1>
<p>Esta aplicacion demuestra file-based routing, form actions,
   hooks.server.ts, runes ($state/$derived/$effect) y stores
   cross-call en Svelte 5.</p>
