// tests/FxSpringApplicationTests.java
// Test de smoke que verifica que el context carga.
package com.example.fxspring;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("test")
class FxSpringApplicationTests {

    @Test
    void contextLoads() {
    }
}
