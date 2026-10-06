// Auditoria.java
// Entidad JPA inmutable (no setters, solo getters via @Data).
// Se crea automaticamente al confirmar una transferencia.
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
@Table(name = "auditoria")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Auditoria {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String accion;

    @Column(nullable = false)
    private String entidad;

    @Column(nullable = false)
    private String entidadId;

    @Column(nullable = false)
    private String usuarioId;

    @Column(nullable = false)
    private Instant timestamp = Instant.now();
}
