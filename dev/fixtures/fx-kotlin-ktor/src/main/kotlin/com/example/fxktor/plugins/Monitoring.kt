// plugins/Monitoring.kt
// Plugin de CallLogging y metricas. Trampa superficial #3: la
// app NO usa Koin para resolver la clase de log aunque esta
// declarada en AppModule.
package com.example.fxktor.plugins

import io.ktor.server.application.Application
import io.ktor.server.application.install
import io.ktor.server.plugins.callloging.CallLogging
import io.ktor.server.request.path
import org.slf4j.event.Level

fun Application.monitoring() {
    install(CallLogging) {
        level = Level.INFO
        filter { call -> call.request.path().startsWith("/api/") }
    }
}
