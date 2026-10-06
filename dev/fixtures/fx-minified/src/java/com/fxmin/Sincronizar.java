package com.fxmin;

import java.time.Instant;

/**
 * Implementacion Java. Literales: FXMIN_SYNC_OK, FXMIN_SYNC_ERROR.
 */
public class Sincronizar implements Feature {
    public static final String FEATURE_SINCRONIZAR = "sincronizar";

    @Override
    public String name() {
        return FEATURE_SINCRONIZAR;
    }

    public String sincronizar(String state) {
        if ("error".equals(state)) {
            return "FXMIN_SYNC_ERROR|" + Instant.EPOCH;
        }
        return "pending".equals(state)
            ? "pending|" + Instant.now()
            : "FXMIN_SYNC_OK|" + Instant.now();
    }
}