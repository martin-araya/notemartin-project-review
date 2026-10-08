package com.example.fxandroid.util

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * Trampa S1: este helper existe pero NUNCA se importa ni se llama
 * desde ningun modulo del fixture. La skill debe verificar que no
 * aparece en runtime code.
 */
object LegacyDateFormatter {
    fun format(date: Date): String {
        val fmt = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.US)
        return fmt.format(date)
    }

    fun parse(text: String): Date? {
        val fmt = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.US)
        return try { fmt.parse(text) } catch (e: Exception) { null }
    }
}