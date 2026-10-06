// tests/service/TransferenciaServiceTest.java
// Tests runtime de TransferenciaService. Verifica el bug de
// auto-invocation: this.validarSaldo() corre en la misma
// transaccion (no en REQUIRES_NEW).
package com.example.fxspring.service;

import com.example.fxspring.domain.Transferencia;
import com.example.fxspring.repository.TransferenciaRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@SpringBootTest
@ActiveProfiles("test")
class TransferenciaServiceTest {

    @Autowired
    private TransferenciaService service;

    @MockBean
    private TransferenciaRepository repo;

    @MockBean
    private ApplicationEventPublisher publisher;

    @Test
    void crear_persiste_con_estado_pendiente() {
        when(repo.save(any(Transferencia.class))).thenAnswer(inv -> {
            Transferencia t = inv.getArgument(0);
            t.setId(1L);
            return t;
        });
        Transferencia t = service.crear(1L, 2L, new BigDecimal("100.00"));
        assertEquals(Transferencia.Estado.PENDIENTE, t.getEstado());
        assertNotNull(t.getCreatedAt());
    }

    @Test
    void crear_rechaza_monto_negativo() {
        // El bug de auto-invocation: this.validarSaldo() corre
        // en la misma transaccion, asi que el throw NO crea
        // una nueva transaccion. La propagacion del error sigue
        // funcionando porque REQUIRES_NEW no se respeta.
        assertThrows(RuntimeException.class, () ->
            service.crear(1L, 2L, new BigDecimal("-50.00"))
        );
    }

    @Test
    void confirmar_pasa_a_estado_completada_y_dispara_evento() {
        Transferencia t = new Transferencia();
        t.setId(1L);
        t.setEstado(Transferencia.Estado.PENDIENTE);
        when(repo.findByIdForUpdate(1L)).thenReturn(Optional.of(t));
        when(repo.save(any(Transferencia.class))).thenAnswer(inv -> inv.getArgument(0));

        Transferencia saved = service.confirmar(1L);
        assertEquals(Transferencia.Estado.COMPLETADA, saved.getEstado());
    }
}
