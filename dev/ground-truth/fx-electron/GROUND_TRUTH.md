# Ground truth — fx-electron (F06af)

Fixture Electron 32 con TypeScript 5.5, IPC channels via `ipcMain.handle`/`ipcRenderer.invoke`, `contextBridge` exponiendo `window.api`, menú nativo con accelerators, utility process para actualizaciones, protocolo personalizado `app://`, y electron-builder con `asarUnpack` + `extraResources`. Ver `ground_truth.json` para la maquina y este documento para la explicacion humana.

## Resumen

| Item | Valor |
|---|---|
| Stack | Electron 32.2 + Node 20 + TypeScript 5.5 + esbuild 0.24 + Vitest 2.1 + electron-builder 25.1 |
| Plataforma | Windows, macOS, Linux |
| Features | 3: abrir-proyecto, exportar-pdf, actualización-automática |
| R-NN totales | 21 (7 por feature) |
| Trampas ecosistema | 6 (E1..E6) |
| Trampas paquete | 6 (P1..P6) |
| Trampas superficiales | 3 (S1..S3) |
| Surfaces | 13 (6 IPC + 1 contextBridge + 3 menu accelerators + 1 protocol + 2 workers) |
| Unique tokens | 33 con prefijo `NPRGT-FXELEC-` |

## Trampas del ecosistema

1. **TRAP-E1 — ipc_channels_strings** (`handlers.ts:11`): 6 channels IPC por string.
2. **TRAP-E2 — context_bridge_api** (`preload/index.ts:24`): `window.api` con 6 funciones.
3. **TRAP-E3 — menu_native_accelerators** (`appMenu.ts:11`): Menu.buildFromTemplate con File/Edit/View/Help.
4. **TRAP-E4 — utility_process_and_child_process** (`updater.ts:13`): `utilityProcess.fork` + `child_process.fork`.
5. **TRAP-E5 — app_protocol_custom_scheme** (`appProtocol.ts:18`): `protocol.handle('app', ...)` + `registerSchemesAsPrivileged`.
6. **TRAP-E6 — electron_builder_asar_unpack** (`electron-builder.yml:18`): `asarUnpack` + `extraResources`.

## Trampas del paquete

1. **TRAP-P1 — ipc_no_try_catch** (`handlers.ts:54`): `fs.readFile` sin try/catch.
2. **TRAP-P2 — menu_accelerator_duplicated** (`appMenu.ts:24`): `CmdOrCtrl+O` en dos items.
3. **TRAP-P3 — utility_process_no_exit_handler** (`updater.ts:13`): sin `child.on('exit', ...)`.
4. **TRAP-P4 — context_bridge_function_trap** (`preload/index.ts:24`): no se exponen `Function` no serializables.
5. **TRAP-P5 — protocol_no_register_privileged** (`appProtocol.ts:18`): `registerSchemesAsPrivileged` debe ir antes de `app.ready()`.
6. **TRAP-P6 — autoupdater_http_not_https** (`autoUpdater.ts:13`): `setFeedURL` con `http://` falla.

## Trampas superficiales

1. **TRAP-S1 — legacy_logger_unused** (`legacyLogger.ts:5`).
2. **TRAP-S2 — feature_flags_unread** (`featureFlags.ts:5`).
3. **TRAP-S3 — format_timestamp_unused** (`api.ts:8`).

## Features

Ver `ground_truth.json` para el detalle de trazas, decision_points, outcomes y config.

## Limitacion operativa

Los tests NO requieren display real gracias a `xvfb-run -a` (Linux) o son headless en macOS. `ipcMain`/`ipcRenderer` se mockean con `vi.mock('electron')`. El `utilityProcess` se mockea para evitar fork real.