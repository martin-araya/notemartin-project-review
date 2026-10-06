// TransferenciaService.java
// Service con el bug de auto-invocation AOP. Trampa ecosistema
// #2: el metodo transferir() llama internamente a
// this.validarSaldo() (que es @Transactional(propagation =
// REQUIRES_NEW)). Como Spring AOP no intercepta llamadas this,
// validarSaldo se ejecuta dentro de la transaccion padre en
// vez de crear una nueva. La skill debe notar la llamada
// interna y la falta de proxy.
package com.example.fxspring.service;

import com.example.fxspring.domain.Transferencia;
import com.example.fxspring.event.TransferenciaRealizadaEvent;
import com.example.fxspring.repository.TransferenciaRepository;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class TransferenciaService {

    private final TransferenciaRepository repo;
    private final ApplicationEventPublisher publisher;

    public TransferenciaService(TransferenciaRepository repo, ApplicationEventPublisher publisher) {
        this.repo = repo;
        this.publisher = publisher;
    }

    @Transactional
    public Transferencia crear(Long cuentaOrigenId, Long cuentaDestinoId, java.math.BigDecimal monto) {
        // Bug: this.validarSaldo() no se intercepta por AOP
        // porque es una llamada interna. validarSaldo corre
        // dentro de la misma transaccion, no en REQUIRES_NEW.
        this.validarSaldo(cuentaOrigenId, monto);

        Transferencia t = new Transferencia();
        t.setCuentaOrigenId(cuentaOrigenId);
        t.setCuentaDestinoId(cuentaDestinoId);
        t.setMonto(monto);
        t.setEstado(Transferencia.Estado.PENDIENTE);
        return repo.save(t);
    }

    // Trampa paquete #6: el throw de RuntimeException NO se
    // maneja en el listener. Spring lo ignora silenciosamente
    // despues del commit, pero el listener no reintenta.
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void validarSaldo(Long cuentaOrigenId, java.math.BigDecimal monto) {
        if (monto.signum() < 0) {
            throw new RuntimeException("monto invalido");
        }
    }

    @Transactional
    public Transferencia confirmar(Long id) {
        Transferencia t = repo.findByIdForUpdate(id)
            .orElseThrow(() -> new IllegalStateException("not_found"));
        t.setEstado(Transferencia.Estado.COMPLETADA);
        Transferencia saved = repo.save(t);
        // Dispara el evento que el listener procesa en AFTER_COMMIT.
        publisher.publishEvent(new TransferenciaRealizadaEvent(this, saved.getId()));
        return saved;
    }

    @Transactional(readOnly = true)
    public List<Transferencia> listarPorOrigen(Long cuentaOrigenId) {
        return repo.findByCuentaOrigenId(cuentaOrigenId);
    }
}
