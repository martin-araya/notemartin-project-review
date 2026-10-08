import React from 'react';
import { Platform, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useRoute, type RouteProp } from '@react-navigation/native';

import { useAppDispatch, useAppSelector } from '@app/store/hooks';
import { PaymentsController } from '@features/payments/application/PaymentsController';
import { Routes } from '@app/navigation/routes';
import type { Payment } from '@app/store/slices/paymentsSlice';

type PayRoute = RouteProp<Record<string, { orderId: string }>, string>;

export function PaymentsScreen() {
  const dispatch = useAppDispatch();
  const route = useRoute<PayRoute>();
  const initialOrderId = (route.params as any)?.orderId ?? 'order-default';
  const items = useAppSelector((s) => s.payments.items);
  const isProcessing = useAppSelector((s) => s.payments.isProcessing);
  const lastError = useAppSelector((s) => s.payments.lastError);
  const controller = React.useMemo(() => new PaymentsController(dispatch), [dispatch]);

  const handlePay = async () => {
    await controller.startProcessing(initialOrderId, 9.99);
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Pagos NFC</Text>
      <Text>Pedido: {initialOrderId}</Text>
      <Text>Plataforma: {Platform.OS}</Text>

      <TouchableOpacity
        accessibilityRole="button"
        style={[styles.button, isProcessing && styles.buttonDisabled]}
        disabled={isProcessing}
        onPress={handlePay}
      >
        <Text style={styles.buttonText}>
          {isProcessing ? 'Procesando...' : 'Pagar $9.99'}
        </Text>
      </TouchableOpacity>

      {lastError && (
        <View style={styles.error}>
          <Text style={styles.errorText}>{lastError}</Text>
        </View>
      )}

      <Text style={styles.subtitle}>Historial reciente</Text>
      {items.slice(-5).reverse().map((p: Payment) => (
        <View key={p.id} style={styles.item}>
          <Text>#{p.orderId} - {p.amount} {p.currency}</Text>
          <Text>Tag: {p.tagId} ({p.status})</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 12 },
  subtitle: { fontSize: 18, marginTop: 16, marginBottom: 8 },
  button: { backgroundColor: '#6750A4', padding: 16, borderRadius: 8, alignItems: 'center', marginVertical: 16 },
  buttonDisabled: { backgroundColor: '#9b8ec2' },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
  error: { backgroundColor: '#fee2e2', padding: 12, borderRadius: 6 },
  errorText: { color: '#7f1d1d' },
  item: { paddingVertical: 6, borderBottomWidth: 1, borderColor: '#eee' },
});