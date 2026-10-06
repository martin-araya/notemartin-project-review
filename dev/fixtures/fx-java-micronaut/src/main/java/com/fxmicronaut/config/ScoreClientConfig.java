package com.fxmicronaut.config;

import io.micronaut.context.annotation.ConfigurationProperties;

/**
 * Configuracion del cliente HTTP declarativo que consulta el score externo.
 * Vive en application.yml bajo la clave ``score.client``.
 *
 * Trampa de paquete #1: si ``timeoutMs`` es 0 o negativo, se considera
 * "sin timeout" (la llamada puede colgar). El caller debe validar que
 * ``timeoutMs > 0`` antes de invocar el cliente.
 */
@ConfigurationProperties("score.client")
public record ScoreClientConfig(String baseUrl, int timeoutMs) {
    public ScoreClientConfig {
        if (baseUrl == null || baseUrl.isBlank()) {
            baseUrl = "https://score.example.com";
        }
        // Trampa de paquete #1: timeoutMs <= 0 -> "sin timeout" (combinacion
        // de setting + comportamiento).
        if (timeoutMs <= 0) {
            timeoutMs = 0;
        }
    }
}
