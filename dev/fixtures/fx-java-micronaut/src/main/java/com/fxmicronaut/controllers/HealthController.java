package com.fxmicronaut.controllers;

import io.micronaut.http.MediaType;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.Produces;

@Controller("/health")
public class HealthController {

    @Get
    @Produces(MediaType.TEXT_PLAIN)
    public String health() {
        return "UP";
    }
}
