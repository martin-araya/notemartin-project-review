<script setup lang="ts">
// Editor del modulo de cuenta. definePageMeta declara el
// middleware global 'auth' (definido en middleware/auth.global.ts).
definePageMeta({
  middleware: ['auth']
});

const { current, isPremium, update, logout } = useProfile('u-1');

onMounted(async () => {
  const store = useProfileStore();
  if (!store.current) await store.fetch('u-1');
});

const nombre = ref('');
const email = ref('');
watch(current, (p) => {
  if (p) {
    nombre.value = p.nombre;
    email.value = p.email;
  }
}, { immediate: true });

async function onSave() {
  await update({ nombre: nombre.value, email: email.value });
}
</script>

<template>
  <div>
    <h1>Cuenta</h1>
    <form class="fx-form" @submit.prevent="onSave">
      <label>Nombre <input v-model="nombre" type="text" /></label>
      <label>Email <input v-model="email" type="email" /></label>
      <button type="submit">Guardar</button>
    </form>
    <p v-if="isPremium" class="info">Premium</p>
    <button @click="logout">Cerrar sesion</button>
  </div>
</template>
