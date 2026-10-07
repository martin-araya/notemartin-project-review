// domain/StockEvent.kt
// Sealed class con subtipos. Trampa ecosistema #5: si se anade
// un nuevo subtipo (e.g. `object ItemArchived`) sin actualizar
// el `when` exhaustivo en InventarioService.handle(), el codigo
// compila si el `when` se usa como statement, pero falla en
// runtime con `NoWhenBranchMatchedException` si se usa como
// expression.
package com.example.fxktor.domain

import kotlinx.serialization.Serializable

@Serializable
sealed class StockEvent {
    abstract val itemId: Int
    abstract val timestamp: Long

    @Serializable
    data class ItemCreated(
        override val itemId: Int,
        override val timestamp: Long = System.currentTimeMillis(),
        val item: Item
    ) : StockEvent()

    @Serializable
    data class ItemUpdated(
        override val itemId: Int,
        override val timestamp: Long = System.currentTimeMillis(),
        val cambios: Map<String, String>
    ) : StockEvent()

    @Serializable
    data class ItemDeleted(
        override val itemId: Int,
        override val timestamp: Long = System.currentTimeMillis()
    ) : StockEvent()
}
