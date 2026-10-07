// plugins/StatusPages.kt
// Plugin de manejo de errores via StatusPages. Trampa paquete
// #2: el `when` en `status` no cubre todos los casos posibles
// del sealed class Result, por lo que errores custom quedan sin
// handler.
package com.example.fxktor.plugins

import io.ktor.http.HttpStatusCode
import io.ktor.server.application.Application
import io.ktor.server.application.install
import io.ktor.server.plugins.statuspages.StatusPages
import io.ktor.server.response.respond

fun Application.statusPages() {
    install(StatusPages) {
        exception<IllegalArgumentException> { call, cause ->
            call.respond(HttpStatusCode.BadRequest, mapOf("error" to (cause.message ?: "bad_request")))
        }
        exception<NoSuchElementException> { call, cause ->
            call.respond(HttpStatusCode.NotFound, mapOf("error" to (cause.message ?: "not_found")))
        }
    }
}
