// Transferencia.java
// Entidad JPA con @Version (optimistic lock). Trampa paquete
// #5: el servicio no maneja OptimisticLockException; si dos
// requests modifican la misma transferencia, el segundo hace
// upsert silencioso. La skill debe notar la presencia de
// @Version y la falta de manejo de OptimisticLockException.
package com.example.fxspring.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.Version;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "transferencias")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Transferencia {

    public enum Estado { PENDIENTE, COMPLETADA, RECHAZADA }

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long cuentaOrigenId;

    @Column(nullable = false)
    private Long cuentaDestinoId;

    @Column(nullable = false)
    private BigDecimal monto;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Estado estado = Estado.PENDIENTE;

    @Version
    private Long version;

    @Column(nullable = false, updatable = false)
    private Instant createdAt = Instant.now();
}
