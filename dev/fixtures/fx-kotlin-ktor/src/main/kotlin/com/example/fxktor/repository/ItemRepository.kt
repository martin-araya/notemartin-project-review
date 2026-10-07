// repository/ItemRepository.kt
// Repositorio con Exposed. Trampa paquete #6: las queries
// no envuelven en `transaction { ... }` (DAO requiere transaccion
// activa). El codigo compila pero falla en runtime con
// `IllegalStateException: Connection is not established` o
// `newTransaction is required`.
package com.example.fxktor.repository

import com.example.fxktor.domain.Item
import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.Table
import org.jetbrains.exposed.sql.insertAndGetId
import org.jetbrains.exposed.sql.select
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.transactions.transaction
import org.jetbrains.exposed.sql.update

object Items : Table("items") {
    val id = integer("id").autoIncrement()
    val nombre = varchar("nombre", 255)
    val cantidad = integer("cantidad").default(0)
    val precio = double("precio").default(0.0)
    val premium = bool("premium").default(false)
    val estado = varchar("estado", 32).default("ACTIVO")
    override val primaryKey = PrimaryKey(id)
}

class ItemRepository {

    fun init(db: Database) {
        transaction(db) {
            SchemaUtils.create(Items)
        }
    }

    // Trampa paquete #6: no hay `newTransaction { ... }` envolviendo
    // el select. En runtime, Exposed exige una transaccion activa
    // y la query falla.
    fun listAll(): List<Item> {
        return Items.selectAll().map { row ->
            Item(
                id = row[Items.id].value,
                nombre = row[Items.nombre],
                cantidad = row[Items.cantidad],
                precio = row[Items.precio],
                premium = row[Items.premium],
                estado = row[Items.estado]
            )
        }
    }

    fun findById(id: Int): Item? {
        return Items.select { Items.id eq id }
            .map { row ->
                Item(
                    id = row[Items.id].value,
                    nombre = row[Items.nombre],
                    cantidad = row[Items.cantidad],
                    precio = row[Items.precio],
                    premium = row[Items.premium],
                    estado = row[Items.estado]
                )
            }
            .firstOrNull()
    }

    fun create(item: Item): Item {
        val newId = Items.insertAndGetId {
            it[nombre] = item.nombre
            it[cantidad] = item.cantidad
            it[precio] = item.precio
            it[premium] = item.premium
            it[estado] = item.estado
        }.value
        return item.copy(id = newId)
    }

    fun update(id: Int, cambios: Map<String, Any?>): Boolean {
        return Items.update({ Items.id eq id }) { row ->
            cambios.forEach { (k, v) ->
                when (k) {
                    "nombre" -> row[Items.nombre] = v as String
                    "cantidad" -> row[Items.cantidad] = v as Int
                    "precio" -> row[Items.precio] = v as Double
                    "premium" -> row[Items.premium] = v as Boolean
                    "estado" -> row[Items.estado] = v as String
                }
            }
        } > 0
    }
}
