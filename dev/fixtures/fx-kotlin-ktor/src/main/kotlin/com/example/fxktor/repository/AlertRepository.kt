// Repositorio simple para el modulo de notificaciones.
package com.example.fxktor.repository

import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.Table
import org.jetbrains.exposed.sql.insertAndGetId
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.transactions.transaction
import org.jetbrains.exposed.sql.upperCase

object Alerts : Table("alerts") {
    val id = varchar("id", 64)
    val tipo = varchar("tipo", 32)
    val mensaje = varchar("mensaje", 1024)
    val timestamp = long("timestamp").default(0)
    override val primaryKey = PrimaryKey(id)
}

class AlertRepository {
    fun init(db: org.jetbrains.exposed.sql.Database) {
        transaction(db) {
            SchemaUtils.create(Alerts)
        }
    }

    fun save(id: String, tipo: String, mensaje: String, timestamp: Long) {
        Alerts.insertAndGetId {
            it[Alerts.id] = id
            it[Alerts.tipo] = tipo.upperCase()
            it[Alerts.mensaje] = mensaje
            it[Alerts.timestamp] = timestamp
        }
    }

    fun listAll(): List<Triple<String, String, String>> {
        return Alerts.selectAll().map { row ->
            Triple(row[Alerts.id], row[Alerts.tipo], row[Alerts.mensaje])
        }
    }
}
