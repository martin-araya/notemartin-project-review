// di/AppModule.kt
// Modulo de Koin para la inyeccion de dependencias.
// Trampa ecosistema #6: InventarioService declara `repo` con
// `by inject()`, que requiere KoinComponent. La trampa es que
// en una corrutina con `Dispatchers.Default`, el
// KoinComponent queda en un thread distinto y el `inject()`
// puede fallar.
// Trampa superficial #3: se declara `single { DummyLogger() }`
// pero la app no lo usa.
package com.example.fxktor.di

import com.example.fxktor.repository.AlertRepository
import com.example.fxktor.repository.ItemRepository
import com.example.fxktor.service.AlertasService
import com.example.fxktor.service.InventarioService
import org.koin.dsl.module
import org.slf4j.Logger
import org.slf4j.LoggerFactory

class DummyLogger : Logger by LoggerFactory.getLogger("dummy")

val appModule = module {
    single<ItemRepository> { ItemRepository() }
    single<AlertRepository> { AlertRepository() }
    single<InventarioService> { InventarioService(get()) }
    single<AlertasService> { AlertasService(get()) }
    single<DummyLogger> { DummyLogger() }
}
