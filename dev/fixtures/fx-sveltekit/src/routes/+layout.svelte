<script lang="ts">
  // src/routes/+layout.svelte
  // Layout raiz con navegacion. Renderiza el slot.
  import '../styles/main.scss';
</script>

<div>
  <header class="fx-top">
    <a href="/">Inicio</a>
    <a href="/tareas">Tareas</a>
    <a href="/etiquetas">Etiquetas</a>
    <a href="/compartir">Compartir</a>
  </header>
  <main>
    <slot />
  </main>
</div>
