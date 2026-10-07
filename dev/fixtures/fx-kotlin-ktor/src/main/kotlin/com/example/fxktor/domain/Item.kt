// domain/Item.kt
// Entidad de dominio serializable. Trampa paquete #7: el field
// `metadata: Map<String, String>` se serializa como un mapa
// generico, lo que rompe la compatibilidad si los campos cambian
// de tipo. La trampa: kotlinx.serialization no valida el shape
// en runtime.
package com.example.fxktor.domain

import kotlinx.serialization.Serializable

@Serializable
data class Item(
    val id: Int = 0,
    val nombre: String,
    val cantidad: Int = 0,
    val precio: Double = 0.0,
    val premium: Boolean = false,
    val estado: String = "ACTIVO",
    val metadata: Map<String, String> = emptyMap()
)
