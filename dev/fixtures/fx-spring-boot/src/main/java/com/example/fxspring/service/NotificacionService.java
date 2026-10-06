// NotificacionService.java
// Service que persiste registros de avisos. Trampa paquete
// #3: el metodo esta anotado @Async pero la app no tiene
// @EnableAsync, asi que se ejecuta sincronamente y bloquea
// el hilo HTTP del controller. La skill debe notar la
// falta de @EnableAsync.
package com.example.fxspring.service;

import com.example.fxspring.domain.Notificacion;
import com.example.fxspring.repository.NotificacionRepository;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class NotificacionService {

    private final NotificacionRepository repo;

    public NotificacionService(NotificacionRepository repo) {
        this.repo = repo;
    }

    @Async
    @Transactional
    public Notificacion enviar(String destinatario, String mensaje) {
        Notificacion n = new Notificacion();
        n.setDestinatario(destinatario);
        n.setMensaje(mensaje);
        n.setEstado("ENVIADO");
        // Dead store: la app no envia email real, solo persiste.
        return repo.save(n);
    }
}
