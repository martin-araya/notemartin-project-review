// tests/repository/DerivedQueryTest.java
// Tests de derived queries con Testcontainers (PostgreSQL real).
// Requiere Docker daemon; si no, cae al fallback H2.
package com.example.fxspring.repository;

import com.example.fxspring.domain.Cuenta;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@ActiveProfiles("test")
@Testcontainers
class DerivedQueryTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")
        .withDatabaseName("fxdb")
        .withUsername("fx")
        .withPassword("fx");

    @DynamicPropertySource
    static void setProps(DynamicPropertyRegistry r) {
        r.add("spring.datasource.url", postgres::getJdbcUrl);
        r.add("spring.datasource.username", postgres::getUsername);
        r.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private CuentaRepository repo;

    @Test
    void findByEmail_retorna_la_cuenta_correcta() {
        Cuenta c = new Cuenta();
        c.setEmail("a@b.c");
        c.setTitular("A");
        c.setSaldo(new BigDecimal("100.00"));
        repo.save(c);

        Optional<Cuenta> found = repo.findByEmail("a@b.c");
        assertTrue(found.isPresent());
        assertEquals("a@b.c", found.get().getEmail());
    }

    @Test
    void findByEmailAndEstado_filtra_correctamente() {
        Cuenta c = new Cuenta();
        c.setEmail("act@b.c");
        c.setEstado("ACTIVA");
        repo.save(c);

        Optional<Cuenta> found = repo.findByEmailAndEstado("act@b.c", "ACTIVA");
        assertTrue(found.isPresent());

        Optional<Cuenta> notFound = repo.findByEmailAndEstado("act@b.c", "BLOQUEADA");
        assertTrue(notFound.isEmpty());
    }

    @Test
    void findByEmail_retorna_empty_si_no_existe() {
        assertTrue(repo.findByEmail("nadie@b.c").isEmpty());
    }
}
