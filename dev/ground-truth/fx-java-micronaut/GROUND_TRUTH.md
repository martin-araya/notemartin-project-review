# Ground truth: fx-java-micronaut (F06c)

Fixture de servicio REST Micronaut 4 (Java 21) con DI compile-time, persistencia
JDBC, migraciones Flyway, cliente HTTP declarativo, eventos in-process, scheduler
y configuracion por entornos.

## Vision general

- **Proceso:** un unico JAR Micronaut levantado en JVM 21 con Netty.
- **4 features:** `alta-cliente`, `consulta-score-externo`, `cierre-diario-programado`,
  `notificar-evento`.
- **Bean condicional:** `DataSourceFactory` con `@Requires(env = ...)` y
  `@Requires(notEnv = ...)`.
- **Cliente HTTP declarativo:** `ScoreClient` es interface con `@Client`; sin
  implementacion en el codigo fuente.
- **Precedencia yml:** `application.yml` < `application-{profile}.yml` < env vars.
- **Eventos desacoplados:** `ApplicationEventPublisher` + `@EventListener`.
- **Scheduler:** `DailyCloseScheduler` con `@Scheduled(cron = "${daily-close.cron}")`.
- **Migraciones Flyway:** V1 crea `clientes` y `scores`; V2 crea
  `score_categories` con la columna `categoria_ajustada` consumida solo por
  una `@Query` nativa en `ScoreRepository`.

## 4 features (cada una con >= 6 R-NN)

1. **FEAT-001 alta-cliente** (`POST /clientes`): validacion con `@Valid`,
   rechazo de duplicados por documento, publicacion de `ClienteAltaEvent`.
2. **FEAT-002 consulta-score-externo** (`GET /clientes/score`): llamada
   declarativa al `ScoreClient`; tolera score no disponible con 404.
3. **FEAT-003 cierre-diario-programado** (`@Scheduled`): corre en el cron
   configurado; cuenta clientes; publica `CierreDiarioEvent`.
4. **FEAT-004 notificar-evento** (`@EventListener`): `NotifierService` recibe
   ambos eventos y loguea + agrega a una lista `delivered`.

## 6 trampas del ecosistema (CC-06)

1. **Beans condicionales**: `@Requires(env = "dev")` en `DataSourceFactory`.
2. **`@Client` declarativo**: `ScoreClient` es interface; sin `class`.
3. **Precedencia yml**: `application.yml` < `application-dev.yml` < env vars.
4. **`ApplicationEventPublisher` + `@EventListener`**: emisor y receptor en
   clases distintas.
5. **`@Scheduled(cron = "${...}")`**: la expresion vive en `application.yml`.
6. **Columna agregada por Flyway V2**: `score_categories.categoria_ajustada`
   consumida solo por `@Query` nativa.

## 6 trampas del paquete (CC-04)

1. `timeoutMs = 0` en `ScoreClientConfig` deshabilita el timeout.
2. `ClienteService.alta` traga la excepcion del publisher.
3. `ClienteService.alta` sin `@Transactional`: race condition.
4. `DailyCloseScheduler.run` con `config.enabled=false` no publica; con
   `config=null` lanza NPE.
5. `ScoreService.forDocumento("")` no valida y retorna `Optional.empty()`.
6. `@EventListener` registrado aunque la DI falle al primer evento (lazy).

## Decisiones y variantes

- **Imagen Docker `gradle:8.10-jdk21-jammy`**: trae JDK 21 + Gradle 8.10
  pre-instalados. El host de desarrollo no necesita ni uno ni otro.
- **H2 en memoria para tests**: `application-test.yml` apunta a
  `jdbc:h2:mem:test` y deshabilita el scheduler (`daily-close.enabled: false`).
- **`@MockBean(ScoreClient.class)`**: los tests de `ScoreService` mockean
  el cliente declarativo para evitar la red.
- **Flyway como ground truth de la trampa #6**: V2 no agrega nada al modelo
  de Micronaut Data, solo a la BD; la `@Query` nativa es la unica forma de
  consumir `categoria_ajustada`.
