package com.example.fxandroid.featurepremium

/**
 * Trampa E4: el feature premium solo existe en el source set `paid`.
 * En el flavor `free`, este paquete no se compila y `PremiumEnabled`
 * no esta disponible. Si el codigo `paid` se intenta inyectar en `free`,
 * Hilt lanza `MissingBinding`.
 */
class PremiumEnabled {
    fun advancedExport(): String = "advanced export result"
}