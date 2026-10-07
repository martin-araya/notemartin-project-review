// Extension function sobre Route que define los endpoints del
// modulo de notificaciones. El POST emite un evento via
// AlertasService.emitir(). La trampa paquete #7: el Alert
// se serializa como JSON polimorfico; el discriminador (nombre
// del subtipo) debe estar en el JSON para deserializar
// correctamente.
package com.example.fxktor.routes

import com.example.fxktor.domain.Alert
import com.example.fxktor.service.AlertasService
import io.ktor.http.HttpStatusCode
import io.ktor.server.application.call
import io.ktor.server.request.receive
import io.ktor.server.response.respond
import io.ktor.server.routing.Route
import io.ktor.server.routing.get
import io.ktor.server.routing.post
import io.ktor.server.routing.route
import org.koin.ktor.ext.inject

fun Route.alertas() {
    val service by inject<AlertasService>()

    route("/alerts") {
        get {
            call.respond(service.listar())
        }
        post {
            val alert = call.receive<Alert>()
            if (alert.mensaje.isBlank()) {
                call.respond(HttpStatusCode.UnprocessableEntity, mapOf("error" to "mensaje_required"))
                return@post
            }
            service.emitir(alert)
            call.respond(HttpStatusCode.Created, alert)
        }
    }
}
