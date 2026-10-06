package com.fxmicronaut.exceptions;

public class DuplicateClienteException extends RuntimeException {
    public DuplicateClienteException(String documento) {
        super("Cliente duplicado: " + documento);
    }
}
