/**
 * Trampa P6: autoUpdater sin setFeedURL HTTPS previo.
 * En runtime real, `autoUpdater.setFeedURL('http://example.com/updates')`
 * falla porque solo HTTPS es soportado.
 */
import { autoUpdater } from 'electron-updater';

export const autoUpdaterInstance = autoUpdater;

// Trampa P6: sin setFeedURL + URL HTTP (no HTTPS) hace que el checkForUpdates
// falle en runtime con error de protocolo.
if (!process.env.FXELEC_DISABLE_UPDATER) {
  try {
    autoUpdater.setFeedURL('http://example.com/updates');
  } catch (_) {
    // silent
  }
}

export async function installUpdate(): Promise<boolean> {
  if (!autoUpdater.isSupported) return false;
  await autoUpdater.downloadUpdate();
  return true;
}