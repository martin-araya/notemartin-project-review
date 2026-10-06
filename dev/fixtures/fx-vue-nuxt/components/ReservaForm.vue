<script setup lang="ts">
// components/ReservaForm.vue
// Formulario de nueva reserva. Usa defineModel para v-model
// personalizado (Vue 3.4+) y defineEmits para 'submit'/'cancelar'.
// El handler interno de submit hace preventDefault y emite 'submit'
// al padre. Trampa: el preventDefault se aplica tambien al
// submit del padre, asi que si el padre tiene un form propio
// nunca recibe el submit.
const fecha = defineModel<string>('fecha', { default: '' });
const personas = defineModel<number>('personas', { default: 2 });
const sala = defineModel<string>('sala', { default: 'A' });

const emit = defineEmits<{
  (e: 'submit', payload: { fecha: string; personas: number; sala: string }): void;
  (e: 'cancelar'): void;
}>();

function onSubmit(ev: Event) {
  ev.preventDefault();
  emit('submit', { fecha: fecha.value, personas: personas.value, sala: sala.value });
}
</script>

<template>
  <form class="fx-form" @submit="onSubmit">
    <label>Fecha
      <input v-model="fecha" type="text" placeholder="YYYY-MM-DDTHH:MM:SS" />
    </label>
    <label>Personas
      <input v-model.number="personas" type="number" min="1" max="20" />
    </label>
    <label>Sala
      <select v-model="sala">
        <option value="A">A</option>
        <option value="B">B</option>
        <option value="C">C</option>
      </select>
    </label>
    <button type="submit">Reservar</button>
    <button type="button" @click="emit('cancelar')">Cancelar</button>
  </form>
</template>
