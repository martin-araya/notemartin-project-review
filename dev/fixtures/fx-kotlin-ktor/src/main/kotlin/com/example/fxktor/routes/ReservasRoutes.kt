// Extension function sobre Route que define los endpoints del
// modulo de stock. La trampa paquete #5 (Exposed sin
// transaccion) se manifiesta aqui: las queries del
// repository fallan en runtime.
package com.example.fxktor.routes

import com.example.fxktor.service.InventarioService
import io.ktor.http.HttpStatusCode
import io.ktor.server.application.call
import io.ktor.server.request.receive
import io.ktor.server.response.respond
import io.ktor.server.routing.Route
import io.ktor.server.routing.delete
import io.ktor.server.routing.get
import io.ktor.server.routing.post
import io.ktor.server.routing.route
import org.koin.ktor.ext.inject

fun Route.reservas() {
    val service by inject<InventarioService>()

    route("/reservas") {
        get {
            // En un fixture real, esto leeria de una tabla
            // dedicada. Aqui retornamos la lista completa del
            // servicio principal.
            call.respond(service.listar())
        }
        post {
            val body = call.receive<Map<String, Int>>()
            val itemId = body["itemId"] ?: return@post call.respond(HttpStatusCode.BadRequest)
            // Trampa: el POST no hace nada, solo responde 201
            // con el item original. La reserva no se persiste.
            val item = service.obtener(itemId) ?: return@post call.respond(HttpStatusCode.NotFound)
            call.respond(HttpStatusCode.Created, item)
        }
        delete("/{id}") {
            val id = call.parameters["id"]?.toIntOrNull() ?: return@delete call.respond(HttpStatusCode.BadRequest)
            val ok = service.eliminar(id)
            if (ok) call.respond(HttpStatusCode.NoContent) else call.respond(HttpStatusCode.NotFound)
        }
    }
}
