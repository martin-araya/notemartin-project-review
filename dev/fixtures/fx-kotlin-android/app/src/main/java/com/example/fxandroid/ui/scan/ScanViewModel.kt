package com.example.fxandroid.ui.scan

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.fxandroid.data.repository.ProductRepository
import com.example.fxandroid.domain.model.Product
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed interface ScanState {
    data object Idle : ScanState
    data object Scanning : ScanState
    data class Success(val product: Product) : ScanState
    data class Error(val message: String) : ScanState
}

@HiltViewModel
class ScanViewModel @Inject constructor(
    private val repo: ProductRepository
) : ViewModel() {

    private val _state = MutableStateFlow<ScanState>(ScanState.Idle)
    val state: StateFlow<ScanState> = _state.asStateFlow()

    fun validateEan(ean: String): String? {
        if (ean.length != 13) return "EAN debe ser 13 dígitos"
        if (!ean.all { it.isDigit() }) return "EAN solo dígitos"
        return null
    }

    fun onScanClick(ean: String) {
        val err = validateEan(ean)
        if (err != null) {
            _state.value = ScanState.Error(err)
            return
        }
        viewModelScope.launch {
            _state.value = ScanState.Scanning
            try {
                val product = repo.scan(ean)
                if (product != null) {
                    _state.value = ScanState.Success(
                        Product(product.id, product.ean, product.name, product.scannedAt)
                    )
                } else {
                    _state.value = ScanState.Error("Producto no encontrado")
                }
            } catch (e: Exception) {
                // Trampa P6: try-catch silencioso. La skill debe detectar
                // que el catch no hace nada con la excepcion (no la logea,
                // no la rethrow, no la reporta al usuario).
            }
        }
    }
}