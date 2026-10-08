import { readFileSync } from 'fs';
import { join } from 'path';

const fixtureRoot = join(__dirname, '../..');

describe('Package traps', () => {
  it('P1 NfcManager.readTag no try/catch', () => {
    const nfcManager = readFileSync(
      join(fixtureRoot, 'src/features/payments/data/NfcManager.ts'),
      'utf8'
    );
    expect(nfcManager).toContain('readTag');
    // The readTag method should NOT wrap in try/catch (P1)
    const readTagMethod = nfcManager.substring(
      nfcManager.indexOf('static async readTag'),
      nfcManager.indexOf('static async stop')
    );
    expect(readTagMethod.includes('try {')).toBe(false);
  });

  it('P2 paymentsSlice mutates state directly', () => {
    const slice = readFileSync(
      join(fixtureRoot, 'src/store/slices/paymentsSlice.ts'),
      'utf8'
    );
    expect(slice).toContain('state.items.push');
  });

  it('P3 NotificationHandler silent catch', () => {
    const handler = readFileSync(
      join(fixtureRoot, 'src/features/notifications/application/NotificationHandler.ts'),
      'utf8'
    );
    expect(handler).toContain('catch (_)');
  });

  it('P4 linkingConfig not Android-disabled', () => {
    const linking = readFileSync(
      join(fixtureRoot, 'src/navigation/linkingConfig.ts'),
      'utf8'
    );
    expect(linking).toContain('fxrn://');
    expect(linking).not.toContain('Platform.OS === \'android\'');
  });

  it('P5 NfcManager.start does not verify permissions', () => {
    const nfcManager = readFileSync(
      join(fixtureRoot, 'src/features/payments/data/NfcManager.ts'),
      'utf8'
    );
    // start() should NOT call PermissionsAndroid
    expect(nfcManager).not.toContain('PermissionsAndroid');
    expect(nfcManager).not.toContain('requestPermissions');
  });

  it('P6 Metro alias paths consistent', () => {
    const metro = readFileSync(join(fixtureRoot, 'metro.config.js'), 'utf8');
    expect(metro).toContain("'@features': path.resolve(__dirname, 'src/features')");
  });
});