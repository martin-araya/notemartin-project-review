package com.fxmin;

/**
 * Implementacion Java. Literal reconocible: FXMIN_LIC_INVALID.
 */
public class ValidarLicencia implements Feature {
    public static final String FEATURE_VALIDAR_LICENCIA = "validar_licencia";

    @Override
    public String name() {
        return FEATURE_VALIDAR_LICENCIA;
    }

    public String validarLicencia(String licenseKey) {
        if (licenseKey == null || licenseKey.length() < 8) {
            return "FXMIN_LIC_INVALID";
        }
        return "2099-12-31";
    }
}