<script setup lang="ts">
// Listado y formulario. No hay lineas de import: los composables,
// stores y componentes entran via auto-imports de Nuxt.
// definePageMeta declara el middleware named que vive en
// middleware/.
definePageMeta({
  middleware: ['reservas-only']
});

const { items, loading, error, refresh, cancelar } = useReservas('u-1');

const nuevaFecha = ref('');
const nuevaPersonas = ref(2);
const nuevaSala = ref('A');

async function onSubmit(payload: any) {
  const store = useReservationsStore();
  await store.create({
    usuarioId: 'u-1',
    fecha: payload.fecha,
    personas: payload.personas,
    sala: payload.sala
  });
  await refresh();
}

onMounted(() => { refresh(); });
</script>

<template>
  <div>
    <h1>Reservas</h1>
    <p v-if="loading">Cargando...</p>
    <p v-else-if="error" class="error">Error: {{ error }}</p>
    <ul v-else class="fx-list">
      <ReservaCard
        v-for="r in items"
        :key="r.id"
        :reserva="r"
        @cancelar="cancelar(r.id)"
      />
    </ul>
    <h2>Nueva</h2>
    <ReservaForm
      v-model:fecha="nuevaFecha"
      v-model:personas="nuevaPersonas"
      v-model:sala="nuevaSala"
      @submit="onSubmit"
      @cancelar="refresh"
    />
  </div>
</template>
