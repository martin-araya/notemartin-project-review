# fx-electron

Fixture F06af. App Electron 32 con TypeScript 5.5, IPC channels via `ipcMain.handle`/`ipcRenderer.invoke`, `contextBridge` exponiendo `window.api`, menú nativo con accelerators, utility process para actualizaciones, protocolo personalizado `app://`, y electron-builder con `asarUnpack` + `extraResources`.

## Stack

- Electron 32.x con Node 20 integrado
- TypeScript 5.5 con `tsc` para main/preload + esbuild 0.24 para renderer
- Vitest 2.x con mocks del módulo `electron`
- electron-builder con `asarUnpack` + `extraResources` + targets mac/win/linux
- electron-builder.yml como config principal
- Renderer en HTML + JS simple (sin React/Vue para reducir superficie)

## Trampas ejercitadas

### Ecosistema (E1‑E6)

1. IPC channels por string: `ipcMain.handle('project:open', ...)` + `ipcRenderer.invoke('project:open')`
2. `contextBridge` exponiendo `window.api` con superficie tipada
3. Menu nativo con accelerators (`CmdOrCtrl+O`/`CmdOrCtrl+E`/`CmdOrCtrl+U`)
4. Utility process para actualizaciones + child_process para PDF export
5. Protocolo personalizado `app://` (file:// restringido por seguridad)
6. electron-builder config con `asarUnpack` + `extraResources`

### Paquete (P1‑P6)

1. `ipcMain.handle` sin try/catch que lanza excepción no controlada
2. Menu `accelerator` duplicado (`CmdOrCtrl+O` en dos items)
3. `utilityProcess.fork` sin `child.on('exit')` handler
4. `contextBridge` con `Function` no serializable
5. `protocol.handle('app')` sin `protocol.registerSchemesAsPrivileged` previo
6. `autoUpdater.checkForUpdates` sin HTTPS provider

### Superficiales (S1‑S3)

1. `util/legacyLogger.ts` con `log.info` no invocado
2. `util/featureFlags.ts` con `ENABLE_BETA` no leído
3. `preload/api.ts` con `formatTimestamp` no invocado

## Features y R-NN

| Feature | R-NN | Cubre trampas |
|---|---|---|
| `abrir-proyecto` | 7 (R-01..R-07) | E1, E2, E3, E5, P1, R-07 deep link |
| `exportar-pdf` | 7 (R-01..R-07) | E1, E4, E3, P1, R-07 menu bulk |
| `actualización-automática` | 7 (R-01..R-07) | E4, E6, P3, P6, R-06 dev mode |

## Cómo correr

### En Linux con Electron + xvfb

```bash
cd dev/fixtures/fx-electron
yarn install --frozen-lockfile
xvfb-run -a yarn vitest --run
```

### En macOS

```bash
cd dev/fixtures/fx-electron
yarn install --frozen-lockfile
yarn vitest --run
```

### En contenedor

```bash
docker build -f dev/fixtures/fx-electron/Dockerfile.test -t npr-fx-electron dev/fixtures/fx-electron/
docker run --rm -v $(pwd)/dev/fixtures/fx-electron/.yarn-cache:$(HOME)/.cache npr-fx-electron
```

### Vía runner

```bash
python dev/tools/run_fixture_tests.py --fixture fx-electron --container
```

## Limitación documentada

Los tests NO requieren un display real gracias a `xvfb-run -a` (Linux) o son headless en macOS. `ipcMain`/`ipcRenderer` se mockean con `vi.mock('electron')`. El `utilityProcess` se mockea para evitar fork real.