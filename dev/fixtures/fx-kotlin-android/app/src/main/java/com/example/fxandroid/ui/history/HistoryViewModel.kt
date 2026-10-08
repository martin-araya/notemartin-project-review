package com.example.fxandroid.ui.history

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.fxandroid.data.repository.HistoryRepository
import com.example.fxandroid.domain.model.HistoryEntry
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class HistoryViewModel @Inject constructor(
    private val repo: HistoryRepository
) : ViewModel() {

    private val _entries = MutableStateFlow<List<HistoryEntry>>(emptyList())
    val entries: StateFlow<List<HistoryEntry>> = _entries.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    fun load(limit: Int = 50, offset: Int = 0) {
        viewModelScope.launch {
            try {
                repo.page(limit, offset).collect { list ->
                    _entries.value = list.map {
                        HistoryEntry(it.id, it.actor, it.action, it.targetId, it.createdAt)
                    }
                }
            } catch (e: Exception) {
                _error.value = "Error de base de datos: ${e.message}"
            }
        }
    }

    fun search(filter: String) {
        viewModelScope.launch {
            try {
                val results = repo.findByActor(filter)
                _entries.value = results.map {
                    HistoryEntry(it.id, it.actor, it.action, it.targetId, it.createdAt)
                }
            } catch (e: Exception) {
                _error.value = "Error de base de datos"
            }
        }
    }
}