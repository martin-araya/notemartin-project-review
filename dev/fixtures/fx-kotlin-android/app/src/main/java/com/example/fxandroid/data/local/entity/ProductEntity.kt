package com.example.fxandroid.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "products",
    indices = [Index(value = ["ean"], unique = true)]
)
data class ProductEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val ean: String,
    val name: String,
    val scannedAt: Long
)