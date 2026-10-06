package com.fxmicronaut.domain.events;

import com.fxmicronaut.domain.Cliente;

/**
 * Evento publicado cuando un cliente es dado de alta.
 * Lo emite ``ClienteService.alta`` y lo consume ``NotifierService``
 * (acoplados por tipo, no por referencia directa).
 */
public record ClienteAltaEvent(Cliente cliente) {}
