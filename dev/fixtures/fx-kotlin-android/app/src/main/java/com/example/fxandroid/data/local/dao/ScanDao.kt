package com.example.fxandroid.data.local.dao

import androidx.room.Dao
import androidx.room.Query
import com.example.fxandroid.data.local.entity.ProductEntity
import com.example.fxandroid.data.local.entity.HistoryEntity

@Dao
interface ScanDao {
    @Query("DELETE FROM products")
    suspend fun clearProducts()

    @Query("DELETE FROM history")
    suspend fun clearHistory()

    @Query("SELECT COUNT(*) FROM products")
    suspend fun productCount(): Int

    @Query("SELECT COUNT(*) FROM history")
    suspend fun historyCount(): Int
}