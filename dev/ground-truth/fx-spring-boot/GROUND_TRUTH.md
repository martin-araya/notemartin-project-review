# Ground truth de fx-spring-boot (F06m)

API REST **Spring Boot 3** empresarial con persistencia JPA,
Spring Security, eventos transaccionales y procesos asíncronos.
Plantada para que la skill tenga que rastrear las trampas
clasicas del ecosistema Spring:

## Features

1. **cuentas** (FEAT-001): crear, obtener, listar paginado,
   validacion. 7 R-NN.
2. **transferencias** (FEAT-002): crear, confirmar (cambia estado
   y dispara evento), listar. 7 R-NN.
3. **auditoria** (FEAT-003): listar con role ADMIN, registro
   automatico via listener. 7 R-NN.
4. **notificaciones-asíncronas** (FEAT-004): dispatch via
   `@TransactionalEventListener(AFTER_COMMIT)`, sin retry. 7
   R-NN.

## Trampas del ecosistema (CC-06)

1. **auto_config_conditional** (`DatabaseConfig`): el bean
   `@ConditionalOnProperty(..., havingValue = "postgres")` solo
   se activa en prod; en dev no se crea y la app usa H2.
2. **aop_proxy_autoinvocation** (`TransferenciaService`):
   `this.validarSaldo()` con `@Transactional(REQUIRES_NEW)` se
   ejecuta en la misma transaccion porque Spring AOP no
   intercepta llamadas `this.X`.
3. **derived_queries_no_impl** (`CuentaRepository`): los metodos
   `findByEmail`, `findByEmailAndEstado`, `findByEstado` no
   tienen body; Spring Data JPA los implementa en runtime.
4. **security_filter_chain_single** (`SecurityConfig`): un
   unico bean `SecurityFilterChain` define TODAS las rutas.
5. **transactional_event_listener** (`NotificacionListener`):
   `@TransactionalEventListener(phase = AFTER_COMMIT)` solo
   corre si el padre hace commit; rollback = no listener.
6. **lombok_generated**: `@Data` genera getters, setters,
   `equals`, `hashCode`, `toString` y un constructor; no
   aparecen en el codigo fuente.

## Trampas del paquete (CC-04)

1. **transactional_class_level** (`CuentaService`):
   `@Transactional` a nivel de clase; metodos read-only
   heredan la transaccion.
2. **cacheable_no_null_check** (`CuentaService.findByEmailCached`):
   `@Cacheable` sin condicion `unless`; cachea null en
   cache miss.
3. **async_no_enable_async** (`NotificacionService.enviar`):
   `@Async` declarado pero la app no tiene `@EnableAsync`;
   el metodo ejecuta sincronamente.
4. **preauthorize_incorrect_spel**
   (`TransferenciaController.cancelar`): SpEL
   `#id == authentication.principal.id` no valida ownership.
5. **version_silent_overwrite** (`Transferencia.@Version`):
   optimistic lock presente pero
   `OptimisticLockException` no se maneja.
6. **transactional_event_listener_silent_fail**
   (`NotificacionListener`): excepciones del listener se
   ignoran silenciosamente.

## Trampas superficiales (CC-05)

1. **dead_route** (`CuentaController.listAll`): ruta declarada
   pero no en el matcher de SecurityFilterChain.
2. **controller_no_preauthorize** (`AuditoriaController.listar`):
   sin `@PreAuthorize` a nivel de metodo.
3. **async_config_no_properties** (`AsyncConfig` + `application.yml`):
   el `@Bean Executor` se declara pero
   `spring.task.execution.pool.core-size` no esta en yml.

## Archivos clave del fixture

- `pom.xml`: Spring Boot 3.3.5 parent, Java 17, starters
  web/data-jpa/security/validation/actuator, Lombok 1.18.38,
  Flyway, PostgreSQL, H2, Testcontainers, JUnit 5.
- `src/main/java/com/example/fxspring/`:
  - `FxSpringApplication.java`: `@SpringBootApplication` (sin
    `@EnableAsync`).
  - `config/`: SecurityConfig, DatabaseConfig, AsyncConfig.
  - `domain/`: Cuenta, Transferencia, Auditoria, Notificacion
    (todas con `@Data` de Lombok).
  - `repository/`: CuentaRepository (derived), TransferenciaRepository
    (con `@Lock`), NotificacionRepository, AuditoriaRepository.
  - `service/`: CuentaService (`@Transactional` clase), TransferenciaService
    (auto-invocation bug), AuditoriaService, NotificacionService
    (`@Async` sin `@EnableAsync`).
  - `controller/`: CuentaController, TransferenciaController
    (con `@PreAuthorize` incorrecto), AuditoriaController.
  - `event/TransferenciaRealizadaEvent.java`.
  - `listener/NotificacionListener.java` (`@TransactionalEventListener`).
- `src/main/resources/`: application.yml (H2 dev, Postgres prod),
  db/migration/V1__init.sql, logback-spring.xml.
- `src/test/java/com/example/fxspring/`: 11 archivos JUnit 5.
