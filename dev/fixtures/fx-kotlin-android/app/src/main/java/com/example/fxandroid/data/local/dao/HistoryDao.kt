package com.example.fxandroid.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.example.fxandroid.data.local.entity.HistoryEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface HistoryDao {

    @Query("SELECT * FROM history ORDER BY createdAt DESC LIMIT :limit OFFSET :offset")
    fun page(limit: Int, offset: Int): Flow<List<HistoryEntity>>

    // Trampa P1: SQL con string concatenation vulnerable a SQLi
    // (no es @Query sino el helper findByActorUnsafe que demuestra
    // el patron peligroso). El DAO correcto usa @Query con param.
    @Query("SELECT * FROM history WHERE actor = :actor ORDER BY createdAt DESC")
    suspend fun findByActor(actor: String): List<HistoryEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(entry: HistoryEntity)

    @Query("DELETE FROM history WHERE id = :id")
    suspend fun deleteById(id: Long)

    @Query("SELECT COUNT(*) FROM history")
    suspend fun count(): Int
}