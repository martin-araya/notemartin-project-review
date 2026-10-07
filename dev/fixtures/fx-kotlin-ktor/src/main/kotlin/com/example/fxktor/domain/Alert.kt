// Sealed class para el modulo de notificaciones. Se serializa
// como JSON polimorfico con discriminador por defecto
// (nombre del subtipo).
package com.example.fxktor.domain

import kotlinx.serialization.Serializable

@Serializable
sealed class Alert {
    abstract val id: String
    abstract val timestamp: Long

    @Serializable
    data class Info(
        override val id: String,
        override val timestamp: Long = System.currentTimeMillis(),
        val mensaje: String
    ) : Alert()

    @Serializable
    data class Warning(
        override val id: String,
        override val timestamp: Long = System.currentTimeMillis(),
        val mensaje: String
    ) : Alert()

    @Serializable
    data class Critical(
        override val id: String,
        override val timestamp: Long = System.currentTimeMillis(),
        val mensaje: String
    ) : Alert()
}
