# Fixture F06m — fx-spring-boot

API REST **Spring Boot 3** empresarial con persistencia **JPA**,
**Spring Security**, eventos transaccionales y procesos
asíncronos, **Lombok** para reducir boilerplate, **Flyway** para
migraciones, **Testcontainers** para tests con PostgreSQL real.
Plantada para que la skill tenga que rastrear las trampas
clasicas del ecosistema Spring:

## Stack

- **Backend:** Java 21, Spring Boot 3.3.
- **Persistencia:** Spring Data JPA + Hibernate.
- **Seguridad:** Spring Security con SecurityFilterChain.
- **Validacion:** Jakarta Validation (jakarta.validation).
- **Observabilidad:** Spring Actuator.
- **Build:** Maven 3.9.
- **Tests:** JUnit 5 + `spring-boot-starter-test` + Testcontainers
  (PostgreSQL 16).

## Como se ejecutan los tests

```bash
make test           # mvn -B -q test
make build          # mvn package -DskipTests
make history        # regenera la historia git (8 commits)
```

En contenedor (con Docker daemon para Testcontainers):

```bash
python dev/tools/run_fixture_tests.py --fixture fx-spring-boot --container
```

## Estructura

- `pom.xml`: Spring Boot 3.3.5 parent, Java 21, starters web/data-jpa/
  security/validation/actuator, Lombok, Flyway, PostgreSQL,
  Testcontainers, JUnit 5.
- `src/main/java/com/example/fxspring/`:
  - `FxSpringApplication.java`: `@SpringBootApplication`.
  - `config/{SecurityConfig, DatabaseConfig, AsyncConfig}.java`.
  - `domain/{Cuenta, Transferencia, Auditoria, Notificacion}.java`:
    entidades JPA con Lombok `@Data`.
  - `repository/{Cuenta, Transferencia, Notificacion}Repository.java`:
    `JpaRepository` con derived queries y `@Lock`.
  - `service/{Cuenta, Transferencia, Auditoria, Notificacion}Service.java`:
    `@Service` con `@Transactional` y `@Async`.
  - `controller/{Cuenta, Transferencia, Auditoria}Controller.java`:
    `@RestController` con `@PreAuthorize`.
  - `event/TransferenciaRealizadaEvent.java`.
  - `listener/NotificacionListener.java`:
    `@TransactionalEventListener(AFTER_COMMIT)`.
- `src/main/resources/`:
  - `application.yml` con perfiles `dev` y `prod`.
  - `db/migration/V1__init.sql` (Flyway).
  - `logback-spring.xml`.
- `src/test/java/com/example/fxspring/`: 11 archivos JUnit 5 con
  Testcontainers para los tests de repository y security.

## Features

1. **cuentas** (FEAT-001): crear, obtener, listar paginado,
   validacion. 7 R-NN.
2. **transferencias** (FEAT-002): crear, confirmar, optimistic
   lock, auto-invocation bug. 7 R-NN.
3. **auditoria** (FEAT-003): listar con role ADMIN, evento
   transaccional. 7 R-NN.
4. **notificaciones-asíncronas** (FEAT-004): dispatch via
   `@TransactionalEventListener(AFTER_COMMIT)`, sin retry. 7
   R-NN.

## Trampas plantadas

- 6 del ecosistema (CC-06): auto-config + @ConditionalOnProperty,
  proxies AOP con auto-invocation bug, derived queries sin
  implementacion, SecurityFilterChain unico,
  @TransactionalEventListener(AFTER_COMMIT), Lombok genera
  getters/builders/constructores.
- 6 del paquete (CC-04): @Transactional a nivel de clase,
  @Cacheable sin null, @Async sin @EnableAsync, @PreAuthorize
  con SpEL incorrecta, @Version mal sincronizado,
  @TransactionalEventListener con excepcion no manejada.
- 3 superficiales (CC-05): CuentaController.listAll dead,
  AuditoriaController sin @PreAuthorize, AsyncConfig sin
  properties.