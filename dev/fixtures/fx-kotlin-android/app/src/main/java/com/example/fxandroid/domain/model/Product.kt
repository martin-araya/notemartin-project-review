package com.example.fxandroid.domain.model

data class Product(
    val id: Long,
    val ean: String,
    val name: String,
    val scannedAt: Long
) {
    val eanValid: Boolean
        get() = ean.length == 13 && ean.all { it.isDigit() }
}