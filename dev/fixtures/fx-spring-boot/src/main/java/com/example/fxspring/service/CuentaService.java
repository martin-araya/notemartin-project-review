// CuentaService.java
// Service con @Transactional a nivel de clase. Trampa paquete
// #1: el read-only findByEmailCached hereda la transaccion
// aunque no deberia. La skill debe notar la diferencia entre
// @Transactional(readOnly = true) y @Transactional a nivel de
// clase.
package com.example.fxspring.service;

import com.example.fxspring.domain.Cuenta;
import com.example.fxspring.repository.CuentaRepository;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.Optional;

@Service
@Transactional
public class CuentaService {

    private final CuentaRepository repo;

    public CuentaService(CuentaRepository repo) {
        this.repo = repo;
    }

    public Cuenta crear(Cuenta c) {
        if (repo.findByEmail(c.getEmail()).isPresent()) {
            throw new IllegalStateException("email duplicado: " + c.getEmail());
        }
        c.setSaldo(c.getSaldo() == null ? BigDecimal.ZERO : c.getSaldo());
        return repo.save(c);
    }

    public Optional<Cuenta> findById(Long id) {
        return repo.findById(id);
    }

    // Trampa paquete #2: @Cacheable sin condicion de null.
    // Si el email no existe, devuelve null y el cache guarda null.
    // La skill debe notar que Spring Cache guarda Optional.empty()
    // en algunos casos pero null literal en otros, dependiendo
    // del CacheManager.
    @Cacheable(value = "cuentas", key = "#email")
    public Optional<Cuenta> findByEmailCached(String email) {
        return repo.findByEmail(email);
    }

    public Page<Cuenta> listar(String estado, Pageable pageable) {
        if (estado == null) return repo.findAll(pageable);
        return repo.findByEstado(estado, pageable);
    }
}
