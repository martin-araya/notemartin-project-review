// tests/traps_superficial/TrapsSuperficialTest.kt
package com.example.fxktor.traps_superficial

import org.junit.jupiter.api.Test
import org.junit.jupiter.api.BeforeAll
import java.io.IOException
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import kotlin.test.assertTrue
import kotlin.test.assertFalse

class TrapsSuperficialTest {
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
    fun s01_inventario_audit_dead_route() {
        val r = read("routes/InventarioRoutes.kt")
        // La ruta GET("/{id}/audit") existe pero su cuerpo
        // retorna lista vacia.
        assertTrue(r.contains("/{id}/audit"))
    }

    @Test
    fun s02_sendEmail_dead() {
        val s = read("service/AlertasService.kt")
        // sendEmail() esta declarado pero su cuerpo esta vacio.
        assertTrue(s.contains("sendEmail"))
    }

    @Test
    fun s03_dummy_logger_no_usado() {
        val d = read("di/AppModule.kt")
        assertTrue(d.contains("DummyLogger"))
        // Verificamos que no se usa en otra parte.
        val f = read("plugins/Monitoring.kt")
        assertFalse(f.contains("DummyLogger"))
    }
}
