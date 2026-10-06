package com.fxmicronaut.services;

import com.fxmicronaut.client.ScoreClient;
import com.fxmicronaut.domain.Score;
import jakarta.inject.Singleton;

import java.util.Optional;

/**
 * Servicio que expone la consulta de score.
 *
 * Trampa de paquete #5: ``forDocumento("")`` no valida y retorna
 * ``Optional.empty()`` sin error visible al caller.
 */
@Singleton
public class ScoreService {

    private final ScoreClient client;

    public ScoreService(ScoreClient client) {
        this.client = client;
    }

    public Optional<Score> forDocumento(String documento) {
        // Trampa de paquete #5: no validamos que ``documento`` no este vacio.
        // Un documento vacio cae al cliente externo, devuelve 404, y el
        // caller obtiene ``Optional.empty()`` sin explicacion.
        if (documento == null) {
            return Optional.empty();
        }
        try {
            Score s = client.fetch(documento);
            return Optional.ofNullable(s);
        } catch (RuntimeException re) {
            return Optional.empty();
        }
    }
}
