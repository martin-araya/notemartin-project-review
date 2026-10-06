// FxSpringApplication.java
// Punto de entrada de la aplicacion Spring Boot 3.
// Trampa paquete #3: la anotacion que habilita el procesamiento
// de metodos async NO esta declarada en ninguna parte de la app.
// Si un service declara @Async, se ejecuta sincronamente (no
// falla; simplemente no hay pool de hilos async). La skill debe
// notar la falta de esta anotacion.
package com.example.fxspring;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.boot.autoconfigure.domain.EntityScan;

@SpringBootApplication
@ComponentScan(basePackages = "com.example.fxspring")
@EntityScan(basePackages = "com.example.fxspring.domain")
@EnableJpaRepositories(basePackages = "com.example.fxspring.repository")
public class FxSpringApplication {
    public static void main(String[] args) {
        SpringApplication.run(FxSpringApplication.class, args);
    }
}
