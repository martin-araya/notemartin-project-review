package com.fxmicronaut.services;

import com.fxmicronaut.domain.events.CierreDiarioEvent;
import com.fxmicronaut.domain.events.ClienteAltaEvent;
import io.micronaut.runtime.event.annotation.EventListener;
import jakarta.inject.Singleton;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Servicio desacoplado: recibe eventos via @EventListener. NO conoce a los
 * emisores; solo conoce los tipos de evento.
 *
 * Trampa del ecosistema #4: el emisor y el receptor viven en clases
 * distintas. El scanner debe leer ``ApplicationEventPublisher.publishEvent``
 * en un lado y ``@EventListener`` en otro.
 *
 * Trampa de paquete #6: el bean se inyecta en el primer evento, no al
 * arranque. Si la inyeccion falla, el error aparece al primer evento, no
 * en el startup.
 */
@Singleton
public class NotifierService {

    private static final Logger log = LoggerFactory.getLogger(NotifierService.class);

    private final List<String> delivered = new ArrayList<>();

    public List<String> delivered() {
        return Collections.unmodifiableList(delivered);
    }

    public void reset() {
        delivered.clear();
    }

    @EventListener
    public void onClienteAlta(ClienteAltaEvent event) {
        String msg = "Notificacion enviada para cliente " + event.cliente().documento();
        delivered.add(msg);
        log.info(msg);
    }

    @EventListener
    public void onCierreDiario(CierreDiarioEvent event) {
        String msg = "Cierre diario procesado: " + event.totalClientes() + " clientes en " + event.fecha();
        delivered.add(msg);
        log.info(msg);
    }
}
