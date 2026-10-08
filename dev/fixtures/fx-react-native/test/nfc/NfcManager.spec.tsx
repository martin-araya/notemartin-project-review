import { NfcManager } from '../../src/features/payments/data/NfcManager';

describe('NfcManager', () => {
  it('start resolves on success', async () => {
    await expect(NfcManager.start()).resolves.not.toThrow();
  });

  it('readTag returns a tag', async () => {
    const tag = await NfcManager.readTag();
    expect(tag).toEqual({ tagId: 'fxrn-test', type: 'ISO14443A' });
  });

  it('platform detection', () => {
    expect(['ios', 'android']).toContain(NfcManager.getPlatform());
  });

  it('requestPermissions returns granted', async () => {
    await expect(NfcManager.requestPermissions()).resolves.toBe('granted');
  });
});