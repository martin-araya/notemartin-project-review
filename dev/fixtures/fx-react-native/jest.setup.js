// Mocks para tests Jest del fixture F06ae.
// NativeModules.RtcNfcManager se mockea para no requerir un bridge real.

jest.mock('react-native', () => ({
  NativeModules: {
    RtcNfcManager: {
      start: jest.fn(() => Promise.resolve()),
      stop: jest.fn(() => Promise.resolve()),
      readTag: jest.fn(() => Promise.resolve({ tagId: 'fxrn-test', type: 'ISO14443A' })),
      requestPermissions: jest.fn(() => Promise.resolve('granted')),
    },
  },
  Platform: { OS: 'android', Version: 34 },
  NativeEventEmitter: jest.fn(),
  Dimensions: { get: () => ({ width: 360, height: 640 }) },
  StyleSheet: { create: (s) => s },
  Linking: { createURL: () => 'fxrn://', openURL: jest.fn() },
}));

jest.mock('expo-notifications', () => ({
  setNotificationHandler: jest.fn(),
  getPermissionsAsync: jest.fn(() => Promise.resolve({ status: 'granted' })),
  getExpoPushTokenAsync: jest.fn(() => Promise.resolve({ data: 'ExponentPushToken[fxrn-test]' })),
  scheduleNotificationAsync: jest.fn(),
  addNotificationReceivedListener: jest.fn(),
}));

// Silenciar warnings de React act()
const origError = console.error;
console.error = (...args) => {
  if (typeof args[0] === 'string' && args[0].includes('not wrapped in act')) return;
  origError(...args);
};