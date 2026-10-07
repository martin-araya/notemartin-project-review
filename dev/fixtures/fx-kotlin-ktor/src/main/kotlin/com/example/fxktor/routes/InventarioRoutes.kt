// Extension function sobre Route que define los endpoints del
// modulo principal. Trampa superficial #1: la ruta
// GET("/{id}/audit") esta declarada pero nunca se invoca
// (dead route).
package com.example.fxktor.routes

import com.example.fxktor.domain.Item
import com.example.fxktor.domain.StockEvent
import com.example.fxktor.service.InventarioService
import io.ktor.http.HttpStatusCode
import io.ktor.server.application.call
import io.ktor.server.response.respond
import io.ktor.server.routing.Route
import io.ktor.server.routing.delete
import io.ktor.server.routing.get
import io.ktor.server.routing.patch
import io.ktor.server.routing.post
import io.ktor.server.routing.route
import org.koin.ktor.ext.inject

fun Route.inventario() {
    val service by inject<InventarioService>()

    route("/inv") {
        get {
            call.respond(service.listar())
        }
        get("/{id}") {
            val id = call.parameters["id"]?.toIntOrNull() ?: return@get call.respond(HttpStatusCode.BadRequest)
            val item = service.obtener(id) ?: return@get call.respond(HttpStatusCode.NotFound)
            call.respond(item)
        }
        post {
            val body = call.receive<Item>()
            val saved = service.crear(body)
            call.respond(HttpStatusCode.Created, saved)
        }
        patch("/{id}") {
            val id = call.parameters["id"]?.toIntOrNull() ?: return@patch call.respond(HttpStatusCode.BadRequest)
            val cambios = call.receive<Map<String, String>>()
            val ok = service.actualizar(id, cambios)
            if (ok) call.respond(HttpStatusCode.OK) else call.respond(HttpStatusCode.NotFound)
        }
        delete("/{id}") {
            val id = call.parameters["id"]?.toIntOrNull() ?: return@delete call.respond(HttpStatusCode.BadRequest)
            val ok = service.eliminar(id)
            if (ok) call.respond(HttpStatusCode.NoContent) else call.respond(HttpStatusCode.NotFound)
        }
        // Trampa superficial #1: dead route.
        get("/{id}/audit") {
            call.respond(mapOf("audits" to emptyList<String>()))
        }
    }
}
