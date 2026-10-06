package com.fxmicronaut.exceptions;

public class NotFoundClienteException extends RuntimeException {
    public NotFoundClienteException(Long id) {
        super("Cliente no encontrado: " + id);
    }
}
