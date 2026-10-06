<script setup lang="ts">
// Detalle de un item por route param dinamico. Usa $fetch
// directamente sin composable, lo que evita la cache de la store.
const route = useRoute();
const id = computed(() => String(route.params.id));

const { data: reserva, error } = await useAsyncData(
  () => 'item-' + id.value,
  () => $fetch('/api/reservas/' + id.value).catch(() => null)
);
</script>

<template>
  <div>
    <h1>Item {{ id }}</h1>
    <p v-if="error" class="error">{{ error.message }}</p>
    <div v-else-if="reserva">
      <p>Fecha: {{ reserva.fecha }}</p>
      <p>Personas: {{ reserva.personas }}</p>
      <p>Sala: {{ reserva.sala }}</p>
      <p v-if="reserva.premium" class="info">Premium</p>
    </div>
    <p v-else>No encontrado</p>
  </div>
</template>
