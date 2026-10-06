package com.fxmicronaut.repository;

import com.fxmicronaut.domain.Score;
import io.micronaut.data.annotation.Query;
import io.micronaut.data.jdbc.annotation.JdbcRepository;
import io.micronaut.data.model.query.builder.sql.Dialect;
import io.micronaut.data.repository.CrudRepository;

import java.util.Optional;

/**
 * Repository de Score. ``findLatestByDocumentoAndCategory`` es una @Query
 * nativa que depende de la columna ``score_categories.categoria_ajustada``
 * agregada por la migracion V2 de Flyway. Sin V2 esta query fallaria.
 */
@JdbcRepository(dialect = Dialect.H2)
public interface ScoreRepository extends CrudRepository<Score, Long> {

    @Query("""
            SELECT s.id AS id, s.cliente_id AS clienteId, s.valor AS valor,
                   sc.categoria_ajustada AS categoria, s.computed_at AS computedAt
            FROM scores s
            JOIN clientes c ON c.id = s.cliente_id
            JOIN score_categories sc ON sc.code = s.categoria
            WHERE c.documento = :documento
            ORDER BY s.computed_at DESC
            LIMIT 1
            """)
    Optional<Score> findLatestByDocumento(String documento);
}
