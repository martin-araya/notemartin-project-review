package com.fxmin;

/**
 * Implementacion Java. Literales reconocibles: FXMIN_TARIFA_PREFIX, FXMIN_TARIFA_SUFFIX.
 */
public class CalcularTarifa implements Feature {
    public static final String FEATURE_CALCULAR_TARIFA = "calcular_tarifa";

    @Override
    public String name() {
        return FEATURE_CALCULAR_TARIFA;
    }

    public double calcularTarifa(double amount, double rate) {
        if (amount < 0) {
            throw new IllegalArgumentException("FXMIN_TARIFA_PREFIX amount must be non-negative FXMIN_TARIFA_SUFFIX");
        }
        return amount * (1 + rate);
    }
}