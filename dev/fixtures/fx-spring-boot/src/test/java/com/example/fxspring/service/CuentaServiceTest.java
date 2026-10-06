// tests/service/CuentaServiceTest.java
// Tests runtime de CuentaService con @SpringBootTest.
// Requiere Maven para correr; los tests de traps_* son estaticos
// y validan la estructura sin levantar el context.
package com.example.fxspring.service;

import com.example.fxspring.domain.Cuenta;
import com.example.fxspring.repository.CuentaRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@SpringBootTest
@ActiveProfiles("test")
class CuentaServiceTest {

    @Autowired
    private CuentaService service;

    @MockBean
    private CuentaRepository repo;

    @Test
    void crear_devuelve_cuenta_con_saldo_cero() {
        when(repo.findByEmail("a@b.c")).thenReturn(Optional.empty());
        when(repo.save(any(Cuenta.class))).thenAnswer(inv -> inv.getArgument(0));

        Cuenta c = new Cuenta();
        c.setEmail("a@b.c");
        c.setTitular("A");
        Cuenta saved = service.crear(c);
        assertEquals("a@b.c", saved.getEmail());
        assertEquals(0, saved.getSaldo().compareTo(BigDecimal.ZERO));
    }

    @Test
    void crear_falla_con_email_duplicado() {
        when(repo.findByEmail("dup@b.c")).thenReturn(Optional.of(new Cuenta()));
        Cuenta c = new Cuenta();
        c.setEmail("dup@b.c");
        assertThrows(IllegalStateException.class, () -> service.crear(c));
    }

    @Test
    void findByEmailCached_retorna_empty_si_no_existe() {
        when(repo.findByEmail("no@b.c")).thenReturn(Optional.empty());
        assertTrue(service.findByEmailCached("no@b.c").isEmpty());
    }
}
