// NotificacionListener.java
// Listener transaccional. Trampa ecosistema #5:
// @TransactionalEventListener(phase = AFTER_COMMIT) significa
// que el listener solo se ejecuta si la transaccion padre hizo
// commit. Si la transaccion hace rollback, el listener NO corre.
// Ademas, si el listener lanza una excepcion, Spring la ignora
// silenciosamente (trampa paquete #6).
package com.example.fxspring.listener;

import com.example.fxspring.domain.Transferencia;
import com.example.fxspring.event.TransferenciaRealizadaEvent;
import com.example.fxspring.repository.TransferenciaRepository;
import com.example.fxspring.service.AuditoriaService;
import com.example.fxspring.service.NotificacionService;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;
import org.springframework.transaction.event.TransactionPhase;
import org.springframework.transaction.event.TransactionalEventListener;

@Component
public class NotificacionListener {

    private final TransferenciaRepository transferencias;
    private final NotificacionService notificaciones;
    private final AuditoriaService auditoria;

    public NotificacionListener(TransferenciaRepository transferencias,
                                 NotificacionService notificaciones,
                                 AuditoriaService auditoria) {
        this.transferencias = transferencias;
        this.notificaciones = notificaciones;
        this.auditoria = auditoria;
    }

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onTransferenciaRealizada(TransferenciaRealizadaEvent event) {
        Transferencia t = transferencias.findById(event.getTransferenciaId()).orElse(null);
        if (t == null) return;
        // Dead code: la notificacion no se envia realmente.
        notificaciones.enviar("u-" + t.getCuentaOrigenId(),
                              "Transferencia " + t.getId() + " completada");
        // Trampa paquete #5: OptimisticLockException no se maneja.
        auditoria.registrar("TRANSFERENCIA_COMPLETADA",
                              "Transferencia",
                              String.valueOf(t.getId()),
                              "u-" + t.getCuentaOrigenId());
    }
}
