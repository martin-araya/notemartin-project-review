import React from 'react';
import { ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

export function PaymentsScreen() {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Pagos NFC (iOS)</Text>
      <Text>Version iOS con NSNFCReaderUsageDescription.</Text>
      <Text>Para iniciar NFC en iOS, llama NFCNDEFReaderSession.begin()</Text>
      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Iniciar NFC iOS</Text>
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