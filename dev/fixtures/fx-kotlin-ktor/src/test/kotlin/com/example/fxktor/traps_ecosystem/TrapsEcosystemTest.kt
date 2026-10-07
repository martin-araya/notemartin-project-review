// tests/traps_ecosystem/TrapsEcosystemTest.kt
// Tests estaticos via grep (no requieren Ktor runtime).
package com.example.fxktor.traps_ecosystem

import org.junit.jupiter.api.Test
import org.junit.jupiter.api.BeforeAll
import java.io.IOException
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import kotlin.test.assertTrue

class TrapsEcosystemTest {
    companion object {
        private lateinit var root: Path

        @JvmStatic
        @BeforeAll
        fun setup() {
            root = Paths.get("src/main/kotlin/com/example/fxktor").toAbsolutePath()
        }

        private fun read(rel: String): String {
            return Files.readString(root.resolve(rel))
        }
    }

    @Test
    fun e01_dsl_nested() {
        val r = read("plugins/Routing.kt")
        assertTrue(r.contains("Route.routes()"))
        assertTrue(r.contains("inventario()"))
        assertTrue(r.contains("reservas()"))
        assertTrue(r.contains("alertas()"))
    }

    @Test
    fun e02_plugins_installed() {
        val auth = read("plugins/Auth.kt")
        assertTrue(auth.contains("install(Authentication)"))
        val sp = read("plugins/StatusPages.kt")
        assertTrue(sp.contains("install(StatusPages)"))
    }

    @Test
    fun e03_extension_functions() {
        val r = read("routes/InventarioRoutes.kt")
        assertTrue(r.contains("fun Route.inventario()"))
        val r2 = read("routes/ReservasRoutes.kt")
        assertTrue(r2.contains("fun Route.reservas()"))
    }

    @Test
    fun e04_coroutines_flow() {
        val s = read("service/InventarioService.kt")
        assertTrue(s.contains("flow {"))
        assertTrue(s.contains("emit(it)"))
    }

    @Test
    fun e05_sealed_class_when() {
        val s = read("service/InventarioService.kt")
        assertTrue(s.contains("sealed class") || s.contains("StockEvent"))
        assertTrue(s.contains("is StockEvent.ItemCreated"))
    }

    @Test
    fun e06_delegated_property() {
        val s = read("service/InventarioService.kt")
        assertTrue(s.contains("by inject()"))
        val m = read("di/AppModule.kt")
        assertTrue(m.contains("KoinComponent"))
    }
}
