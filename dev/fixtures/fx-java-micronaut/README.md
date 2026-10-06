# fx-java-micronaut (F06c)

Fixture de **servicio REST Micronaut 4** escrito en Java 21. Modela la arquitectura
de un microservicio empresarial con DI compile-time, persistencia JDBC, migraciones
Flyway, cliente HTTP declarativo, eventos in-process, scheduler y configuración por
entornos.

Sirve para que la skill `notemartin-project-review` practique sobre código real de
Java empresarial, con énfasis en:

- **Beans condicionales** vía `@Requires(env = ...)` + `@Factory` (el bean activo
  depende del entorno; un escaneo estático no ve cuál se inyecta en runtime).
- **`@Client` declarativo** para HTTP saliente (la interfaz no tiene
  implementación en el código fuente; el cliente se genera en compilación).
- **Precedencia de configuración** `application.yml` < `application-{profile}.yml`
  < variables de entorno.
- **`ApplicationEventPublisher` + `@EventListener`** desacoplando emisor y receptor.
- **`@Scheduled(cron = "${...}")`** con la expresión en la configuración, no
  hardcodeada.
- **Flyway** con migraciones incrementales (V1, V2) y `@Query` nativa que depende
  de columnas agregadas por V2.

## Estructura

```
src/main/java/com/fxmicronaut/
  Application.java                  arranque Micronaut
  config/                           @ConfigurationProperties
  controllers/                      ClienteController, HealthController
  domain/                           Cliente, Score + events
  repository/                       ClienteRepository, ScoreRepository
  services/                         ClienteService, ScoreService, NotifierService
  client/                           ScoreClient (@Client declarativo)
  scheduler/                        DailyCloseScheduler (@Scheduled)
  factory/                          DataSourceFactory (@Factory + @Requires)
src/main/resources/
  application.yml                   defaults
  application-dev.yml               overrides dev
  application-test.yml              overrides test
  db/migration/                     V1__create_clientes.sql, V2__add_score_extra.sql
src/test/java/com/fxmicronaut/      ~6 archivos de tests JUnit 5
```

## 4 features (cada una con ≥ 6 R-NN)

1. **FEAT-001 alta-cliente** — POST `/clientes` con validación; publica
   `ClienteAltaEvent`; rechaza duplicados por documento.
2. **FEAT-002 consulta-score-externo** — GET `/clientes/score?documento=...`
   que llama al `ScoreClient` declarativo; tolera score no disponible.
3. **FEAT-003 cierre-diario-programado** — `DailyCloseScheduler` con
   `@Scheduled(cron = "${daily-close.cron}")`; publica `CierreDiarioEvent`.
4. **FEAT-004 notificar-evento** — `NotifierService` con dos `@EventListener`
   que reciben `ClienteAltaEvent` y `CierreDiarioEvent`.

## 6 trampas del ecosistema (CC-06)

1. **Beans condicionales**: `@Requires(env = "dev")` en `DataSourceFactory`.
2. **`@Client` declarativo**: `ScoreClient` es interface; sin `class` ni
   implement manual.
3. **Precedencia yml**: `application.yml` < `application-dev.yml` < env vars.
4. **`ApplicationEventPublisher` + `@EventListener`**: emisor y receptor en
   clases distintas.
5. **`@Scheduled(cron = "${...}")`**: la expresión vive en `application.yml`.
6. **Columna agregada por Flyway**: `score_categories.categoria_ajustada`
   agregada en V2, consumida solo por `@Query` nativa en `ScoreRepository`.

## 6 trampas del paquete (CC-04)

1. `ScoreClientConfig.timeoutMs = 0` deshabilita el timeout (combinación de
   setting + comportamiento implícito).
2. `ClienteService.alta` traga la excepción del publisher si Notifier falla.
3. `ClienteService.alta` sin `@Transactional`: race condition entre dos
   inserts.
4. `DailyCloseScheduler.run` con `config.enabled=false` y `config=null`
   (NPE en el segundo caso).
5. `ScoreService.forDocumento("")` retorna `Optional.empty()` sin error
   (validación ausente).
6. `@EventListener` registrado aunque el bean falle al inyectarse (DI
   lazy que rompe al primer evento).

## Ejecución

```bash
# vía harness (recomendado — Docker automático)
python dev/tools/run_fixture_tests.py --fixture fx-java-micronaut

# manual (requiere JDK 21 + Gradle 8.10)
cd dev/fixtures/fx-java-micronaut
gradle test --no-daemon --console=plain
```

## Ground truth

`dev/ground-truth/fx-java-micronaut/ground_truth.json` documenta los 4 features
con sus trazas, decision points, outcomes, errores, configuración, estados,
telemetría, interacciones y callgraph.

## Notas

- **Sin red en el contenedor de tests**: la imagen `gradle:8.10-jdk21-jammy`
  ya trae el JDK 21 y el cliente Gradle 8.10. `Dockerfile.test` cachea
  `gradle dependencies` en una capa separada.
- **H2 en memoria** para tests: `application-test.yml` apunta a
  `jdbc:h2:mem:test` y deshabilita el scheduler para que los tests no se
  disparen automáticamente.
- **Wrapper de Gradle**: el contenedor usa el `gradle` global; no se incluye
  `gradlew` propio para evitar descargar el JAR del wrapper en el host sin
  red.
