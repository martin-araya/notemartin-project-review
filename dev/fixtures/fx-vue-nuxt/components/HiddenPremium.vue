<script setup lang="ts">
// components/HiddenPremium.vue
// Componente que renderiza contenido solo para usuarios premium.
// Importado con ruta completa en pages/index.vue (rompiendo el
// patron de auto-imports). No se usa en el template de index.
defineProps<{ mostrar?: boolean }>();
</script>

<template>
  <div v-if="mostrar" class="premium-only">
    Contenido premium
  </div>
</template>
