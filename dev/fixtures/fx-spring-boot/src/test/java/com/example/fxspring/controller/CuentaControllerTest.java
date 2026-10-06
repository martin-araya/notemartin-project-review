// tests/controller/CuentaControllerTest.java
// Tests con @WebMvcTest + MockMvc.
package com.example.fxspring.controller;

import com.example.fxspring.domain.Cuenta;
import com.example.fxspring.service.CuentaService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.util.Optional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(CuentaController.class)
class CuentaControllerTest {

    @Autowired
    private MockMvc mvc;

    @MockBean
    private CuentaService service;

    @Test
    void crear_devuelve_201_con_cuenta() throws Exception {
        when(service.crear(any(Cuenta.class))).thenAnswer(inv -> {
            Cuenta c = inv.getArgument(0);
            c.setId(1L);
            return c;
        });
        mvc.perform(post("/api/v1/cuentas")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"email\":\"a@b.c\",\"titular\":\"A\"}"))
            .andExpect(status().isCreated());
    }

    @Test
    void get_devuelve_404_si_no_existe() throws Exception {
        when(service.findById(1L)).thenReturn(Optional.empty());
        mvc.perform(get("/api/v1/cuentas/1"))
            .andExpect(status().isNotFound());
    }

    @Test
    void crear_devuelve_400_con_email_invalido() throws Exception {
        // @Valid + @Email rechaza emails sin formato.
        mvc.perform(post("/api/v1/cuentas")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"email\":\"no-es-email\",\"titular\":\"X\"}"))
            .andExpect(status().isBadRequest());
    }
}
