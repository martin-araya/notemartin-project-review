// Notificacion.java
// Entidad JPA simple. Se crea via @TransactionalEventListener
// (AFTER_COMMIT) cuando se confirma una transferencia.
package com.example.fxspring.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Entity
@Table(name = "notificaciones")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Notificacion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String destinatario;

    @Column(nullable = false)
    private String mensaje;

    @Column(nullable = false)
    private String estado = "PENDIENTE";

    @Column(nullable = false, updatable = false)
    private Instant createdAt = Instant.now();
}
