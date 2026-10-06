// Implementacion en TypeScript. Literales: FXMIN_SYNC_OK, FXMIN_SYNC_ERROR.

export const FEATURE_SINCRONIZAR = 'sincronizar';

export function sincronizar(state: 'idle' | 'pending' | 'error'): { status: string; timestamp: string } {
  if (state === 'error') {
    return { status: 'FXMIN_SYNC_ERROR', timestamp: new Date(0).toISOString() };
  }
  return { status: state === 'pending' ? 'pending' : 'FXMIN_SYNC_OK', timestamp: new Date().toISOString() };
}

export function _unusedSyncHelper(): void {
  // empty
}