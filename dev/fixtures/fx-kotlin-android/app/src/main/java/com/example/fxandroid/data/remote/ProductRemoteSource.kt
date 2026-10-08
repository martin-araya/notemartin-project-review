package com.example.fxandroid.data.remote

/**
 * Stub de cliente remoto. La skill debe notar que NO se usa ningun
 * cliente HTTP real (Retrofit/Ktor); las llamadas se simulan en memoria.
 */
class ProductRemoteSource {
    fun fetchByEan(ean: String): RemoteProductDto? {
        // Simulación: solo devuelve un producto si el EAN empieza con "84"
        if (!ean.startsWith("84")) return null
        return RemoteProductDto(ean = ean, name = "Producto $ean")
    }
}

data class RemoteProductDto(
    val ean: String,
    val name: String
)