package com.example.fxandroid.util

import com.example.fxandroid.BuildConfig

/**
 * Trampa S2: BuildConfig.DEBUG se lee pero nunca se usa.
 * La skill debe detectar la variable `debug` no usada.
 */
object EnvConfig {
    val debug: Boolean = BuildConfig.DEBUG

    fun isDebug(): Boolean = debug
}