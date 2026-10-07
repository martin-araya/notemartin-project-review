# Ground truth de fx-kotlin-ktor (F06n)

Servicio **Ktor 3** con corrutinas, inyeccion Koin, persistencia
Exposed, serializacion kotlinx. Plantada para que la skill tenga
que rastrear las trampas clasicas del ecosistema Kotlin:

## Features

1. **inventario** (FEAT-001): listar, obtener, crear, actualizar,
   eliminar. 7 R-NN.
2. **reservas-de-stock** (FEAT-002): reservar, liberar, listar
   activas. 7 R-NN.
3. **alertas** (FEAT-003): emitir, listar, validar nivel. 7 R-NN.

## Trampas del ecosistema (CC-06)

1. **routing_dsl_nested**: el DSL se reparte entre 3 archivos
   (InventarioRoutes, ReservasRoutes, AlertasRoutes), cada uno
   expone una extension function sobre Route.
2. **plugins_installed**: el orden de `install(...)` en
   FxKtorApplication importa; `auth()` no se invoca.
3. **extension_functions**: properties y functions sobre
   tipos de otros modulos (Route, KoinComponent).
4. **coroutines_app_scope**: `launch` en `CoroutineScope` sin
   cancelar al apagar la app (memory leak).
5. **sealed_class_when**: `when` exhaustivo; agregar un nuevo
   subtipo rompe el handler.
6. **delegated_property**: `by inject()` no es lazy y requiere
   KoinContext.

## Trampas del paquete (CC-04)

1. **routing_no_auth**: endpoints accesibles sin auth.
2. **sealed_class_when_statement**: el when no devuelve valor
   (statement), por lo que el compilador no exige exhaustividad.
3. **flow_no_buffer**: `observedItems()` sin `.buffer()`.
4. **by_inject_in_property**: la inyeccion se evalua en cada
   `get()`.
5. **exposed_no_transaction**: queries sin `transaction { }`.
6. **kotlinx_serialization_sealed**: sealed class con `@Serializable`
   requiere discriminador en el JSON.

## Trampas superficiales (CC-05)

1. **dead_route**: `GET /inv/{id}/audit` retorna lista vacia.
2. **dead_email**: `sendEmail()` con cuerpo vacio.
3. **dead_dummy_logger**: `DummyLogger` declarado en Koin pero
   nunca inyectado.

## Archivos clave del fixture

- `build.gradle.kts`: Kotlin 2.0.21, Ktor 3.0.1, Koin 4.0,
  Exposed 1.0-beta, kotlinx-serialization 1.7, kotlinx-coroutines
  1.8, H2 2.2, Flyway 10, JUnit 5.10, ktor-server-test-host.
- `settings.gradle.kts`: `rootProject.name = "fx-kotlin-ktor"`.
- `src/main/kotlin/com/example/fxktor/FxKtorApplication.kt`:
  `fun main() { embeddedServer(Netty, ...) { install(...); routing { routes() } } }`.
- `plugins/`: Routing.kt, Auth.kt, StatusPages.kt,
  Serializacion.kt, Monitoring.kt (extension functions sobre
  Application o Pipeline).
- `di/AppModule.kt`: Koin module con `single` para repos y
  services.
- `domain/`: Item.kt, StockEvent.kt (sealed), Alert.kt
  (sealed).
- `repository/`: ItemRepository.kt, AlertRepository.kt
  (Exposed DAO + Table).
- `service/`: InventarioService.kt, AlertasService.kt
  (suspend + Flow + CoroutineScope).
- `routes/`: InventarioRoutes.kt, ReservasRoutes.kt,
  AlertasRoutes.kt (extension functions sobre Route).
- `src/test/kotlin/com/example/fxktor/`: FxKtorApplicationTests,
  domain/, traps_ecosystem/, traps_package/,
  traps_superficial/.
