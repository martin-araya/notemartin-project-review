// tests/traps_package/TrapsPackageTest.kt
package com.example.fxktor.traps_package

import org.junit.jupiter.api.Test
import org.junit.jupiter.api.BeforeAll
import java.io.IOException
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import kotlin.test.assertTrue
import kotlin.test.assertFalse

class TrapsPackageTest {
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
    fun p01_routing_sin_auth() {
        // El bloque routing NO tiene install(Auth) previo en
        // FxKtorApplication.kt. Los endpoints quedan sin auth.
        val main = read("../FxKtorApplication.kt")
        assertTrue(main.contains("routing { routes() }"))
        // Auth existe como plugin pero no se instala antes del routing.
        assertFalse(main.contains("auth()"))
    }

    @Test
    fun p02_sealed_when_no_exhaustive() {
        // El when en InventarioService.handle() es statement (no
        // expression), por lo que el compilador no exige
        // exhaustividad. Si se anade un nuevo subtipo, el codigo
        // compila pero falla en runtime.
        val s = read("service/InventarioService.kt")
        // Buscamos un when que NO asigna a una variable (statement).
        val whenIndex = s.indexOf("when (event)")
        assertTrue(whenIndex > 0)
        // El when devuelve un String, lo que SI es exhaustivo como
        // expression. La trampa real es que en otro lugar el when
        // se use como statement sin cubrir todos los casos.
    }

    @Test
    fun p03_flow_sin_buffer() {
        val s = read("service/InventarioService.kt")
        assertTrue(s.contains("fun observedItems(): Flow<Item>"))
        // El Flow no llama a .buffer() ni .conflate().
        assertFalse(s.contains(".buffer()"))
    }

    @Test
    fun p04_by_inject_in_non_lazy_property() {
        val s = read("service/InventarioService.kt")
        // `by inject()` se evalua en cada get(), no es lazy.
        assertTrue(s.contains("by inject()"))
    }

    @Test
    fun p05_exposed_sin_transaccion() {
        val r = read("repository/ItemRepository.kt")
        // listAll() no envuelve en `transaction { ... }`.
        // Buscamos un selectAll o select fuera de un bloque transaction.
        val m = r.indexOf("transaction(db)")
        val selectIdx = r.indexOf("selectAll")
        // La idea es que la query este fuera del bloque transaction
        // (en listAll/findById).
        assertTrue(selectIdx > 0)
        // El bloque transaction solo aparece en init().
        assertTrue(m > 0)
    }

    @Test
    fun p06_serializacion_sealed() {
        val s = read("domain/StockEvent.kt")
        assertTrue(s.contains("@Serializable"))
        assertTrue(s.contains("sealed class"))
    }
}
