# fx-react-native

Fixture F06ae. App React Native 0.74 con Expo 51 bare workflow, módulos nativos (TurboModules) Kotlin/Swift, Redux Toolkit, React Navigation, plugins Expo que modifican `prebuild`, deep linking, Metro aliases y notificaciones push.

## Stack

- React Native 0.74.5 con Expo SDK 51 bare workflow
- TypeScript 5.4
- `@reduxjs/toolkit` 2.2 + `react-redux` 9.1
- `@react-navigation/native` 6.1 + `@react-navigation/native-stack` 6.9
- Metro 0.51.2 con `resolver.extraNodeModules` (aliases `@app` + `@features`)
- Babel 7 + `babel-plugin-module-resolver`
- `expo-build-properties` + `expo-notifications` + `expo-linking` + `expo-splash-screen`
- TurboModules `RtcNfcManager` con stubs Kotlin/Swift
- `react-native-nfc-manager` como fallback
- Jest 29 + `@testing-library/react-native` 12.5 (sin emulador)

## Trampas ejercitadas

### Ecosistema (E1‑E6)

1. TurboModules `RtcNfcManager` resueltos por nombre via `NativeModules`
2. Archivos por plataforma `.ios.tsx`/`.android.tsx` resueltos por Metro
3. Expo config plugins que modifican `prebuild`
4. Deep linking via `linkingConfig.ts` con 3 schemes
5. Metro aliases via `metro.config.js` + `babel-plugin-module-resolver`
6. Notification handlers en background via `expo-notifications`

### Paquete (P1‑P6)

1. `NativeModules.RtcNfcManager.readTag()` sin `try/catch`
2. Redux slice que mutea state directamente sin `immer`
3. `NotificationHandler` que traga errores con `catch (_)`
4. `linkingConfig.ts` con `enabled: false` en Android
5. `NfcManager.start()` sin verificar permisos NFC
6. Metro alias inconsistente entre `.ios.tsx` y `.android.tsx`

### Superficiales (S1‑S3)

1. `util/logger.ts` con `Logger.log` no invocado
2. `util/dateFormat.ts` con `formatDate` no usado
3. `NfcManager.ios.ts` con helper `formatIsoString` declarado pero no usado

## Features y R-NN

| Feature | R-NN | Cubre trampas |
|---|---|---|
| `pagos-con-nfc` | 7 (R-01..R-07) | E1, E2, E4, P1, P5, R-07 deep link |
| `historial` | 7 (R-01..R-07) | E2 Redux, R-07 desde notificación |
| `notificaciones-push` | 7 (R-01..R-07) | E6, P3, P4 |

## Cómo correr

### En Linux/macOS con Node 20 + Yarn

```bash
cd dev/fixtures/fx-react-native
yarn install --frozen-lockfile
yarn jest --no-coverage
```

### En contenedor

```bash
docker build -f dev/fixtures/fx-react-native/Dockerfile.test -t npr-fx-react-native dev/fixtures/fx-react-native/
docker run --rm -v $(pwd)/dev/fixtures/fx-react-native/.yarn-cache:/app/.yarn-cache npr-fx-react-native
```

### Vía runner

```bash
python dev/tools/run_fixture_tests.py --fixture fx-react-native --container
```

## Limitación documentada

Los tests NO requieren emulador Android/iOS gracias a `jest.mock('react-native', ...)` con `NativeModules.RtcNfcManager` mockeado. Los TurboModules nativos (`.kt`/`.swift`) son solo evidencia textual, no se compilan en CI.