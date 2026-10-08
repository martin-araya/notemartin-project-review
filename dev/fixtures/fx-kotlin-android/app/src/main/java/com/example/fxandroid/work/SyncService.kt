package com.example.fxandroid.work

import android.app.Service
import android.content.Intent
import android.os.IBinder

/**
 * Service declarado en el AndroidManifest (trampa E1) pero no se invoca
 * desde código Kotlin. Existe solo para forzar a la skill a notar el
 * `<service>` en el manifest.
 */
class SyncService : Service() {
    override fun onBind(intent: Intent?): IBinder? = null
}