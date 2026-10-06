<script setup lang="ts">
// components/ReservaCard.vue
// Tarjeta de una reserva. Usa defineProps con TypeScript y defineEmits
// para emitir 'cancelar' al padre. El CSS premium-hide se aplica
// cuando la reserva es premium y el usuario no lo es.
const props = defineProps<{ reserva: any }>();
const emit = defineEmits<{ (e: 'cancelar'): void }>();
</script>

<template>
  <li :class="{ 'premium-hide': reserva.premium && reserva.usuarioId !== 'u-1' }">
    <strong>{{ reserva.id }}</strong>
    - {{ reserva.fecha }}
    - {{ reserva.personas }} personas
    - sala {{ reserva.sala }}
    <button @click="emit('cancelar')">Cancelar</button>
  </li>
</template>
