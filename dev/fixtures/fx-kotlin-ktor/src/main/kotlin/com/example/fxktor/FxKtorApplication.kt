// FxKtorApplication.kt
// Punto de entrada del servicio Ktor.
// Trampa ecosistema #4: AlertasService hace `launch { ... }`
// en el `application` scope. El Job queda atado al GlobalScope
// por defecto, lo que rompe la cancelacion estructurada.
// Trampa paquete #1: el bloque `routing { ... }` NO tiene
// `install(Auth)` previo, asi que los endpoints quedan
// accesibles sin autenticacion.
package com.example.fxktor

import com.example.fxktor.di.appModule
import com.example.fxktor.plugins.monitoring
import com.example.fxktor.plugins.routes
import com.example.fxktor.plugins.statusPages
import io.ktor.serialization.kotlinx.json.json
import io.ktor.server.application.install
import io.ktor.server.engine.embeddedServer
import io.ktor.server.netty.Netty
import io.ktor.server.plugins.contentnegotiation.ContentNegotiation
import io.ktor.server.routing.routing
import org.koin.ktor.plugin.Koin
import org.koin.logger.slf4j.slf4jLogger

fun main() {
    embeddedServer(Netty, port = 8080, host = "0.0.0.0") {
        install(ContentNegotiation) { json() }
        install(Koin) {
            slf4jLogger()
            modules(appModule)
        }
        monitoring()
        statusPages()
        routing { routes() }
    }.start(wait = true)
}
