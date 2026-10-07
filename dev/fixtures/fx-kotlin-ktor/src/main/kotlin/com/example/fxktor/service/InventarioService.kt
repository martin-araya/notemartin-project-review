// service/InventarioService.kt
// Service con corutinas y Flow. Trampa ecosistema #6: `repo` se
// declara con `by inject()` (KoinComponent), que se evalua en
// cada acceso. En corrutinas con Dispatchers.Default, el
// KoinContext puede no estar disponible, lanzando
// `KoinScopeComponent.getKoin()`.
// Trampa paquete #4: el Flow `observedItems` no llama a
// `.buffer()`, lo que significa que un consumidor lento bloquea
// al emisor.
package com.example.fxktor.service

import com.example.fxktor.domain.Item
import com.example.fxktor.domain.StockEvent
import com.example.fxktor.repository.ItemRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import org.koin.core.component.KoinComponent
import org.koin.core.component.inject

class InventarioService(private val baseRepo: ItemRepository) : KoinComponent {

    // Trampa ecosistema #6: `by inject()` requiere GlobalContext
    // activo. En una corutina con Dispatchers.Default, esto falla.
    private val repo: ItemRepository by inject()

    suspend fun listar(): List<Item> = repo.listAll()

    suspend fun obtener(id: Int): Item? = repo.findById(id)

    suspend fun crear(item: Item): Item = repo.create(item)

    suspend fun actualizar(id: Int, cambios: Map<String, Any?>): Boolean = repo.update(id, cambios)

    suspend fun eliminar(id: Int): Boolean {
        val actual = repo.findById(id) ?: return false
        // Trampa paquete #4: el Flow emite sin buffer.
        return actual.cantidad > 0
    }

    // observedItems() retorna un Flow sin operaciones de
    // backpressure. Un consumidor lento bloquea al productor.
    fun observedItems(): Flow<Item> = flow {
        repo.listAll().forEach { emit(it) }
    }

    // Maquina de estados: sealed class + when exhaustivo. La trampa
    // es que si se anade un nuevo subtipo (sin actualizar el
    // when), el codigo compila como statement pero falla en
    // runtime con NoWhenBranchMatchedException.
    fun handle(event: StockEvent): String {
        return when (event) {
            is StockEvent.ItemCreated -> "created:${event.itemId}"
            is StockEvent.ItemUpdated -> "updated:${event.itemId}"
            is StockEvent.ItemDeleted -> "deleted:${event.itemId}"
        }
    }
}
