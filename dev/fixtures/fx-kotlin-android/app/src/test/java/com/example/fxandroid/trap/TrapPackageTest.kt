package com.example.fxandroid.trap

import com.example.fxandroid.data.local.dao.HistoryDao
import com.example.fxandroid.data.local.entity.HistoryEntity
import com.example.fxandroid.data.repository.HistoryRepositoryImpl
import kotlinx.coroutines.flow.Flow
import org.junit.jupiter.api.Assertions.assertFalse
import kotlinx.coroutines.flow.flowOf
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class TrapPackageTest {

    private class NoopHistoryDao : HistoryDao {
        override fun page(limit: Int, offset: Int): Flow<List<HistoryEntity>> = flowOf(emptyList())
        override suspend fun findByActor(actor: String): List<HistoryEntity> = emptyList()
        override suspend fun upsert(entry: HistoryEntity) {}
        override suspend fun deleteById(id: Long) {}
        override suspend fun count(): Int = 0
    }

    @Test
    fun `P1 Room DAO uses Query parameters not concatenation`() {
        val daoFile = java.io.File("src/main/java/com/example/fxandroid/data/local/dao/HistoryDao.kt")
        assertTrue(daoFile.exists())
        assertTrue(daoFile.readText().contains("@Query"))
    }

    @Test
    fun `P2 ProductRepositoryImpl is not Singleton`() {
        val moduleFile = java.io.File("src/main/java/com/example/fxandroid/di/AppModule.kt")
        assertTrue(moduleFile.exists())
        val content = moduleFile.readText()
        assertTrue(content.contains("ProductRepositoryImpl"))
        // provideProductRepository is not annotated @Singleton
        val prodProvidesSection = content.substringAfter("provideProductRepository").take(200)
        assertFalse(prodProvidesSection.contains("@Singleton"))
    }

    @Test
    fun `P3 SyncScheduler uses expedited without notification check`() {
        val schedulerFile = java.io.File("src/main/java/com/example/fxandroid/work/SyncScheduler.kt")
        assertTrue(schedulerFile.exists())
        assertTrue(schedulerFile.readText().contains("setExpedited"))
        assertTrue(!schedulerFile.readText().contains("POST_NOTIFICATIONS"))
    }

    @Test
    fun `P4 DatabaseModule lacks addMigrations`() {
        val dbFile = java.io.File("src/main/java/com/example/fxandroid/di/DatabaseModule.kt")
        assertTrue(dbFile.exists())
        val content = dbFile.readText()
        assertTrue(content.contains("Room.databaseBuilder"))
        assertTrue(!content.contains("addMigrations("))
    }

    @Test
    fun `P5 LegacyProductActivity bypasses repository`() {
        val appFile = java.io.File("src/main/java/com/example/fxandroid/ui/legacy/LegacyProductActivity.kt")
        assertTrue(appFile.exists())
        assertTrue(appFile.readText().contains("execSQL"))
    }

    @Test
    fun `P6 ScanViewModel has silent try-catch`() {
        val vmFile = java.io.File("src/main/java/com/example/fxandroid/ui/scan/ScanViewModel.kt")
        assertTrue(vmFile.exists())
        val content = vmFile.readText()
        assertTrue(content.contains("catch (e: Exception)"))
    }
}