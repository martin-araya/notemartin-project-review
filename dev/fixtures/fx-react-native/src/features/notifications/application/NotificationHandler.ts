import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

import { store } from '@app/store';
import { setToken, setPermission } from '@app/store/slices/notificationsSlice';

/**
 * Trampa E6: registro de notification handler en background + push token.
 * Trampa P3: el handleNotification traga errores con `catch (_) { return {} }`
 * silenciando fallos del handler.
 */
export async function registerNotifications(): Promise<void> {
  // Trampa P3: catch silencioso
  try {
    if (Platform.OS === 'android') {
      await Notifications.setNotificationChannelAsync('default', {
        name: 'default',
        importance: Notifications.AndroidImportance.DEFAULT,
      });
    }
    const { status } = await Notifications.getPermissionsAsync();
    store.dispatch(setPermission(status === 'granted' ? 'granted' : (status as any)));
    const tokenResult = await Notifications.getExpoPushTokenAsync({
      projectId: 'fxrn-project',
    });
    store.dispatch(setToken(tokenResult.data));
  } catch (_) {
    // Trampa P3: error tragado sin log ni rethrow
  }

  // Handler en background
  Notifications.setNotificationHandler({
    handleNotification: async () => {
      try {
        // Simulacion de logica real de background
        return {
          shouldShowAlert: true,
          shouldPlaySound: false,
          shouldSetBadge: false,
          shouldShowBanner: true,
          shouldShowList: true,
        };
      } catch (_) {
        // Trampa P3: error tragado
        return {
          shouldShowAlert: false,
          shouldPlaySound: false,
          shouldSetBadge: false,
          shouldShowBanner: false,
          shouldShowList: false,
        };
      }
    },
  });
}