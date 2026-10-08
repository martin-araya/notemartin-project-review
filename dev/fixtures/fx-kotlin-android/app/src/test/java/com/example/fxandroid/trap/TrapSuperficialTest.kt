package com.example.fxandroid.trap

import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class TrapSuperficialTest {

    @Test
    fun `S1 LegacyDateFormatter is unused`() {
        val srcFiles = listOf(
            "src/main/java/com/example/fxandroid/ui/scan/ScanViewModel.kt",
            "src/main/java/com/example/fxandroid/ui/scan/ScanScreen.kt",
            "src/main/java/com/example/fxandroid/ui/history/HistoryViewModel.kt",
            "src/main/java/com/example/fxandroid/ui/history/HistoryScreen.kt",
            "src/main/java/com/example/fxandroid/ui/legacy/LegacyProductActivity.kt",
            "src/main/java/com/example/fxandroid/ui/legacy/LegacyProductFragment.kt",
            "src/main/java/com/example/fxandroid/ui/premium/PremiumGateScreen.kt",
            "src/main/java/com/example/fxandroid/work/SyncWorker.kt",
            "src/main/java/com/example/fxandroid/work/SyncScheduler.kt",
            "src/main/java/com/example/fxandroid/receiver/SyncTriggerReceiver.kt",
            "src/main/java/com/example/fxandroid/navigation/FxNavGraph.kt"
        )
        for (path in srcFiles) {
            val file = java.io.File(path)
            if (file.exists()) {
                assertFalse(
                    file.readText().contains("LegacyDateFormatter"),
                    "LegacyDateFormatter referenced in $path"
                )
            }
        }
    }

    @Test
    fun `S2 EnvConfig BuildConfig DEBUG unused`() {
        val envConfigFile = java.io.File("src/main/java/com/example/fxandroid/util/EnvConfig.kt")
        assertTrue(envConfigFile.exists())
        val content = envConfigFile.readText()
        assertTrue(content.contains("BuildConfig.DEBUG"))
        assertTrue(content.contains("debug") || content.contains("isDebug"))
    }

    @Test
    fun `S3 LegacyProductFragment onCreateView returns null`() {
        val fragFile = java.io.File("src/main/java/com/example/fxandroid/ui/legacy/LegacyProductFragment.kt")
        assertTrue(fragFile.exists())
        assertTrue(fragFile.readText().contains("return null"))
    }
}