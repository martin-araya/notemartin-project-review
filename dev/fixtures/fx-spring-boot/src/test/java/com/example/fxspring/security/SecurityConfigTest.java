// tests/security/SecurityConfigTest.java
// Tests runtime de Spring Security con @SpringBootTest.
// Verifica que las rutas publicas son accesibles y las privadas
// requieren autenticacion.
package com.example.fxspring.security;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.HttpStatus;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.web.client.RestClient;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class SecurityConfigTest {

    @LocalServerPort
    private int port;

    @Test
    void ruta_publica_es_accesible_sin_auth() {
        RestClient client = RestClient.create("http://localhost:" + port);
        // La ruta del health endpoint esta en permitAll().
        var response = client.get().uri("/actuator/health").retrieve().toEntity(String.class);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    void ruta_privada_devuelve_401_sin_auth() {
        RestClient client = RestClient.create("http://localhost:" + port);
        // La ruta bajo /api/v1/** esta en authenticated(); sin auth -> 401.
        try {
            client.get().uri("/api/v1/cuentas/1").retrieve().toEntity(String.class);
            fail("debio lanzar 401");
        } catch (org.springframework.web.client.HttpClientErrorException e) {
            assertEquals(HttpStatus.UNAUTHORIZED, e.getStatusCode());
        }
    }

    @Test
    void ruta_auditoria_devuelve_401_sin_auth() {
        // El SecurityFilterChain tiene hasRole(ADMIN) para
        // la ruta de logs. Sin auth -> 401.
        RestClient client = RestClient.create("http://localhost:" + port);
        try {
            client.get().uri("/api/v1/logs").retrieve().toEntity(String.class);
            fail("debio lanzar 401");
        } catch (org.springframework.web.client.HttpClientErrorException e) {
            assertEquals(HttpStatus.UNAUTHORIZED, e.getStatusCode());
        }
    }
}
