import type { FxElectronApi } from './index';

/**
 * Helper declarado pero NO invocado en runtime (trampa S3).
 * La skill debe detectar que este helper no se usa.
 */
export function formatTimestamp(ts: number): string {
  const d = new Date(ts);
  return d.toISOString();
}

declare global {
  interface Window {
    api: FxElectronApi;
  }
}

export {};