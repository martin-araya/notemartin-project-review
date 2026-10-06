package com.fxmicronaut.client;

import com.fxmicronaut.domain.Score;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.client.annotation.Client;

/**
 * Cliente HTTP declarativo: la interfaz no tiene implementacion en el codigo
 * fuente. Micronaut genera el proxy en tiempo de compilacion a partir de
 * las anotaciones (@Client + @Get).
 *
 * Trampa del ecosistema #2: el scanner que busca ``class implements
 * ScoreClient`` no encuentra nada; debe leer las anotaciones y razonar
 * sobre el proxy generado.
 *
 * El ``${score.client.base-url}`` se resuelve contra application.yml.
 */
@Client("${score.client.base-url}")
public interface ScoreClient {

    @Get("/score?documento={documento}")
    Score fetch(String documento);
}
