package com.example.fxandroid.work

import android.content.Context
import androidx.work.Constraints
import androidx.work.ExistingWorkPolicy
import androidx.work.NetworkType
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.OutOfQuotaPolicy
import androidx.work.WorkManager
import androidx.work.WorkRequest
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SyncScheduler @Inject constructor(
    @ApplicationContext private val ctx: Context
) {
    fun scheduleOnce(): WorkRequest {
        // Trampa P3: expedited sin verificar POST_NOTIFICATIONS en API 33+.
        // El worker falla silenciosamente sin notificar al usuario.
        val request = OneTimeWorkRequestBuilder<SyncWorker>()
            .setConstraints(
                Constraints.Builder()
                    .setRequiredNetworkType(NetworkType.CONNECTED)
                    .build()
            )
            .setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)
            .build()
        WorkManager.getInstance(ctx)
            .enqueueUniqueWork("sync", ExistingWorkPolicy.REPLACE, request)
        return request
    }
}