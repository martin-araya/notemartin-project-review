# Fixture F06n — fx-kotlin-ktor

Servicio **Ktor 3** con corrutinas, inyeccion de dependencias
via **Koin 4**, persistencia con **Exposed 1**, serializacion
JSON via **kotlinx.serialization**. Plantada para que la skill
tenga que rastrear las trampas clasicas del ecosistema Kotlin:

## Stack

- **Lenguaje:** Kotlin 2.0 (JVM 21).
- **Framework:** Ktor 3.0 (server-core + server-netty + server-test-host).
- **DI:** Koin 4.0 (koin-ktor + koin-core + koin-test).
- **Persistencia:** Exposed 1.0 (DAO + JDBC) + H2 + Flyway 10.
- **Serializacion:** kotlinx.serialization 1.7.
- **Concurrencia:** kotlinx.coroutines 1.8 (Flow, launch, async).
- **Build:** Gradle 8.10 (Kotlin DSL).
- **Tests:** JUnit 5 + ktor-server-test-host + koin-test.

## Como se ejecutan los tests

```bash
make test           # gradle test --console=plain
make build          # gradle build -x test
make history        # regenera la historia git (8 commits)
```

En contenedor (con JDK 21 + Gradle 8.10):

```bash
python dev/tools/run_fixture_tests.py --fixture fx-kotlin-ktor --container
```

## Estructura

- `build.gradle.kts`: Kotlin 2.0, Ktor 3.0.1, Koin 4.0, Exposed 1.0,
  kotlinx-serialization 1.7, kotlinx-coroutines 1.8, H2 2.2, Flyway 10,
  JUnit 5.10, ktor-server-test-host.
- `settings.gradle.kts`: `rootProject.name = "fx-kotlin-ktor"`.
- `gradle.properties`: `kotlin.code.style=official`.
- `src/main/kotlin/com/example/fxktor/`:
  - `FxKtorApplication.kt`: `fun main() { embeddedServer(...) }`.
  - `plugins/`: Routing.kt, Auth.kt, StatusPages.kt,
    Serialization.kt, Monitoring.kt (extension functions sobre
    Application o Pipeline).
  - `di/AppModule.kt`: Koin module con `single { ... }` y
    `factory { ... }`.
  - `domain/`: Item.kt (`@Serializable data class`),
    StockEvent.kt (`@Serializable sealed class` + subtipos),
    Alert.kt.
  - `repository/`: ItemRepository.kt (Exposed `Table` + DAO),
    AlertRepository.kt.
  - `service/`: InventarioService.kt (suspend + Flow),
    AlertasService.kt (launch en app scope).
  - `routes/`: InventarioRoutes.kt, ReservasRoutes.kt,
    AlertasRoutes.kt (extension functions sobre Route).
- `src/test/kotlin/com/example/fxktor/`:
  - `FxKtorApplicationTests.kt`, `routes/`, `di/`, `domain/`,
  - `traps_ecosystem/`, `traps_package/`, `traps_superficial/`.

## Features

1. **inventario** (FEAT-001): listar, obtener, crear, actualizar,
   eliminar. 7 R-NN.
2. **reservas-de-stock** (FEAT-002): reservar, liberar, listar
   activas. 7 R-NN.
3. **alertas** (FEAT-003): emitir, listar, validar nivel. 7 R-NN.

## Trampas plantadas

- 6 del ecosistema (CC-06): DSL de routing anidado, plugins
  instalados, extension functions y properties, corrutinas en
  app scope + Flow, sealed class + when exhaustivo, propiedades
  delegadas (by lazy, by inject).
- 6 del paquete (CC-04): routing sin install(Auth) previo,
  sealed class con when no exhaustivo, Flow sin buffer, by inject
  en propiedad no lazy, Exposed sin transaccion, kotlinx.serialization
  con sealed class.
- 3 superficiales (CC-05): ItemRoute dead, sendEmail dead,
  DummyLogger dead.
