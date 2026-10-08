package com.example.fxandroid.ui.history

import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.hilt.navigation.compose.hiltViewModel

@Composable
fun HistoryScreen(
    viewModel: HistoryViewModel = hiltViewModel(),
    initialFilter: String? = null
) {
    val entries by viewModel.entries.collectAsState()
    val error by viewModel.error.collectAsState()

    LaunchedEffect(initialFilter) {
        if (initialFilter != null) viewModel.search(initialFilter)
        else viewModel.load()
    }

    if (error != null) {
        Text(text = error ?: "")
    } else if (entries.isEmpty()) {
        Text(text = "Aún no hay escaneos")
    } else {
        LazyColumn {
            items(entries) { entry ->
                Text(text = "${entry.actor} → ${entry.action} @ ${entry.targetId}")
            }
        }
    }
}