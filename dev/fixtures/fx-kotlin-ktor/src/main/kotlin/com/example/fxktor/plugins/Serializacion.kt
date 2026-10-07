// plugins/Serializacion.kt
// Plugin de serializacion JSON. La app ya llama install
// directamente en FxKtorApplication; este archivo queda como
// helper.
package com.example.fxktor.plugins

import io.ktor.serialization.kotlinx.json.json
import io.ktor.server.application.Application
import io.ktor.server.application.install
import io.ktor.server.plugins.contentnegotiation.ContentNegotiation
import kotlinx.serialization.json.Json

fun Application.json() {
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = true
        })
    }
}
