// components/PerfilEditor.vue
// Editor inline con v-model sobre el objeto completo. No se usa
// en las paginas actuales; queda como componente disponible para
// uso futuro. El grep en pages/ confirma que ninguna pagina lo
// renderiza.
import { ref, watch } from 'vue';

const props = defineProps<{ profile: any }>();
const emit = defineEmits<{ (e: 'save', patch: any): void }>();

const local = ref({ ...(props.profile || {}) });
watch(() => props.profile, (p) => { local.value = { ...(p || {}) }; });
</script>

<template>
  <form class="fx-form" @submit.prevent="emit('save', local)">
    <label>Nombre <input v-model="local.nombre" type="text" /></label>
    <label>Email <input v-model="local.email" type="email" /></label>
    <button type="submit">Guardar</button>
  </form>
</template>
