// plugins/Auth.kt
// Plugin de autenticacion basico via header Authorization.
// Trampa ecosistema #2: el orden de install(Auth) importa
// porque el AuthenticationProvider debe estar disponible antes
// de que las rutas lo usen.
package com.example.fxktor.plugins

import io.ktor.server.application.Application
import io.ktor.server.application.install
import io.ktor.server.auth.Authentication
import io.ktor.server.auth.UserIdPrincipal
import io.ktor.server.auth.basic

fun Application.auth() {
    install(Authentication) {
        basic("auth-basic") {
            realm = "fx-kotlin-ktor"
            validate { credentials ->
                if (credentials.name == "admin" && credentials.password == "admin") {
                    UserIdPrincipal(credentials.name)
                } else null
            }
        }
    }
}
