import React from 'react';
import { PermissionsAndroid, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

async function ensureNfcPermission(): Promise<boolean> {
  if (PermissionsAndroid.PERMISSIONS.NFC) {
    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.NFC,
    );
    return granted === PermissionsAndroid.RESULTS.GRANTED;
  }
  return true;
}

export function PaymentsScreen() {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Pagos NFC (Android)</Text>
      <Text>Version Android con verify permisos antes de NfcManager.start().</Text>
      <TouchableOpacity
        style={styles.button}
        onPress={async () => {
          const ok = await ensureNfcPermission();
          if (!ok) return;
        }}>
        <Text style={styles.buttonText}>Conceder permiso NFC</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 12 },
  button: { backgroundColor: '#6750A4', padding: 16, borderRadius: 8, alignItems: 'center' },
  buttonText: { color: '#fff' },
});