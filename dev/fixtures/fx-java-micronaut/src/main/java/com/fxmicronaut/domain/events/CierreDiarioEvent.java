package com.fxmicronaut.domain.events;

import java.time.LocalDate;

/**
 * Evento publicado por ``DailyCloseScheduler`` al cierre diario.
 * Lo consume ``NotifierService``.
 */
public record CierreDiarioEvent(LocalDate fecha, int totalClientes) {}
