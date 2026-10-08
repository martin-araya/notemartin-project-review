package com.example.fxandroid.di

import android.content.Context
import androidx.room.Room
import com.example.fxandroid.data.local.FxDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(
        @ApplicationContext ctx: Context
    ): FxDatabase {
        // Trampa P4: el builder no invoca el metodo de migracion.
        // Si en el futuro se sube la version, la app crashea
        // con IllegalStateException. La skill debe notar la version
        // y la ausencia de migraciones.
        return Room.databaseBuilder(
            ctx,
            FxDatabase::class.java,
            "fx_android.db"
        )
            .fallbackToDestructiveMigrationOnDowngrade(true)
            .build()
    }

    @Provides
    fun provideProductDao(db: FxDatabase) = db.productDao()

    @Provides
    fun provideHistoryDao(db: FxDatabase) = db.historyDao()

    @Provides
    fun provideScanDao(db: FxDatabase) = db.scanDao()
}