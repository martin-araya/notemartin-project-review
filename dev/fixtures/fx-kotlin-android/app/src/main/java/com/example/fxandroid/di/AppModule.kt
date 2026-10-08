package com.example.fxandroid.di

import com.example.fxandroid.data.remote.ProductRemoteSource
import com.example.fxandroid.data.repository.HistoryRepository
import com.example.fxandroid.data.repository.HistoryRepositoryImpl
import com.example.fxandroid.data.repository.ProductRepository
import com.example.fxandroid.data.repository.ProductRepositoryImpl
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

// Trampa P2: ProductRepositoryImpl NO esta marcado con @Singleton.
// El repo se recrea cada vez que se inyecta, lo que pierde estado en memoria
// (e.g. un cache en runtime). La skill debe detectar la falta de @Singleton.
@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    fun provideProductRemoteSource(): ProductRemoteSource = ProductRemoteSource()

    @Provides
    fun provideProductRepository(
        remote: ProductRemoteSource
    ): ProductRepository = ProductRepositoryImpl(remote)

    @Provides
    fun provideHistoryRepository(): HistoryRepository = HistoryRepositoryImpl()
}