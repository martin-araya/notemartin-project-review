package com.example.fxandroid.ui.scan

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel

@Composable
fun ScanScreen(
    viewModel: ScanViewModel = hiltViewModel(),
    prefilledEan: String? = null
) {
    val state by viewModel.state.collectAsState()
    var ean by remember { mutableStateOf(prefilledEan ?: "") }

    Column {
        Text(text = "Escanear producto")
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            value = ean,
            onValueChange = { ean = it },
            label = { Text("EAN 13 dígitos") }
        )
        Spacer(Modifier.height(8.dp))
        Button(onClick = { viewModel.onScanClick(ean) }) {
            Text("Escanear")
        }
        when (val s = state) {
            ScanState.Idle -> Text("Listo")
            ScanState.Scanning -> Text("Escaneando…")
            is ScanState.Success -> Text("Producto guardado: ${s.product.name}")
            is ScanState.Error -> Text("Error: ${s.message}")
        }
    }
}