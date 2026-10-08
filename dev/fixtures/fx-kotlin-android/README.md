# fx-kotlin-android

Fixture F06ac. App Android Kotlin 2.0 con Jetpack Compose, vistas XML heredadas con ViewBinding, Hilt (DI), Room (persistencia), WorkManager (background), flavors free/paid y Navigation Component con deep links.

## Stack

- Kotlin 2.0.21 + KSP 2.0.21
- Android Gradle Plugin 8.7.2 con Gradle 8.10.2
- compileSdk = 35, minSdk = 24, targetSdk = 35
- JDK 21
- Hilt 2.51.1 con `@HiltAndroidApp` + `@AndroidEntryPoint` + `@HiltViewModel`
- Jetpack Compose (BOM 2024.10.00) + Material 3
- AppCompatActivity + ViewBinding (vista legacy)
- Room 2.6.1 con DAO anotados
- WorkManager 2.10.0 + CoroutineWorker
- Navigation Compose 2.8.4 + nav_graph.xml con deep links
- Gradle flavors `free` / `paid`
- Robolectric 4.13 para tests JVM

## Trampas ejercitadas

### Ecosistema (E1‑E6)

1. `AndroidManifest.xml` con Activity, Receiver, Service e intent filters (no en código)
2. Hilt con código generado `@Hilt_*` (no en `Sources/`)
3. Room DAO con `@Query` SQL embebido
4. Flavors `free`/`paid` con source sets distintos
5. Recursos `R.*` + layouts XML con `android:onClick`
6. WorkManager + `BroadcastReceiver` + deep links

### Paquete (P1‑P6)

1. `@Query` Room con concatenación vulnerable
2. Repository sin `@Singleton`
3. `SyncWorker` expedited sin check `POST_NOTIFICATIONS`
4. Room sin `addMigrations` (crashea al subir versión)
5. `LegacyProductActivity.onSaveClick` con `db.execSQL` directo
6. `ScanViewModel` con try-catch silencioso

### Superficiales (S1‑S3)

1. `LegacyDateFormatter` sin consumidores
2. `EnvConfig.BuildConfig.DEBUG` no usado
3. `LegacyProductFragment.onCreateView` devuelve `null`

## Features y R-NN

| Feature | R-NN | Cubre trampas |
|---|---|---|
| `escaneo-de-productos` | 7 (R-01..R-07) | E1, E3, E5, P6, R-07 deep link |
| `historial` | 7 (R-01..R-07) | E5, E6, R-07 desde notificación |
| `sincronización-en-segundo-plano` | 7 (R-01..R-07) | E1, E6, P3, P4 |
| `funcion-premium` | 7 (R-01..R-07) | E4 (solo `paid`), P2 (DI falla en `free`) |

## Cómo correr

### En Linux (contenedor)

```bash
docker build -f dev/fixtures/fx-kotlin-android/Dockerfile.test -t npr-fx-kotlin-android dev/fixtures/fx-kotlin-android/
docker run --rm -v $(pwd)/dev/fixtures/fx-kotlin-android/.gradle-cache:/app/.gradle npr-fx-kotlin-android
```

### En macOS con Android SDK instalado

```bash
cd dev/fixtures/fx-kotlin-android
ANDROID_HOME=$HOME/Library/Android/sdk ./gradlew test --no-daemon
```

### Vía runner

```bash
python dev/tools/run_fixture_tests.py --fixture fx-kotlin-android --container
```