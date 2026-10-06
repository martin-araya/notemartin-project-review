// AuditoriaRepository.java
// Dead code: existe para que AuditoriaService inyecte algo,
// pero no se usa en ningun feature activo. La app solo
// define la interfaz; JpaRepository se autogenera.
package com.example.fxspring.repository;

import com.example.fxspring.domain.Auditoria;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AuditoriaRepository extends JpaRepository<Auditoria, Long> {
}
