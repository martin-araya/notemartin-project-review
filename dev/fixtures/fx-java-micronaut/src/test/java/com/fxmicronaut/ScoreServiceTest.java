package com.fxmicronaut;

import com.fxmicronaut.client.ScoreClient;
import com.fxmicronaut.domain.Score;
import com.fxmicronaut.services.ScoreService;
import io.micronaut.test.annotation.MockBean;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.Test;

import java.time.Instant;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

/**
 * Cubre el flujo de consulta de score al cliente externo:
 *  - el stub de ScoreClient devuelve un score
 *  - score no encontrado (cliente devuelve null)
 *  - cliente lanza excepcion
 *  - documento vacio (trampa de paquete #5)
 *  - documento null
 *
 * El `@MockBean(ScoreClient.class)` reemplaza el bean generado por
 * Micronaut con un mock para que el test no haga red.
 */
@MicronautTest
class ScoreServiceTest {

    @Inject
    ScoreService service;

    @Inject
    ScoreClient scoreClient;

    @MockBean(ScoreClient.class)
    ScoreClient scoreClientMock() {
        return mock(ScoreClient.class);
    }

    @Test
    void devuelve_score_del_cliente_externo() {
        Score s = new Score(1L, 1L, 850, "AAA", Instant.now());
        when(scoreClient.fetch("D1")).thenReturn(s);

        Optional<Score> out = service.forDocumento("D1");
        assertThat(out).isPresent();
        assertThat(out.get().valor()).isEqualTo(850);
        assertThat(out.get().categoria()).isEqualTo("AAA");
    }

    @Test
    void retorna_vacio_si_cliente_devuelve_null() {
        when(scoreClient.fetch("D2")).thenReturn(null);
        assertThat(service.forDocumento("D2")).isEmpty();
    }

    @Test
    void retorna_vacio_si_cliente_lanza_excepcion() {
        when(scoreClient.fetch("D3")).thenThrow(new RuntimeException("upstream down"));
        assertThat(service.forDocumento("D3")).isEmpty();
    }

    @Test
    void retorna_vacio_si_documento_null() {
        assertThat(service.forDocumento(null)).isEmpty();
    }

    @Test
    void retorna_vacio_si_documento_vacio_sin_error() {
        // Trampa de paquete #5: documento vacio no se valida; el cliente
        // externo recibe "" y devuelve null/404 -> Optional.empty().
        when(scoreClient.fetch("")).thenReturn(null);
        assertThat(service.forDocumento("")).isEmpty();
    }

    @Test
    void maneja_score_con_categoria_ajustada() {
        // La @Query de ScoreRepository mapea a categoria_ajustada. Aqui
        // simulamos que el cliente externo ya devuelve la categoria ajustada.
        Score s = new Score(1L, 1L, 920, "premium", Instant.now());
        when(scoreClient.fetch("D4")).thenReturn(s);

        Optional<Score> out = service.forDocumento("D4");
        assertThat(out).isPresent();
        assertThat(out.get().categoria()).isEqualTo("premium");
    }
}
