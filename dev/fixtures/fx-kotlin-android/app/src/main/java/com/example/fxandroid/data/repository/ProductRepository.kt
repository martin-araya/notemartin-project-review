package com.example.fxandroid.data.repository

import com.example.fxandroid.data.local.dao.ProductDao
import com.example.fxandroid.data.local.entity.ProductEntity
import com.example.fxandroid.data.remote.ProductRemoteSource
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

interface ProductRepository {
    suspend fun scan(ean: String): ProductEntity?
    fun observeRecent(limit: Int = 50): Flow<List<ProductEntity>>
}

class ProductRepositoryImpl @Inject constructor(
    private val remote: ProductRemoteSource,
    private val productDao: ProductDao
) : ProductRepository {

    override suspend fun scan(ean: String): ProductEntity? {
        val existing = productDao.findByEan(ean)
        if (existing != null) return existing
        val remoteProduct = remote.fetchByEan(ean) ?: return null
        val entity = ProductEntity(
            ean = remoteProduct.ean,
            name = remoteProduct.name,
            scannedAt = System.currentTimeMillis()
        )
        val id = productDao.insert(entity)
        return entity.copy(id = id)
    }

    override fun observeRecent(limit: Int): Flow<List<ProductEntity>> =
        productDao.observeRecent(limit)
}