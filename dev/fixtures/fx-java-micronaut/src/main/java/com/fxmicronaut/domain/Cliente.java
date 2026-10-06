package com.fxmicronaut.domain;

import io.micronaut.data.annotation.GeneratedValue;
import io.micronaut.data.annotation.Id;
import io.micronaut.data.annotation.MappedEntity;
import io.micronaut.serde.annotation.Serdeable;
import jakarta.validation.constraints.NotBlank;

import java.time.Instant;

/**
 * Entidad Cliente. Mapea a la tabla ``clientes`` (definida en
 * V1__create_clientes.sql). El id es generado por la BD.
 */
@MappedEntity("clientes")
@Serdeable
public record Cliente(
        @Id @GeneratedValue Long id,
        @NotBlank String nombre,
        @NotBlank String documento,
        @NotBlank String email,
        Instant createdAt
) {
    public Cliente {
        if (createdAt == null) {
            createdAt = Instant.now();
        }
    }
}
