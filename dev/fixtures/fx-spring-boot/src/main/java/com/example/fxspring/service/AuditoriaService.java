// Service que persiste registros de trazabilidad. Se invoca desde
// el evento TransferenciaRealizadaEvent del modulo principal.
package com.example.fxspring.service;

import com.example.fxspring.domain.Auditoria;
import com.example.fxspring.repository.AuditoriaRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuditoriaService {

    private final AuditoriaRepository repo;

    public AuditoriaService(AuditoriaRepository repo) {
        this.repo = repo;
    }

    // Trampa paquete #5: la excepcion de lock optimista NO se
    // maneja aqui. Si dos requests concurrentes intentan crear el
    // mismo registro, el segundo hace upsert silencioso.
    @Transactional
    public Auditoria registrar(String accion, String entidad, String entidadId, String usuarioId) {
        Auditoria a = new Auditoria();
        a.setAccion(accion);
        a.setEntidad(entidad);
        a.setEntidadId(entidadId);
        a.setUsuarioId(usuarioId);
        return repo.save(a);
    }
}
