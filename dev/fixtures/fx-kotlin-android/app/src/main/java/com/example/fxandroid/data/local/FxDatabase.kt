package com.example.fxandroid.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.example.fxandroid.data.local.dao.HistoryDao
import com.example.fxandroid.data.local.dao.ProductDao
import com.example.fxandroid.data.local.dao.ScanDao
import com.example.fxandroid.data.local.entity.HistoryEntity
import com.example.fxandroid.data.local.entity.ProductEntity

@Database(
    entities = [ProductEntity::class, HistoryEntity::class],
    version = 1,
    exportSchema = false
)
abstract class FxDatabase : RoomDatabase() {
    abstract fun productDao(): ProductDao
    abstract fun historyDao(): HistoryDao
    abstract fun scanDao(): ScanDao
}