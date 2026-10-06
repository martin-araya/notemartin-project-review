// TransferenciaController.java
// REST controller. Trampa paquete #4: @PreAuthorize con SpEL
// "#id == authentication.principal.id" no valida que el id
// del path pertenezca al usuario autenticado. La trampa es
// que authentication.principal.id no es el id de la
// transferencia sino el del usuario (un Long para userId),
// asi que un usuario podria cancelar cualquier transferencia
// que coincida con su propio userId (lo cual es improbable).
package com.example.fxspring.controller;

import com.example.fxspring.domain.Transferencia;
import com.example.fxspring.service.TransferenciaService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/transferencias")
public class TransferenciaController {

    private final TransferenciaService service;

    public TransferenciaController(TransferenciaService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<Transferencia> crear(@RequestBody Map<String, Object> body) {
        Long origenId = Long.valueOf(body.get("cuentaOrigenId").toString());
        Long destinoId = Long.valueOf(body.get("cuentaDestinoId").toString());
        BigDecimal monto = new BigDecimal(body.get("monto").toString());
        return ResponseEntity.status(201).body(service.crear(origenId, destinoId, monto));
    }

    @PatchMapping("/{id}/confirmar")
    public ResponseEntity<Transferencia> confirmar(@PathVariable Long id) {
        return ResponseEntity.ok(service.confirmar(id));
    }

    // Trampa paquete #4: SpEL incorrecta. Cualquier usuario
    // autenticado puede cancelar cualquier transferencia.
    @DeleteMapping("/{id}")
    @PreAuthorize("#id == authentication.principal.id")
    public ResponseEntity<Void> cancelar(@PathVariable Long id) {
        // No implementado: la cancelacion real no existe.
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/origen/{cuentaOrigenId}")
    public ResponseEntity<List<Transferencia>> listarPorOrigen(@PathVariable Long cuentaOrigenId) {
        return ResponseEntity.ok(service.listarPorOrigen(cuentaOrigenId));
    }
}
