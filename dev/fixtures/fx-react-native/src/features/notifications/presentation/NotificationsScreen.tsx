import React from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';

import { useAppSelector } from '@app/store/hooks';

export function NotificationsScreen() {
  const token = useAppSelector((s) => s.notifications.token);
  const permission = useAppSelector((s) => s.notifications.permission);
  const scheduleId = useAppSelector((s) => s.notifications.scheduleId);

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Notificaciones Push</Text>
      <View style={styles.row}>
        <Text style={styles.label}>Token:</Text>
        <Text style={styles.value}>{token ?? '(no registrado)'}</Text>
      </View>
      <View style={styles.row}>
        <Text style={styles.label}>Permiso:</Text>
        <Text style={styles.value}>{permission}</Text>
      </View>
      <View style={styles.row}>
        <Text style={styles.label}>Schedule:</Text>
        <Text style={styles.value}>{scheduleId ?? '(ninguno)'}</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 12 },
  row: { flexDirection: 'row', paddingVertical: 4 },
  label: { fontWeight: '600', marginRight: 8 },
  value: { flex: 1 },
});