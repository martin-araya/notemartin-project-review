package com.example.fxandroid.featurepremium

/**
 * Trampa E4: el flavor `free` solo tiene `PremiumDisabled`.
 * `PremiumEnabled` no se compila y causa `MissingBinding` si se inyecta.
 */
class PremiumDisabled {
    fun cta(): String = "Comprar Pro"
}