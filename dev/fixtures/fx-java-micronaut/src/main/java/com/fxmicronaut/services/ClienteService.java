package com.fxmicronaut.services;

import com.fxmicronaut.domain.Cliente;
import com.fxmicronaut.domain.events.ClienteAltaEvent;
import com.fxmicronaut.exceptions.DuplicateClienteException;
import com.fxmicronaut.repository.ClienteRepository;
import io.micronaut.context.event.ApplicationEventPublisher;
import jakarta.inject.Singleton;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Orquesta la alta de un cliente: valida duplicados, persiste, y publica
 * el evento ``ClienteAltaEvent``.
 *
 * Trampa de paquete #2: la excepcion del publisher se traga (try/catch
 * vacio) para que un fallo de Notifier no bloquee el alta.
 *
 * Trampa de paquete #3: el metodo no es transaccional. Dos inserts
 * concurrentes con el mismo documento pueden ambos pasar el ``findByDocumento``
 * y ambos llegar a ``save``; el UNIQUE constraint los rechaza.
 */
@Singleton
public class ClienteService {

    private static final Logger log = LoggerFactory.getLogger(ClienteService.class);

    private final ClienteRepository repo;
    private final ApplicationEventPublisher<ClienteAltaEvent> publisher;

    public ClienteService(ClienteRepository repo,
                          ApplicationEventPublisher<ClienteAltaEvent> publisher) {
        this.repo = repo;
        this.publisher = publisher;
    }

    public Cliente alta(Cliente c) {
        repo.findByDocumento(c.documento()).ifPresent(existing -> {
            throw new DuplicateClienteException(existing.documento());
        });
        Cliente saved = repo.save(c);
        try {
            // Trampa de paquete #2: swallow del error del publisher.
            publisher.publishEvent(new ClienteAltaEvent(saved));
        } catch (RuntimeException re) {
            log.warn("publisher fallo para {}: {}", saved.documento(), re.getMessage());
        }
        return saved;
    }
}
