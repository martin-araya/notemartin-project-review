package com.fxmicronaut.domain;

import io.micronaut.data.annotation.GeneratedValue;
import io.micronaut.data.annotation.Id;
import io.micronaut.data.annotation.MappedEntity;
import io.micronaut.serde.annotation.Serdeable;

import java.time.Instant;

/**
 * Score externo asociado a un cliente. La columna ``categoria`` puede
 * contener valores "AAA", "BBB", "CCC" que se mapean a
 * ``categoria_ajustada`` (premium/standard/basic) en la tabla
 * ``score_categories`` (definida en V2). La conversion vive en la
 * @Query nativa de ScoreRepository.
 */
@MappedEntity("scores")
@Serdeable
public record Score(
        @Id @GeneratedValue Long id,
        Long clienteId,
        int valor,
        String categoria,
        Instant computedAt
) {}
