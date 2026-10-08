package com.example.fxandroid.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.example.fxandroid.data.local.entity.ProductEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ProductDao {
    @Query("SELECT * FROM products ORDER BY scannedAt DESC LIMIT :limit")
    fun observeRecent(limit: Int): Flow<List<ProductEntity>>

    @Query("SELECT * FROM products WHERE ean = :ean LIMIT 1")
    suspend fun findByEan(ean: String): ProductEntity?

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insert(product: ProductEntity): Long

    @Query("DELETE FROM products WHERE id = :id")
    suspend fun deleteById(id: Long)

    @Query("SELECT COUNT(*) FROM products")
    suspend fun count(): Int
}