// DatabaseConfig.java
// Config bean con @ConditionalOnProperty. Trampa ecosistema #1:
// el bean solo se crea si app.db.url tiene havingValue "postgres".
// En dev (perfil dev) no se establece esa property, asi que el
// bean no se crea y la app usa H2 por default.
package com.example.fxspring.config;

import com.zaxxer.hikari.HikariDataSource;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.Profile;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;

import javax.sql.DataSource;

@Configuration
public class DatabaseConfig {

    @Bean
    @Primary
    @ConditionalOnProperty(name = "app.db.url", havingValue = "postgres")
    @ConfigurationProperties("spring.datasource")
    public DataSource postgresDataSource() {
        return DataSourceBuilder.create().type(HikariDataSource.class).build();
    }

    // Dead method: nunca se invoca. La trampa superficial #3
    // menciona que el @Bean Executor declarado en AsyncConfig
    // nunca se usa porque la property spring.task.execution.pool
    // no esta configurada en application.yml.
    @Bean
    @Profile("prod")
    public String productionMarker() {
        return "prod";
    }
}
