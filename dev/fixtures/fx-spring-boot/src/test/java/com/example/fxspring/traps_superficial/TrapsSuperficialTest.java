// tests/traps_superficial/TrapsSuperficialTest.java
package com.example.fxspring.traps_superficial;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeAll;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.*;

class TrapsSuperficialTest {

    private static Path root;

    @BeforeAll
    static void setup() {
        root = Paths.get("src/main/java/com/example/fxspring");
    }

    private String read(String rel) throws IOException {
        return Files.readString(root.resolve(rel));
    }

    @Test
    void s01_cuenta_controller_listAll_exists_but_not_in_security() throws IOException {
        String ctrl = read("controller/CuentaController.java");
        // El metodo listAll() existe pero la ruta no esta en el matcher.
        assertTrue(ctrl.contains("public ResponseEntity<Page<Cuenta>> listAll"));
    }

    @Test
    void s02_auditoria_controller_no_preauthorize() throws IOException {
        String ctrl = read("controller/AuditoriaController.java");
        // El metodo listar() no tiene @PreAuthorize.
        // Buscamos en la firma del metodo (entre la declaracion y la apertura {).
        int idx = ctrl.indexOf("public List<Auditoria> listar");
        assertTrue(idx > 0);
        int braceIdx = ctrl.indexOf("{", idx);
        String signature = ctrl.substring(idx, braceIdx);
        assertFalse(signature.contains("@PreAuthorize"));
    }

    @Test
    void s03_async_config_no_properties() throws IOException {
        String cfg = read("config/AsyncConfig.java");
        // El @Bean Executor esta declarado pero application.yml
        // no define spring.task.execution.pool.core-size.
        assertTrue(cfg.contains("@Bean"));
        assertTrue(cfg.contains("Executor"));

        String yml = Files.readString(Paths.get("src/main/resources/application.yml"));
        // La property no aparece en application.yml.
        assertFalse(yml.contains("spring.task.execution.pool"));
    }
}
