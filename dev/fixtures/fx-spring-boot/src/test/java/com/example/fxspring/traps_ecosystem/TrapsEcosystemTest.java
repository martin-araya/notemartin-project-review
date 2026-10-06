// tests/traps_ecosystem/TrapsEcosystemTest.java
// Tests estaticos via grep (no requieren Spring runtime).
package com.example.fxspring.traps_ecosystem;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeAll;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.*;

class TrapsEcosystemTest {

    private static Path root;

    @BeforeAll
    static void setup() {
        root = Paths.get("src/main/java/com/example/fxspring");
    }

    private String read(String rel) throws IOException {
        return Files.readString(root.resolve(rel));
    }

    @Test
    void e01_auto_config_conditional() throws IOException {
        String db = read("config/DatabaseConfig.java");
        assertTrue(db.contains("@ConditionalOnProperty"));
        assertTrue(db.contains("havingValue = \"postgres\""));
    }

    @Test
    void e02_aop_proxy_autoinvocation() throws IOException {
        String svc = read("service/TransferenciaService.java");
        assertTrue(svc.contains("this.validarSaldo"));
        assertTrue(svc.contains("@Transactional"));
        // La trampa: la llamada this.X no se intercepta por AOP.
        assertFalse(svc.contains("self.validarSaldo")); // no usa self-injection
    }

    @Test
    void e03_derived_queries_no_implementation() throws IOException {
        String repo = read("repository/CuentaRepository.java");
        assertTrue(repo.contains("findByEmail"));
        // El metodo es una derived query: Spring Data JPA lo
        // implementa. No hay body de metodo (no hay { entre la
        // firma y el ;), solo declaraciones de interface.
        assertFalse(repo.contains("return "));
        assertFalse(repo.contains("throw "));
        // Verificamos que el metodo es solo declaracion (termina en ;).
        assertTrue(repo.contains("findByEmail(String email);"));
    }

    @Test
    void e04_security_filter_chain_single_bean() throws IOException {
        String cfg = read("config/SecurityConfig.java");
        assertTrue(cfg.contains("SecurityFilterChain"));
        // Trampa: una sola cadena define todas las rutas.
        // Si el controller agrega una ruta sin actualizar el
        // matcher, queda accesible.
        assertTrue(cfg.contains("requestMatchers(\"/api/v1/**\")"));
    }

    @Test
    void e05_transactional_event_listener_after_commit() throws IOException {
        String listener = read("listener/NotificacionListener.java");
        assertTrue(listener.contains("@TransactionalEventListener"));
        assertTrue(listener.contains("AFTER_COMMIT"));
    }

    @Test
    void e06_lombok_generates_getters() throws IOException {
        String cuenta = read("domain/Cuenta.java");
        // Lombok @Data genera getters/setters, equals, hashCode, toString.
        // El codigo fuente NO contiene esos metodos.
        assertTrue(cuenta.contains("import lombok.Data"));
        assertTrue(cuenta.contains("@Data"));
        assertFalse(cuenta.contains("public Long getId()"));
        assertFalse(cuenta.contains("public void setId("));
    }
}
