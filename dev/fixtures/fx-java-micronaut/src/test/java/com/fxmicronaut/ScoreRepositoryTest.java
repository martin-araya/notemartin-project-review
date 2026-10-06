package com.fxmicronaut;

import com.fxmicronaut.domain.Score;
import com.fxmicronaut.repository.ClienteRepository;
import com.fxmicronaut.repository.ScoreRepository;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.time.Instant;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Cubre que la columna ``categoria_ajustada`` agregada por Flyway V2
 * (tabla ``score_categories``) funciona junto con ``scores``.
 *
 * Si V2 no se ejecuta, esta query falla con Table not found.
 */
@MicronautTest
class ScoreRepositoryTest {

    @Inject
    ScoreRepository scoreRepo;

    @Inject
    ClienteRepository clienteRepo;

    @AfterEach
    void cleanup() {
        scoreRepo.deleteAll();
        clienteRepo.deleteAll();
    }

    @Test
    void find_latest_by_documento_retorna_ultimo_score() {
        com.fxmicronaut.domain.Cliente cliente = clienteRepo.save(
                new com.fxmicronaut.domain.Cliente(null, "S1", "DOC-S1", "s1@example.com", null));

        // Insertamos dos scores: el segundo es el mas reciente.
        scoreRepo.save(new Score(null, cliente.id(), 700, "AAA", Instant.now().minusSeconds(60)));
        scoreRepo.save(new Score(null, cliente.id(), 850, "AAA", Instant.now()));

        Optional<Score> latest = scoreRepo.findLatestByDocumento("DOC-S1");
        assertThat(latest).isPresent();
        assertThat(latest.get().valor()).isEqualTo(850);
    }

    @Test
    void find_latest_by_documento_retorna_vacio_si_no_hay() {
        assertThat(scoreRepo.findLatestByDocumento("NOPE")).isEmpty();
    }

    @Test
    void migracion_v2_crea_tabla_score_categories() {
        // La migracion V2 crea esta tabla. Si no se ejecuta, la query
        // findLatestByDocumento falla. Aqui verificamos que la query
        // corre sin error (es decir, la tabla existe).
        com.fxmicronaut.domain.Cliente cliente = clienteRepo.save(
                new com.fxmicronaut.domain.Cliente(null, "S2", "DOC-S2", "s2@example.com", null));
        scoreRepo.save(new Score(null, cliente.id(), 600, "BBB", Instant.now()));
        Optional<Score> latest = scoreRepo.findLatestByDocumento("DOC-S2");
        assertThat(latest).isPresent();
    }
}
