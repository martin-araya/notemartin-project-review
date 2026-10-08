/**
 * Trampa E5: el protocolo personalizado `app://` requiere que
 * `protocol.registerSchemesAsPrivileged` se llame ANTES de `app.ready`.
 * Si no se hace en orden, `protocol.handle('app', ...)` falla en runtime.
 * La skill debe detectar el orden.
 */
import { protocol, net, app } from 'electron';
import path from 'path';

const SCHEME = 'app';

protocol.registerSchemesAsPrivileged([
  {
    scheme: SCHEME,
    privileges: { standard: true, secure: true, supportFetchAPI: true },
  },
]);

export function registerAppProtocol(): void {
  protocol.handle(SCHEME, async (request) => {
    // Trampa E5 + trampa P5 (orden): si la linea de arriba no se ejecuto,
    // esta linea lanza excepcion porque `app` no esta registrado como privileged.
    const url = new URL(request.url);
    let filePath = url.pathname;
    if (filePath.startsWith('/')) filePath = filePath.slice(1);
    const resolved = path.join(app.getAppPath(), filePath);
    return net.fetch(`file://${resolved}`);
  });
}