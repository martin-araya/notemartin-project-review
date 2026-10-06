// CuentaRepository.java
// Repositorio con derived queries. Trampa ecosistema #3:
// los metodos findByEmail, findByEmailAndEstado, findByEstado
// NO tienen implementacion en el codigo fuente. Spring Data
// JPA los genera en tiempo de ejecucion a partir del nombre
// del metodo. La skill debe notar la ausencia de body.
package com.example.fxspring.repository;

import com.example.fxspring.domain.Cuenta;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface CuentaRepository extends JpaRepository<Cuenta, Long> {

    Optional<Cuenta> findByEmail(String email);

    Optional<Cuenta> findByEmailAndEstado(String email, String estado);

    Page<Cuenta> findByEstado(String estado, Pageable pageable);
}
