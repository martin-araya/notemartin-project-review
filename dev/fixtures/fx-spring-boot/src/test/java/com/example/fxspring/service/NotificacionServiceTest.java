// tests/service/NotificacionServiceTest.java
package com.example.fxspring.service;

import com.example.fxspring.domain.Notificacion;
import com.example.fxspring.repository.NotificacionRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ActiveProfiles;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@ActiveProfiles("test")
class NotificacionServiceTest {

    @Autowired
    private NotificacionService service;

    @MockBean
    private NotificacionRepository repo;

    @Test
    void enviar_retorna_notificacion_con_estado_enviado() {
        when(repo.save(any(Notificacion.class))).thenAnswer(inv -> inv.getArgument(0));
        Notificacion n = service.enviar("a@b.c", "Hola");
        assertEquals("ENVIADO", n.getEstado());
        assertEquals("a@b.c", n.getDestinatario());
    }

    @Test
    void enviar_ejecuta_sincronamente_sin_enable_async() {
        // Trampa paquete #3: sin @EnableAsync, el metodo
        // @Async se ejecuta sincronamente. Verificamos que el
        // test termina rapido, no en un hilo async.
        long t0 = System.currentTimeMillis();
        when(repo.save(any(Notificacion.class))).thenAnswer(inv -> inv.getArgument(0));
        service.enviar("a@b.c", "Hola");
        long elapsed = System.currentTimeMillis() - t0;
        assertTrue(elapsed < 1000, "debio ejecutarse sync, elapsed=" + elapsed + "ms");
    }
}
