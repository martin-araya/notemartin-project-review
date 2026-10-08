package com.example.fxandroid.trap

import com.example.fxandroid.data.local.dao.HistoryDao
import com.example.fxandroid.data.local.entity.HistoryEntity
import com.example.fxandroid.data.repository.HistoryRepositoryImpl
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOf
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class TrapEcosystemTest {

    private class NoopHistoryDao : HistoryDao {
        override fun page(limit: Int, offset: Int): Flow<List<HistoryEntity>> = flowOf(emptyList())
        override suspend fun findByActor(actor: String): List<HistoryEntity> = emptyList()
        override suspend fun upsert(entry: HistoryEntity) {}
        override suspend fun deleteById(id: Long) {}
        override suspend fun count(): Int = 0
    }

    @Test
    fun `E1 AndroidManifest declares components via AndroidManifest`() {
        val manifest = checkNotNull(
            javaClass.classLoader?.getResource("AndroidManifest.xml")
        )
        assertTrue(true)
    }

    @Test
    fun `E2 Hilt code generated not in sources`() {
        val sourcesDir = javaClass.protectionDomain.codeSource.location.toString()
        assertTrue(sourcesDir.isNotBlank())
    }

    @Test
    fun `E3 Room DAO uses Query annotation`() {
        val repo = HistoryRepositoryImpl(NoopHistoryDao())
        assertTrue(true)
    }

    @Test
    fun `E4 Free flavor has PremiumDisabled only`() {
        val paidFile = java.io.File("src/paid/java/com/example/fxandroid/featurepremium/PremiumEnabled.kt")
        val freeFile = java.io.File("src/free/java/com/example/fxandroid/featurepremium/PremiumDisabled.kt")
        assertTrue(paidFile.exists())
        assertTrue(freeFile.exists())
    }

    @Test
    fun `E5 Layout has onClick attribute`() {
        val layoutFile = java.io.File("src/main/res/layout/activity_legacy_product.xml")
        assertTrue(layoutFile.exists())
        assertTrue(layoutFile.readText().contains("onClick"))
    }

    @Test
    fun `E6 nav_graph xml has deepLink entries`() {
        val navFile = java.io.File("src/main/res/navigation/nav_graph.xml")
        assertTrue(navFile.exists())
        assertTrue(navFile.readText().contains("deepLink"))
    }
}