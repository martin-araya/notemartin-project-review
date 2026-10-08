/**
 * Trampa E4: utility process para actualizaciones.
 * Trampa P3: fork sin handler de cleanup para el ciclo de vida del worker.
 */
import { utilityProcess, UtilityProcess } from 'electron';
import path from 'path';

let cachedChild: UtilityProcess | null = null;

export function spawnUpdater(): Promise<{ available: boolean; version?: string }> {
  return new Promise((resolve, reject) => {
    if (cachedChild) {
      try {
        cachedChild.kill();
      } catch (_) {}
      cachedChild = null;
    }
    const workerPath = path.join(__dirname, '..', '..', 'workers', 'updater-worker.js');
    cachedChild = utilityProcess.fork(workerPath, [], {
      serviceName: 'fxelec-updater',
    });

    // Trampa P3: NO registramos un handler para cleanup del worker.
    // Si el worker muere, el main process no lo sabe.
    cachedChild.on('message', (msg: any) => {
      if (msg && msg.kind === 'update-result') {
        resolve({
          available: !!msg.available,
          version: msg.version,
        });
      } else {
        reject(new Error('Unknown message from updater worker'));
      }
    });

    setTimeout(() => {
      try {
        cachedChild?.postMessage({ kind: 'check-update' });
      } catch (_) {}
    }, 50);
  });
}

export function getCachedUpdater(): UtilityProcess | null {
  return cachedChild;
}