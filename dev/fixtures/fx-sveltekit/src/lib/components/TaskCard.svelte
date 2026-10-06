<script lang="ts">
  // TaskCard.svelte
  // Tarjeta de un item. defineProps + clase premium-hide. Emite
  // 'delete' al padre; el padre lo engancha al form action.
  import type { Tarea } from '$lib/server/types';
  export let tarea: Tarea;
</script>

<li class:premium-hide={tarea.premium && tarea.usuarioId !== 'u-1'}>
  <strong>{tarea.id}</strong>
  - {tarea.titulo}
  - {tarea.completada ? 'OK' : 'pendiente'}
  <form method="POST" action="?/delete" style="display:inline">
    <input type="hidden" name="id" value={tarea.id} />
    <button type="submit">Borrar</button>
  </form>
</li>
