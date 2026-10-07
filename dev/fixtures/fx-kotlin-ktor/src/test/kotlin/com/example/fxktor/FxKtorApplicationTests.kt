// tests/FxKtorApplicationTests.kt
// Test de smoke que verifica que la app Ktor arranca.
package com.example.fxktor

import io.ktor.client.request.get
import io.ktor.client.statement.bodyAsText
import io.ktor.http.HttpStatusCode
import io.ktor.server.testing.testApplication
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertEquals

class FxKtorApplicationTests {
    @Test
    fun `app starts and root endpoint exists or 404`() = testApplication {
        val response = client.get("/")
        // No hay ruta "/" en el fixture; esperamos 404.
        assertEquals(HttpStatusCode.NotFound, response.status)
    }
}
