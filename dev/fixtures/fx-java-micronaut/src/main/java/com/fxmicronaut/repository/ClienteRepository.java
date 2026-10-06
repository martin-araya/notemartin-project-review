package com.fxmicronaut.repository;

import com.fxmicronaut.domain.Cliente;
import io.micronaut.data.jdbc.annotation.JdbcRepository;
import io.micronaut.data.model.query.builder.sql.Dialect;
import io.micronaut.data.repository.CrudRepository;

import java.util.Optional;

@JdbcRepository(dialect = Dialect.H2)
public interface ClienteRepository extends CrudRepository<Cliente, Long> {
    Optional<Cliente> findByDocumento(String documento);
}
