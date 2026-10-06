<script setup lang="ts">
// Listado de avisos con filtro de no leidas. Cada item usa el
// componente NotificacionItem (auto-import) que emite 'mark-read'
const { items, unread, loading, refresh, markRead } = useNotificationsStore();
const filter = ref<'all' | 'unread'>('all');

const visible = computed(() => filter.value === 'unread' ? unread : items);

onMounted(() => { refresh('u-1'); });
</script>

<template>
  <div>
    <h1>Avisos</h1>
    <select v-model="filter">
      <option value="all">Todas</option>
      <option value="unread">No leidas</option>
    </select>
    <p v-if="loading">Cargando...</p>
    <ul v-else class="fx-list">
      <NotificacionItem
        v-for="n in visible"
        :key="n.id"
        :notificacion="n"
        @mark-read="markRead(n.id)"
      />
    </ul>
  </div>
</template>
