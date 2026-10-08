# Ground truth — fx-react-native (F06ae)

Fixture React Native 0.74 con Expo SDK 51 bare workflow, TurboModules Kotlin/Swift, Redux Toolkit, React Navigation, plugins Expo que modifican `prebuild`, deep linking, Metro aliases y notificaciones push. Ver `ground_truth.json` para la maquina y este documento para la explicacion humana.

## Resumen

| Item | Valor |
|---|---|
| Stack | RN 0.74.5 + Expo 51 bare + TypeScript 5.4 + RTK 2.2 + RN Navigation 6.1 + Metro 0.51 |
| Plataforma | Android 7+ (minSdk) e iOS 13+ |
| Features | 3: pagos-con-nfc, historial, notificaciones-push |
| R-NN totales | 21 (7 por feature) |
| Trampas ecosistema | 6 (E1..E6) |
| Trampas paquete | 6 (P1..P6) |
| Trampas superficiales | 2 (S1..S2) |
| Surfaces | 10 (5 screens + 2 deep-links + 1 bridge + 2 native handlers) |
| Unique tokens | 34 con prefijo `NPRGT-FXRN-` |

## Trampas del ecosistema

1. **TRAP-E1 — bridge_native_module** (`NfcManager.ts:18`): `NativeModules.RtcNfcManager` resuelve un modulo nativo por string.
2. **TRAP-E2 — platform_file_resolution** (`PaymentsScreen.ios.tsx:6`): Metro selecciona `.ios.tsx` o `.android.tsx` segun plataforma.
3. **TRAP-E3 — expo_config_plugins** (`app.json:30`): 6 plugins que modifican `prebuild`.
4. **TRAP-E4 — deep_linking_config** (`linkingConfig.ts:4`): 3 prefixes + 5 rutas + 2 deepLinks.
5. **TRAP-E5 — metro_aliases** (`metro.config.js:11`): 7 aliases en `extraNodeModules`.
6. **TRAP-E6 — background_notification_handler** (`NotificationHandler.ts:34`): `setNotificationHandler` en background.

## Trampas del paquete

1. **TRAP-P1 — nfc_read_tag_no_catch** (`NfcManager.ts:30`): bridge sin `try/catch`.
2. **TRAP-P2 — redux_slice_direct_mutation** (`paymentsSlice.ts:34`): mutacion directa.
3. **TRAP-P3 — notification_silent_catch** (`NotificationHandler.ts:16`): `catch (_)` silencioso.
4. **TRAP-P4 — linking_config_android_disabled** (`linkingConfig.ts:10`): sin branching Android.
5. **TRAP-P5 — nfc_start_no_permissions** (`NfcManager.ts:23`): sin verificar permiso NFC.
6. **TRAP-P6 — metro_alias_inconsistent** (`metro.config.js:15`): aliases con paths inconsistentes.

## Trampas superficiales

1. **TRAP-S1 — logger_unused** (`logger.ts:3`).
2. **TRAP-S2 — date_format_unused** (`dateFormat.ts:3`).

## Features

Ver `ground_truth.json` para el detalle de trazas, decision_points, outcomes y config.

## Limitacion operativa

Los tests NO requieren emulador Android/iOS gracias a `jest.mock('react-native', ...)` con `NativeModules.RtcNfcManager` mockeado. Los TurboModules nativos (`.kt`/`.swift`) son solo evidencia textual, no se compilan en CI.