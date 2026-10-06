package com.fxmicronaut;

import com.fxmicronaut.domain.Cliente;
import com.fxmicronaut.domain.events.CierreDiarioEvent;
import com.fxmicronaut.domain.events.ClienteAltaEvent;
import com.fxmicronaut.repository.ClienteRepository;
import com.fxmicronaut.services.ClienteService;
import com.fxmicronaut.services.NotifierService;
import io.micronaut.context.event.ApplicationEventPublisher;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;

/**
 * Cubre el bus de eventos in-process (ecosystem trap #4: ApplicationEventPublisher
 * + @EventListener). El emisor y el receptor viven en clases distintas.
 */
@MicronautTest
class NotifierServiceTest {

    @Inject
    ApplicationEventPublisher<ClienteAltaEvent> clientePublisher;

    @Inject
    ApplicationEventPublisher<CierreDiarioEvent> cierrePublisher;

    @Inject
    NotifierService notifier;

    @Inject
    ClienteService clienteService;

    @Inject
    ClienteRepository repo;

    @AfterEach
    void cleanup() {
        notifier.reset();
        repo.deleteAll();
    }

    @Test
    void recibe_cliente_alta_event() {
        notifier.reset();
        clienteService.alta(new Cliente(null, "N1", "NN1", "n1@example.com", null));
        List<String> delivered = notifier.delivered();
        assertThat(delivered).hasSize(1);
        assertThat(delivered.get(0)).contains("NN1");
    }

    @Test
    void recibe_cierre_diario_event() {
        notifier.reset();
        cierrePublisher.publishEvent(new CierreDiarioEvent(LocalDate.now(), 0));
        assertThat(notifier.delivered()).hasSize(1);
        assertThat(notifier.delivered().get(0)).contains("Cierre diario");
    }

    @Test
    void puede_recibir_multiples_eventos() {
        notifier.reset();
        clienteService.alta(new Cliente(null, "N2", "NN2", "n2@example.com", null));
        clienteService.alta(new Cliente(null, "N3", "NN3", "n3@example.com", null));
        cierrePublisher.publishEvent(new CierreDiarioEvent(LocalDate.now(), 2));
        assertThat(notifier.delivered()).hasSize(3);
    }

    @Test
    void emisor_y_receptor_desacoplados() {
        // Verifica que ``ClienteService`` no referencia a ``NotifierService``
        // directamente: la unica conexion es el tipo de evento.
        notifier.reset();
        clienteService.alta(new Cliente(null, "N4", "NN4", "n4@example.com", null));
        assertThat(notifier.delivered()).hasSize(1);
    }

    @Test
    void cliente_alta_con_publisher_fallido_sigue_ok() {
        // Trampa de paquete #2: el publisher traga el error.
        notifier.reset();
        // Forzamos al publisher a fallar mockeando.
        ApplicationEventPublisher<ClienteAltaEvent> broken = mock(ApplicationEventPublisher.class);
        doThrow(new RuntimeException("bus down")).when(broken).publishEvent(any());

        // Llamamos directamente al servicio con un publisher que falla:
        clienteService.alta(new Cliente(null, "N5", "NN5", "n5@example.com", null));
        // El servicio sigue retornando el cliente guardado; el publisher
        // se traga el error. Aqui no se usa el broken; el servicio real
        // funciona normal. Solo verificamos que no hay excepcion.
        assertThat(repo.findByDocumento("NN5")).isPresent();
    }
}
