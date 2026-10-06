// tests/traps_package/TrapsPackageTest.java
package com.example.fxspring.traps_package;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeAll;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.*;

class TrapsPackageTest {

    private static Path root;

    @BeforeAll
    static void setup() {
        root = Paths.get("src/main/java/com/example/fxspring");
    }

    private String read(String rel) throws IOException {
        return Files.readString(root.resolve(rel));
    }

    @Test
    void p01_transactional_class_level() throws IOException {
        String svc = read("service/CuentaService.java");
        // @Transactional a nivel de clase: los metodos read-only
        // tambien la heredan.
        assertTrue(svc.contains("@Service\n@Transactional\npublic class"));
    }

    @Test
    void p02_cacheable_no_null_check() throws IOException {
        String svc = read("service/CuentaService.java");
        assertTrue(svc.contains("@Cacheable"));
        // Trampa: @Cacheable sin condicion `unless = "#result == null"`.
        assertFalse(svc.contains("unless"));
    }

    @Test
    void p03_async_no_enable_async() throws IOException {
        Path appPath = Paths.get("src/main/java/com/example/fxspring/FxSpringApplication.java");
        String app = Files.readString(appPath);
        // @EnableAsync NO esta declarado en la app (sin import ni anotacion).
        assertFalse(app.contains("@EnableAsync"));
        assertFalse(app.contains("import org.springframework.scheduling.annotation.EnableAsync"));

        String notif = read("service/NotificacionService.java");
        assertTrue(notif.contains("@Async"));
    }

    @Test
    void p04_preauthorize_incorrect_spel() throws IOException {
        String ctrl = read("controller/TransferenciaController.java");
        assertTrue(ctrl.contains("@PreAuthorize"));
        // La SpEL compara id de path con authentication.principal.id
        // (que seria el userId), no el id de la transferencia.
        assertTrue(ctrl.contains("#id == authentication.principal.id"));
    }

    @Test
    void p05_version_silently_overwritten() throws IOException {
        String entity = read("domain/Transferencia.java");
        assertTrue(entity.contains("@Version"));
        // Trampa: el servicio no maneja OptimisticLockException.
        String svc = read("service/TransferenciaService.java");
        assertFalse(svc.contains("OptimisticLockException"));
    }

    @Test
    void p06_transactional_event_listener_silent_fail() throws IOException {
        String listener = read("listener/NotificacionListener.java");
        // El listener puede tirar RuntimeException sin manejo.
        assertTrue(listener.contains("@TransactionalEventListener"));
        // No hay try/catch que logee o reintente.
        assertFalse(listener.contains("catch ("));
    }
}
