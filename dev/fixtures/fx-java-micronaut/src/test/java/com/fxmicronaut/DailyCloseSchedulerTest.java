package com.fxmicronaut;

import com.fxmicronaut.config.DailyCloseConfig;
import com.fxmicronaut.domain.Cliente;
import com.fxmicronaut.domain.events.CierreDiarioEvent;
import com.fxmicronaut.repository.ClienteRepository;
import com.fxmicronaut.scheduler.DailyCloseScheduler;
import com.fxmicronaut.services.NotifierService;
import io.micronaut.context.ApplicationContext;
import io.micronaut.context.DefaultApplicationContext;
import io.micronaut.context.event.ApplicationEventPublisher;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

/**
 * Cubre el scheduler de cierre diario. Como el cron real se dispara
 * a las 2 AM (config por defecto), los tests invocan ``run()`` directamente.
 *
 * Trampa del ecosistema #5: la expresion cron esta en la configuracion
 * (``daily-close.cron``), no hardcodeada.
 *
 * Trampa de paquete #4: si ``config.enabled()`` es false, run() retorna
 * sin publicar el evento.
 */
@MicronautTest
class DailyCloseSchedulerTest {

    @Inject
    DailyCloseScheduler scheduler;

    @Inject
    ClienteRepository repo;

    @Inject
    NotifierService notifier;

    @Inject
    DailyCloseConfig config;

    @Inject
    ApplicationContext ctx;

    @AfterEach
    void cleanup() {
        notifier.reset();
        repo.deleteAll();
    }

    @Test
    void run_publica_evento_con_total_de_clientes() {
        notifier.reset();
        repo.save(new Cliente(null, "D1", "D1", "d1@example.com", null));
        repo.save(new Cliente(null, "D2", "D2", "d2@example.com", null));
        repo.save(new Cliente(null, "D3", "D3", "d3@example.com", null));

        // Forzamos enabled=true (en tests viene false desde application-test.yml).
        // En vez de tocar la config, instanciamos el scheduler manualmente
        // con un mock de DailyCloseConfig.
        ApplicationEventPublisher<CierreDiarioEvent> publisher = mock(ApplicationEventPublisher.class);
        DailyCloseConfig enabledConfig = mock(DailyCloseConfig.class);
        when(enabledConfig.enabled()).thenReturn(true);

        DailyCloseScheduler s = new DailyCloseScheduler(repo, publisher, enabledConfig);
        s.run();

        verify(publisher).publishEvent(org.mockito.ArgumentMatchers.argThat(
                e -> e.totalClientes() == 3
        ));
    }

    @Test
    void run_no_publica_si_disabled() {
        // Aqui usamos el scheduler real (config.enabled() = false desde
        // application-test.yml). No debe publicar nada.
        notifier.reset();
        repo.save(new Cliente(null, "D1", "D1", "d1@example.com", null));

        scheduler.run();
        assertThat(notifier.delivered()).isEmpty();
    }

    @Test
    void tiene_expresion_cron_externa() {
        // Verifica que la anotacion @Scheduled lee la expresion de la
        // configuracion. Aqui solo verificamos que la config esta disponible.
        assertThat(config.cron()).isNotBlank();
    }
}
