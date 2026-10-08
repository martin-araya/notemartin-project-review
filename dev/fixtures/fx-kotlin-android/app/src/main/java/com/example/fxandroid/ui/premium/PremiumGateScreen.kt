package com.example.fxandroid.ui.premium

import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import com.example.fxandroid.BuildConfig

sealed class PremiumState {
    data object Enabled : PremiumState()
    data object Disabled : PremiumState()
}

fun resolvePremiumState(): PremiumState {
    return if (BuildConfig.PREMIUM_ENABLED) PremiumState.Enabled else PremiumState.Disabled
}

@Composable
fun PremiumGateScreen() {
    val state = resolvePremiumState()
    Column {
        when (state) {
            PremiumState.Enabled -> {
                Text("Funciones premium habilitadas")
                Button(onClick = {}) { Text("Usar exportador avanzado") }
            }
            PremiumState.Disabled -> {
                Text("Premium no disponible en este flavor")
                Button(onClick = {}) { Text("Comprar Pro") }
            }
        }
    }
}