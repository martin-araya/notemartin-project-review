<script setup lang="ts">
// components/NotificacionItem.vue
// Item de la lista del modulo de avisos. Emite 'mark-read' al
// hacer click. La clase archived se aplica a elementos ya leidos.
const props = defineProps<{ notificacion: any }>();
const emit = defineEmits<{ (e: 'mark-read'): void }>();
</script>

<template>
  <li :class="{ archived: notificacion.leida }">
    <span>{{ notificacion.mensaje }}</span>
    <small>{{ notificacion.fecha }}</small>
    <button v-if="!notificacion.leida" @click="emit('mark-read')">Marcar leida</button>
  </li>
</template>
