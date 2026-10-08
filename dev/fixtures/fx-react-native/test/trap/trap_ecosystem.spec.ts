import { readFileSync } from 'fs';
import { join } from 'path';

const fixtureRoot = join(__dirname, '../..');

describe('Ecosystem traps', () => {
  it('E1 native module name RtcNfcManager', () => {
    const nfcManager = readFileSync(
      join(fixtureRoot, 'src/features/payments/data/NfcManager.ts'),
      'utf8'
    );
    expect(nfcManager).toContain('NativeModules.RtcNfcManager');

    const kotlin = readFileSync(
      join(fixtureRoot, 'android_stub/NfcManagerModule.kt'),
      'utf8'
    );
    expect(kotlin).toContain('@ReactModule(name = "RtcNfcManager")');

    const swift = readFileSync(
      join(fixtureRoot, 'ios_stub/NfcManagerModule.swift'),
      'utf8'
    );
    expect(swift).toContain('RtcNfcManager');
  });

  it('E2 platform files .ios.tsx and .android.tsx', () => {
    expect(
      readFileSync(join(fixtureRoot, 'src/features/payments/presentation/PaymentsScreen.ios.tsx'), 'utf8')
    ).toContain('Pagos NFC (iOS)');
    expect(
      readFileSync(join(fixtureRoot, 'src/features/payments/presentation/PaymentsScreen.android.tsx'), 'utf8')
    ).toContain('Pagos NFC (Android)');
  });

  it('E3 Expo config plugins', () => {
    const appJson = readFileSync(join(fixtureRoot, 'app.json'), 'utf8');
    expect(appJson).toContain('./plugins/withNfc');
    expect(appJson).toContain('./plugins/withDeepLinking');
    expect(appJson).toContain('expo-build-properties');
    expect(appJson).toContain('expo-notifications');
  });

  it('E4 deep linking config', () => {
    const linking = readFileSync(
      join(fixtureRoot, 'src/navigation/linkingConfig.ts'),
      'utf8'
    );
    expect(linking).toContain('fxrn://');
    expect(linking).toContain('Linking.createURL');
    expect(linking).toContain('screens');
  });

  it('E5 Metro aliases', () => {
    const metro = readFileSync(join(fixtureRoot, 'metro.config.js'), 'utf8');
    expect(metro).toContain("'@app'");
    expect(metro).toContain("'@features'");
    expect(metro).toContain('extraNodeModules');

    const babel = readFileSync(join(fixtureRoot, 'babel.config.js'), 'utf8');
    expect(babel).toContain('module-resolver');
  });

  it('E6 notification handler background', () => {
    const handler = readFileSync(
      join(fixtureRoot, 'src/features/notifications/application/NotificationHandler.ts'),
      'utf8'
    );
    expect(handler).toContain('setNotificationHandler');
    expect(handler).toContain('handleNotification');
    expect(handler).toContain('getExpoPushTokenAsync');
  });
});