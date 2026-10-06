package com.fxmicronaut.controllers;

import com.fxmicronaut.domain.Cliente;
import com.fxmicronaut.domain.Score;
import com.fxmicronaut.exceptions.NotFoundClienteException;
import com.fxmicronaut.exceptions.NotFoundScoreException;
import com.fxmicronaut.repository.ClienteRepository;
import com.fxmicronaut.services.ClienteService;
import com.fxmicronaut.services.ScoreService;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.HttpStatus;
import io.micronaut.http.annotation.Body;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Error;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.http.annotation.Post;
import io.micronaut.http.exceptions.HttpStatusException;
import io.micronaut.validation.Validated;
import jakarta.validation.Valid;

/**
 * Controller de Cliente. Expone las 4 features como endpoints HTTP.
 */
@Validated
@Controller("/clientes")
public class ClienteController {

    private final ClienteService service;
    private final ClienteRepository repo;
    private final ScoreService scoreService;

    public ClienteController(ClienteService service,
                             ClienteRepository repo,
                             ScoreService scoreService) {
        this.service = service;
        this.repo = repo;
        this.scoreService = scoreService;
    }

    @Post
    public HttpResponse<Cliente> alta(@Body @Valid Cliente cliente) {
        Cliente saved = service.alta(cliente);
        return HttpResponse.created(saved);
    }

    @Get("/{id}")
    public Cliente get(@PathVariable Long id) {
        return repo.findById(id).orElseThrow(() -> new NotFoundClienteException(id));
    }

    @Get("/score")
    public Score scoreByDocumento(String documento) {
        return scoreService.forDocumento(documento)
                .orElseThrow(() -> new NotFoundScoreException(documento));
    }

    @Error(global = true, exception = NotFoundClienteException.class)
    public HttpResponse<String> handleNotFoundCliente(NotFoundClienteException e) {
        return HttpResponse.notFound(e.getMessage());
    }

    @Error(global = true, exception = NotFoundScoreException.class)
    public HttpResponse<String> handleNotFoundScore(NotFoundScoreException e) {
        return HttpResponse.notFound(e.getMessage());
    }
}
