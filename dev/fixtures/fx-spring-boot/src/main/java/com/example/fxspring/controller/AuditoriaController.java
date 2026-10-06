// AuditoriaController.java
// Trampa superficial #2: la ruta de logs NO tiene
// @PreAuthorize("hasRole('ADMIN')"). Cualquier usuario
// autenticado puede leerla. La skill debe notar la falta del
// guard a nivel de metodo.
package com.example.fxspring.controller;

import com.example.fxspring.domain.Auditoria;
import com.example.fxspring.repository.AuditoriaRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/logs")
public class AuditoriaController {

    private final AuditoriaRepository repo;

    public AuditoriaController(AuditoriaRepository repo) {
        this.repo = repo;
    }

    // Trampa superficial #2: deberia ser @PreAuthorize("hasRole('ADMIN')")
    // pero no lo es. La skill debe notar la inconsistencia con
    // el matcher del SecurityFilterChain (que tiene la regla
    // hasRole(ADMIN) para esta ruta) que el bean cubre.
    // En la realidad, ambos matcher se aplican y la app devuelve
    // 403; sin embargo, si alguien quita la regla del
    // SecurityFilterChain, este metodo queda accesible.
    @GetMapping
    public List<Auditoria> listar() {
        return repo.findAll();
    }
}
