import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { PaymentsScreen } from '@features/payments/presentation/PaymentsScreen';
import { HistoryScreen } from '@features/history/presentation/HistoryScreen';
import { NotificationsScreen } from '@features/notifications/presentation/NotificationsScreen';
import { linkingConfig } from './linkingConfig';
import { Routes } from './routes';

const Stack = createNativeStackNavigator();

export function RootNavigator() {
  return (
    <Stack.Navigator
      initialRouteName={Routes.PAYMENTS}
      linking={linkingConfig}
      screenOptions={{
        headerStyle: { backgroundColor: '#6750A4' },
        headerTintColor: '#fff',
      }}
    >
      <Stack.Screen name={Routes.PAYMENTS} component={PaymentsScreen} options={{ title: 'Pagos NFC' }} />
      <Stack.Screen name={Routes.HISTORY} component={HistoryScreen} options={{ title: 'Historial' }} />
      <Stack.Screen name={Routes.NOTIFICATIONS} component={NotificationsScreen} options={{ title: 'Notificaciones' }} />
    </Stack.Navigator>
  );
}