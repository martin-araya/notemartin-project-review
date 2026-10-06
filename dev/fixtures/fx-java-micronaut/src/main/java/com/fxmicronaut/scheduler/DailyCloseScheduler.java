package com.fxmicronaut.scheduler;

import com.fxmicronaut.config.DailyCloseConfig;
import com.fxmicronaut.domain.events.CierreDiarioEvent;
import com.fxmicronaut.repository.ClienteRepository;
import io.micronaut.context.event.ApplicationEventPublisher;
import io.micronaut.scheduling.annotation.Scheduled;
import jakarta.inject.Singleton;

import java.time.LocalDate;

/**
 * Scheduler de cierre diario.
 *
 * Trampa del ecosistema #5: la expresion cron esta en la configuracion
 * (``daily-close.cron``), no hardcodeada en el codigo. Se puede cambiar
 * por variable de entorno o por application-{profile}.yml.
 *
 * Trampa de paquete #4: si ``config`` es null, el metodo lanza NPE. El
 * caller debe inyectar siempre ``DailyCloseConfig``.
 */
@Singleton
public class DailyCloseScheduler {

    private final ClienteRepository repo;
    private final ApplicationEventPublisher<CierreDiarioEvent> publisher;
    private final DailyCloseConfig config;

    public DailyCloseScheduler(ClienteRepository repo,
                               ApplicationEventPublisher<CierreDiarioEvent> publisher,
                               DailyCloseConfig config) {
        this.repo = repo;
        this.publisher = publisher;
        this.config = config;
    }

    @Scheduled(cron = "${daily-close.cron}")
    public void run() {
        if (!config.enabled()) {
            return;
        }
        int total = (int) repo.count();
        publisher.publishEvent(new CierreDiarioEvent(LocalDate.now(), total));
    }
}
