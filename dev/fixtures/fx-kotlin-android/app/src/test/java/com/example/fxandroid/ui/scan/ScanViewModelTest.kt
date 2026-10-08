package com.example.fxandroid.ui.scan

import com.example.fxandroid.data.repository.ProductRepository
import com.example.fxandroid.domain.model.Product
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.runTest
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class ScanViewModelTest {

    private class FakeRepo(private val found: Product?) : ProductRepository {
        override suspend fun scan(ean: String): ProductEntity? {
            return found
        }
        override fun observeRecent(limit: Int) = flowOf(emptyList<ProductEntity>())
    }

    @Test
    fun `validateEan rejects non 13-digit`() {
        val vm = ScanViewModel(FakeRepo(null))
        assertEquals("EAN debe ser 13 dígitos", vm.validateEan("123"))
    }

    @Test
    fun `validateEan rejects non-digit`() {
        val vm = ScanViewModel(FakeRepo(null))
        assertEquals("EAN solo dígitos", vm.validateEan("1234567890ab*3"))
    }

    @Test
    fun `onScanClick rejects invalid ean`() = runTest {
        val vm = ScanViewModel(FakeRepo(null))
        vm.onScanClick("123")
        val state = vm.state.value
        assertTrue(state is ScanState.Error)
    }

    @Test
    fun `onScanClick success path`() = runTest {
        val product = Product(1L, "8400000000017", "Test Product", 0L)
        val vm = ScanViewModel(FakeRepo(product))
        vm.onScanClick("8400000000017")
        val state = vm.state.value
        assertTrue(state is ScanState.Success)
    }
}