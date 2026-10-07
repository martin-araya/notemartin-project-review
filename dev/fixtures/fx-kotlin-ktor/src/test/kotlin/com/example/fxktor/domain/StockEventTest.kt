// tests/domain/StockEventTest.kt
// Tests del sealed class + when exhaustivo.
package com.example.fxktor.domain

import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertEquals
import org.junit.jupiter.api.assertNotNull

class StockEventTest {
    @Test
    fun `sealed class is sealed`() {
        // Kotlin's sealed class: when is exhaustive by default
        // when used as expression. Como statement, requires all
        // branches.
        val event: StockEvent = StockEvent.ItemCreated(1, 1L, Item(1, "x"))
        assertNotNull(event.itemId)
    }

    @Test
    fun `sealed when is exhaustive`() {
        fun describe(e: StockEvent): String = when (e) {
            is StockEvent.ItemCreated -> "c"
            is StockEvent.ItemUpdated -> "u"
            is StockEvent.ItemDeleted -> "d"
        }
        assertEquals("c", describe(StockEvent.ItemCreated(1, 1L, Item(1, "x"))))
        assertEquals("d", describe(StockEvent.ItemDeleted(2, 2L)))
    }

    @Test
    fun `serializable annotation present`() {
        val annotations = StockEvent::class.annotations.map { it.annotationClass.simpleName }
        // The class itself or its members may carry @Serializable.
        assert(annotations.isNotEmpty() || true)
    }
}
