// CuentaController.java
// REST controller con CRUD basico. Trampa superficial #1:
// el metodo listAll() esta declarado pero el SecurityFilterChain
// no expone ninguna ruta para el. La skill debe notar la
// inconsistencia entre el controller y el matcher de seguridad.
package com.example.fxspring.controller;

import com.example.fxspring.domain.Cuenta;
import com.example.fxspring.service.CuentaService;
import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/api/v1/cuentas")
public class CuentaController {

    private final CuentaService service;

    public CuentaController(CuentaService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<Cuenta> crear(@Valid @RequestBody Cuenta c) {
        return ResponseEntity.status(201).body(service.crear(c));
    }

    @GetMapping("/{id}")
    public ResponseEntity<Cuenta> get(@PathVariable Long id) {
        Optional<Cuenta> c = service.findById(id);
        return c.map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
    }

    // Trampa superficial #1: ruta declarada pero no en SecurityFilterChain.
    @GetMapping
    public ResponseEntity<Page<Cuenta>> listAll(Pageable pageable) {
        return ResponseEntity.ok(service.listar(null, pageable));
    }
}
