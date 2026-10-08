import { NativeModules, Platform } from 'react-native';

export interface NfcReadResult {
  tagId: string;
  type: string;
  payload?: string;
}

interface RtcNfcManagerNative {
  start(): Promise<void>;
  stop(): Promise<void>;
  readTag(): Promise<NfcReadResult>;
  requestPermissions(): Promise<'granted' | 'denied'>;
}

/**
 * Trampa E1: Trampa E1: el modulo nativo `RtcNfcManager` se resuelve por nombre
 * a traves del bridge `NativeModules`. Si el modulo no esta linkeado en
 * runtime, el crash ocurre al invocar.
 */
const RtcNfcManager: RtcNfcManagerNative | undefined =
  NativeModules.RtcNfcManager;

export class NfcManager {
  static async start(): Promise<void> {
    // Trampa P5: no verifica permisos antes de invocar el bridge en Android.
    if (!RtcNfcManager) {
      throw new Error('RtcNfcManager module not linked');
    }
    return RtcNfcManager.start();
  }

  static async readTag(): Promise<NfcReadResult | null> {
    // Trampa P1: sin try/catch. Un error del bridge crashea la app.
    if (!RtcNfcManager) {
      throw new Error('RtcNfcManager module not linked');
    }
    return RtcNfcManager.readTag();
  }

  static async stop(): Promise<void> {
    if (!RtcNfcManager) return;
    return RtcNfcManager.stop();
  }

  static getPlatform(): 'ios' | 'android' {
    return Platform.OS as 'ios' | 'android';
  }

  static async requestPermissions(): Promise<'granted' | 'denied'> {
    if (!RtcNfcManager) return 'denied';
    return RtcNfcManager.requestPermissions();
  }
}