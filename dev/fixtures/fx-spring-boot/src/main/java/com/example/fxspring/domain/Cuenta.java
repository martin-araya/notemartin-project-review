// Cuenta.java
// Entidad JPA con Lombok. Trampa ecosistema #6: @Data genera
// getters, setters, equals, hashCode, toString y un constructor
// con todos los campos requeridos. El codigo fuente NO contiene
// esos metodos; la skill debe notar la anotacion.
package com.example.fxspring.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "cuentas")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Cuenta {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    @Column(nullable = false, unique = true)
    @Email
    private String email;

    @NotBlank
    @Column(nullable = false)
    private String titular;

    @Column(nullable = false)
    private BigDecimal saldo = BigDecimal.ZERO;

    @Column(nullable = false)
    private String estado = "ACTIVA";

    @Column(nullable = false, updatable = false)
    private Instant createdAt = Instant.now();
}
