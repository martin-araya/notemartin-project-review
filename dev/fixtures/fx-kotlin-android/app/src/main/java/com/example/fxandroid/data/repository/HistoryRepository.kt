package com.example.fxandroid.data.repository

import com.example.fxandroid.data.local.dao.HistoryDao
import com.example.fxandroid.data.local.entity.HistoryEntity
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

interface HistoryRepository {
    fun page(limit: Int, offset: Int): Flow<List<HistoryEntity>>
    suspend fun findByActor(actor: String): List<HistoryEntity>
    suspend fun upsert(entry: HistoryEntity)
}

class HistoryRepositoryImpl @Inject constructor(
    private val dao: HistoryDao
) : HistoryRepository {

    override fun page(limit: Int, offset: Int): Flow<List<HistoryEntity>> =
        dao.page(limit, offset)

    override suspend fun findByActor(actor: String): List<HistoryEntity> =
        dao.findByActor(actor)

    override suspend fun upsert(entry: HistoryEntity) =
        dao.upsert(entry)
}