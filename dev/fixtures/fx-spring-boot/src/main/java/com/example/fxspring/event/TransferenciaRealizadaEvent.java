// TransferenciaRealizadaEvent.java
// Evento publicado por TransferenciaService al confirmar
// una transferencia. El listener lo procesa en AFTER_COMMIT.
package com.example.fxspring.event;

import org.springframework.context.ApplicationEvent;

public class TransferenciaRealizadaEvent extends ApplicationEvent {
    private final Long transferenciaId;

    public TransferenciaRealizadaEvent(Object source, Long transferenciaId) {
        super(source);
        this.transferenciaId = transferenciaId;
    }

    public Long getTransferenciaId() {
        return transferenciaId;
    }
}
