<script setup lang="ts">
// pages/index.vue
// Landing con links a las paginas principales. El componente
// HiddenPremium se importa con la ruta completa para mostrar el
// patron (no se renderiza en el template; queda como dead-import
// que aparece en el bundle de Vite). Tambien usa $t() y
// $api() inyectados por los plugins, sin importarlos.
const { t } = useNuxtApp();
const { api } = useNuxtApp() as any;
import HiddenPremium from '~/components/HiddenPremium.vue';

useHead({ title: t('app.title') });
</script>

<template>
  <div>
    <header class="fx-top">
      <NuxtLink to="/">{{ t('nav.home') }}</NuxtLink>
      <NuxtLink to="/reservas">Reservas</NuxtLink>
      <NuxtLink to="/perfil">Perfil</NuxtLink>
      <NuxtLink to="/notificaciones">Notificaciones</NuxtLink>
    </header>
    <main>
      <h1>Bienvenido a fx-vue-nuxt</h1>
      <p>Esta aplicacion demuestra auto-imports, middlewares via
         definePageMeta, plugins provide y stores Pinia cross-call.</p>
    </main>
  </div>
</template>
