package com.fxmicronaut.exceptions;

public class NotFoundScoreException extends RuntimeException {
    public NotFoundScoreException(String documento) {
        super("Score no encontrado para documento: " + documento);
    }
}
