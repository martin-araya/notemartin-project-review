package com.example.fxandroid.work

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.example.fxandroid.data.repository.HistoryRepository
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject

@HiltWorker
class SyncWorker @AssistedInject constructor(
    @Assisted ctx: Context,
    @Assisted params: WorkerParameters,
    private val historyRepository: HistoryRepository
) : CoroutineWorker(ctx, params) {

    override suspend fun doWork(): Result {
        return try {
            historyRepository.upsert(
                com.example.fxandroid.data.local.entity.HistoryEntity(
                    actor = "sync",
                    action = "tick",
                    targetId = "0",
                    createdAt = System.currentTimeMillis()
                )
            )
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }
}