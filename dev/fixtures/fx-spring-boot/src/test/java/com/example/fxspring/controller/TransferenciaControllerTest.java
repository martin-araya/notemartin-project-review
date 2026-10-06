// tests/controller/TransferenciaControllerTest.java
package com.example.fxspring.controller;

import com.example.fxspring.domain.Transferencia;
import com.example.fxspring.service.TransferenciaService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(TransferenciaController.class)
class TransferenciaControllerTest {

    @Autowired
    private MockMvc mvc;

    @MockBean
    private TransferenciaService service;

    @Test
    void crear_devuelve_201() throws Exception {
        when(service.crear(any(), any(), any())).thenAnswer(inv -> {
            Transferencia t = new Transferencia();
            t.setId(1L);
            return t;
        });
        mvc.perform(post("/api/v1/transferencias")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"cuentaOrigenId\":1,\"cuentaDestinoId\":2,\"monto\":100}"))
            .andExpect(status().isCreated());
    }

    @Test
    void confirmar_devuelve_200() throws Exception {
        when(service.confirmar(any())).thenAnswer(inv -> {
            Transferencia t = new Transferencia();
            t.setId(1L);
            t.setEstado(Transferencia.Estado.COMPLETADA);
            return t;
        });
        mvc.perform(patch("/api/v1/transferencias/1/confirmar"))
            .andExpect(status().isOk());
    }

    @Test
    void cancelar_devuelve_204() throws Exception {
        mvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
            .delete("/api/v1/transferencias/1"))
            .andExpect(status().isNoContent());
    }
}
