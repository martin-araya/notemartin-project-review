# Ground truth — fx-flutter-dart (F06ad)

Fixture Flutter 3.24 + Dart 3.5 multiplataforma con Riverpod + go_router + freezed/json_serializable + platform channels a Kotlin/Swift + flavors con `--dart-define`. Ver `ground_truth.json` para la maquina y este para la explicacion humana.

## Resumen

| Item | Valor |
|---|---|
| Stack | Flutter 3.24.5 + Dart 3.5.4 + flutter_riverpod 2.5.1 + go_router 14.2.7 + freezed 2.5.7 + json_serializable 6.8.0 + shared_preferences 2.3.2 |
| Plataforma | Android 5+ (minSdk) y iOS 12+; macOS/Linux para tests |
| Flavors | `--dart-define=FX_ENABLE_PREMIUM=true/false` |
| Features | 3: lector-de-documentos, favoritos, ajustes |
| R-NN totales | 21 (7 por feature) |
| Trampas ecosistema | 6 (E1..E6) |
| Trampas paquete | 6 (P1..P6) |
| Trampas superficiales | 3 (S1..S3) |
| Surfaces | 9 (3 composables + 2 deep-links + 2 platform channels + 2 native handlers) |
| Unique tokens | 35 con prefijo `NPRGT-FXFLUTTER-` |

## Trampas del ecosistema

1. **TRAP-E1 — freezed_generated_code** (`document.dart:5`): build_runner genera `.freezed.dart` y `.g.dart`.
2. **TRAP-E2 — riverpod_ref_watch** (`favorites_controller.dart:20`): `ref.watch(readerControllerProvider)`.
3. **TRAP-E3 — platform_channels_strings** (`native_method_channel.dart:16`): `MethodChannel` invoca por nombre.
4. **TRAP-E4 — go_router_redirects** (`app_router.dart:9`): redirect declarativo.
5. **TRAP-E5 — dart_define_flavor** (`settings_controller.dart:9`): `bool.fromEnvironment`.
6. **TRAP-E6 — adaptive_platform_widgets** (`platform_widget.dart:19`): Cupertino vs Material.

## Trampas del paquete

1. **TRAP-P1 — reader_async_notifier_no_catch** (`reader_controller.dart:15`): `build()` sin try/catch.
2. **TRAP-P2 — platform_channel_silent_catch** (`native_method_channel.dart:16`): `catch (_)`.
3. **TRAP-P3 — router_redirect_ignores_auth** (`app_router.dart:9`): redirect sin chequeo.
4. **TRAP-P4 — settings_dart_define_sp_order** (`settings_controller.dart:38`): orden de evaluacion.
5. **TRAP-P5 — freezed_copyWith_unused** (`document.dart:5`): copyWith generado no usado.
6. **TRAP-P6 — adaptive_slider_cupertino_dead** (`platform_widget.dart:46`): rama iOS usa Material.

## Trampas superficiales

1. **TRAP-S1 — logger_helper_unused** (`logger.dart:5`): `Logger.print` sin consumir.
2. **TRAP-S2 — default_locale_unused** (`settings_controller.dart:13`): `_DEFAULT_LOCALE` sin leer.
3. **TRAP-S3 — format_double_helper_dead** (`platform_widget.dart:73`): `_formatDouble` sin invocar.

## Features

Ver `ground_truth.json` para el detalle de trazas, decision_points, outcomes y config.

## Limitacion operativa

Los archivos `.g.dart` y `.freezed.dart` generados por `build_runner` **NO se commitean** al repo (estan en `.gitignore`). Esto evita CC-11 con tokens en archivos generados. CI los genera en runtime con `dart run build_runner build --delete-conflicting-outputs`.