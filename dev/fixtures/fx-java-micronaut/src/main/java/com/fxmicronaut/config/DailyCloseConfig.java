package com.fxmicronaut.config;

import io.micronaut.context.annotation.ConfigurationProperties;

/**
 * Configuracion del scheduler de cierre diario.
 * ``cron`` se lee de ``daily-close.cron`` y ``enabled`` de ``daily-close.enabled``.
 * Ambos pueden sobreescribirse por variables de entorno.
 */
@ConfigurationProperties("daily-close")
public record DailyCloseConfig(String cron, boolean enabled) {
    public DailyCloseConfig {
        if (cron == null || cron.isBlank()) {
            cron = "0 0 2 * * *";
        }
        // enabled es primitivo, no necesita default.
    }
}
