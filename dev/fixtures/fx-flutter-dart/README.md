# fx-flutter-dart

Fixture F06ad. App Flutter multiplataforma con Riverpod (state management) + go_router (navegación declarativa con redirects) + freezed/json_serializable (modelos inmutables generados) + build_runner (generación de código) + platform channels a Kotlin/Swift nativos + flavors con `--dart-define`.

## Stack

- Flutter 3.24.5 con Dart 3.5.4 (canal stable)
- `flutter_riverpod` 2.5.1 + `riverpod_generator` 2.4.0
- `go_router` 14.2.7
- `freezed` 2.5.7 + `json_serializable` 6.8.0 + `build_runner` 2.4.13
- `shared_preferences` 2.3.2 para favoritos
- Platform channels (`MethodChannel('com.example.fxdart/native')`) con stubs Kotlin/Swift
- Flavors via `--dart-define=FX_ENABLE_PREMIUM=true/false`
- Widgets adaptativos iOS/Android

## Trampas ejercitadas

### Ecosistema (E1‑E6)

1. `.g.dart` y `.freezed.dart` generados por `build_runner` (no commiteados al repo, generados en CI)
2. Providers Riverpod que se observan entre sí via `ref.watch(readerControllerProvider)` (grafo implícito)
3. Platform channels: métodos invocados por string `'scanDocument'`, `'capturePage'`
4. `go_router` con redirects declarativos
5. Flavors via `--dart-define=FX_ENABLE_PREMIUM`
6. Widgets adaptativos iOS/Android (CupertinoSlider vs SliderMaterial)

### Paquete (P1‑P6)

1. AsyncNotifier sin `try/catch` (error sin manejar)
2. `MethodChannel.invokeMethod` con `catch (_) {}` silencioso
3. `go_router` redirect que ignora auth
4. `SharedPreferences.getBool` + `dart-define` con orden de evaluación invertido
5. `copyWith` freezed generado pero no usado (warning conceptual)
6. AdaptiveSlider con rama iOS muerta

### Superficiales (S1‑S3)

1. `util/logger.dart` con `Logger.print` nunca invocado
2. `_DEFAULT_LOCALE` declarado pero no usado
3. `_formatDouble` helper muerto en `platform_widget.dart`

## Features y R-NN

| Feature | R-NN | Cubre trampas |
|---|---|---|
| `lector-de-documentos` | 7 (R-01..R-07) | E1, E3, E6, P1, P2, R-07 deep link |
| `favoritos` | 7 (R-01..R-07) | E2, E1, P4, R-07 desde notificación |
| `ajustes` | 7 (R-01..R-07) | E5, E6, P3, P6, R-04 navegación rota |

## Cómo correr

### En Linux/macOS con Flutter instalado

```bash
cd dev/fixtures/fx-flutter-dart
flutter pub get
dart run build_runner build --delete-conflicting-outputs
flutter test
```

### En contenedor

```bash
docker build -f dev/fixtures/fx-flutter-dart/Dockerfile.test -t npr-fx-flutter-dart dev/fixtures/fx-flutter-dart/
docker run --rm npr-fx-flutter-dart
```

### Vía runner

```bash
python dev/tools/run_fixture_tests.py --fixture fx-flutter-dart --container
```

## Limitación documentada

Los archivos `.g.dart` y `.freezed.dart` generados por `build_runner` **NO se commitean** al repo (ver `.gitignore`). Esto evita CC-11 con tokens en archivos generados. CI los genera en runtime con `dart run build_runner build --delete-conflicting-outputs`.