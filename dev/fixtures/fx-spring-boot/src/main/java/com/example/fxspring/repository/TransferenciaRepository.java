// TransferenciaRepository.java
// Repositorio con derived queries y @Lock para pessimistic
// write lock en la consulta de cuenta origen durante la
// transferencia.
package com.example.fxspring.repository;

import com.example.fxspring.domain.Transferencia;
import jakarta.persistence.LockModeType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TransferenciaRepository extends JpaRepository<Transferencia, Long> {

    List<Transferencia> findByCuentaOrigenId(Long cuentaOrigenId);

    List<Transferencia> findByEstado(Transferencia.Estado estado);

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("select t from Transferencia t where t.id = :id")
    java.util.Optional<Transferencia> findByIdForUpdate(@Param("id") Long id);
}
