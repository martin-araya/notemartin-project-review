package com.example.fxdart

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

/**
 * Stubs Kotlin de los handlers del MethodChannel nativo.
 * Este archivo documenta el contrato que la skill debe leer como
 * evidencia textual; NO compila sin un proyecto Android real (F06ad
 * usa platform channels solo via TestDefaultBinaryMessenger en tests).
 */
class MainActivity : FlutterActivity() {
    companion object {
        private const val CHANNEL = "com.example.fxdart/native"

        @JvmStatic
        fun scanDocument(engine: FlutterEngine): Map<String, String>? {
            // Stub: el handler real escanearia un codigo de barras via CameraX.
            return mapOf(
                "hash" to "fxd-${System.currentTimeMillis()}",
                "title" to "Documento Kotlin",
                "body" to "Contenido capturado desde Android nativo",
                "source" to "android-native"
            )
        }

        @JvmStatic
        fun capturePage(engine: FlutterEngine): String? {
            return "android-page-${System.currentTimeMillis()}"
        }
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "scanDocument" -> result.success(scanDocument(flutterEngine))
                    "capturePage" -> result.success(capturePage(flutterEngine))
                    else -> result.notImplemented()
                }
            }
    }
}