// AsyncConfig.java
// Configuracion del pool de hilos async. Trampa superficial
// #3: el @Bean Executor se declara pero la property
// spring.task.execution.pool.core-size no esta en application.yml
// asi que el bean no tiene efecto (Spring usa el default).
package com.example.fxspring.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

@Configuration
public class AsyncConfig {

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(5);
        executor.setQueueCapacity(10);
        executor.setThreadNamePrefix("fx-async-");
        executor.initialize();
        return executor;
    }
}
