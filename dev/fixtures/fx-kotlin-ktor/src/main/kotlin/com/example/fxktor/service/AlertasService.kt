// service/AlertasService.kt
// Service que lanza corrutinas en el application scope. Trampa
// ecosistema #4: `launch { ... }` sin pasar un CoroutineScope
// explicito usa GlobalScope por defecto, lo que rompe la
// cancelacion estructurada y causa memory leaks.
// Trampa paquete #7: sendEmail() es un metodo que no hace nada
// (dead code, no se invoca desde ninguna ruta).
package com.example.fxktor.service

import com.example.fxktor.domain.Alert
import com.example.fxktor.repository.AlertRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import org.koin.core.component.KoinComponent
import org.koin.core.component.inject

class AlertasService(private val baseRepo: AlertRepository) : KoinComponent {

    // Trampa ecosistema #4: la app scope no se cancela, lo que
    // rompe la cancelacion estructurada.
    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())

    private val repo: AlertRepository by inject()

    fun emitir(alert: Alert) {
        scope.launch {
            val tipo = when (alert) {
                is Alert.Info -> "info"
                is Alert.Warning -> "warning"
                is Alert.Critical -> "critical"
            }
            repo.save(alert.id, tipo, alert.mensaje, alert.timestamp)
            sendEmail(alert)
        }
    }

    fun listar(): List<Triple<String, String, String>> = repo.listAll()

    // Trampa paquete #7: dead code, sendEmail no se invoca.
    private fun sendEmail(alert: Alert) {
        // No envia email real; dead code documentado.
    }
}
