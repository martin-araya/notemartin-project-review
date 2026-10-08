# Ground truth — fx-kotlin-android (F06ac)

Fixture Android Kotlin 2.0 con Jetpack Compose + Views XML heredadas + Hilt + Room + WorkManager + flavors free/paid + Navigation Component con deep links. Ver `ground_truth.json` para el detalle y este documento para la explicacion humana.

## Resumen

| Item | Valor |
|---|---|
| Stack | Kotlin 2.0.21, AGP 8.7.2, Gradle 8.10.2, JDK 21 |
| Plataforma | Android 7.0+ (minSdk=24) hasta Android 15 (compileSdk=35) |
| Flavors | `free` / `paid` con source sets distintos |
| Features | 4: escaneo-de-productos, historial, sincronizacion-en-segundo-plano, funcion-premium |
| R-NN totales | 28 (7 por feature) |
| Trampas ecosistema | 6 (E1..E6) |
| Trampas paquete | 6 (P1..P6) |
| Trampas superficiales | 3 (S1..S3) |
| Surfaces | 11 (Activity + composables + deeplinks + receiver + worker + service) |
| Unique tokens | 38 con prefijo `NPRGT-FXANDROID-` |

## Trampas del ecosistema

1. **TRAP-E1 — android_manifest_components** (`AndroidManifest.xml:18`): Activity, Receiver y Service declarados en el manifest que NO se llaman desde codigo Kotlin.
2. **TRAP-E2 — hilt_generated_code** (`FxAndroidApp.kt:5`): `@HiltAndroidApp` + `@AndroidEntryPoint` + `@HiltViewModel` generan `Hilt_*` que vive en `app/build/generated/hilt/`.
3. **TRAP-E3 — room_dao_query** (`HistoryDao.kt:13`): DAOs con `@Query` SQL embebido; el SQL es literal string.
4. **TRAP-E4 — gradle_flavors** (`app/build.gradle.kts:33`): `free`/`paid` con source sets distintos; `PremiumEnabled` solo en `paid`.
5. **TRAP-E5 — android_onclick_resource** (`activity_legacy_product.xml:18`): `android:onClick="onSaveClick"` apunta a metodo del Activity por nombre.
6. **TRAP-E6 — workmanager_and_broadcastreceiver_and_deeplinks** (`AndroidManifest.xml:23`): WorkManager + Receiver + deep links en `nav_graph.xml`.

## Trampas del paquete

1. **TRAP-P1 — dao_query_injection_risk** (`HistoryDao.kt:17`): DAO con patron inseguro de SQLi si el caller concatena.
2. **TRAP-P2 — repo_not_singleton** (`AppModule.kt:21`): `ProductRepositoryImpl` sin `@Singleton`.
3. **TRAP-P3 — sync_worker_expedited_silent** (`SyncScheduler.kt:21`): `setExpedited` sin check `POST_NOTIFICATIONS`.
4. **TRAP-P4 — room_no_migrations** (`DatabaseModule.kt:18`): sin `addMigrations`; crash al subir version.
5. **TRAP-P5 — legacy_activity_bypass_repository** (`LegacyProductActivity.kt:31`): `db.execSQL` directo, bypass de Hilt.
6. **TRAP-P6 — scan_viewmodel_silent_catch** (`ScanViewModel.kt:42`): try-catch que no logea ni rethrow.

## Trampas superficiales

1. **TRAP-S1 — legacy_date_formatter_unused** (`LegacyDateFormatter.kt:5`).
2. **TRAP-S2 — env_config_debug_unused** (`EnvConfig.kt:7`).
3. **TRAP-S3 — legacy_fragment_returns_null** (`LegacyProductFragment.kt:7`).

## Features

Ver `ground_truth.json` para el detalle de trazas, decision_points, outcomes y config.