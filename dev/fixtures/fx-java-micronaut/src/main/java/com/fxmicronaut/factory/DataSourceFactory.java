package com.fxmicronaut.factory;

import com.zaxxer.hikari.HikariDataSource;
import io.micronaut.context.annotation.Bean;
import io.micronaut.context.annotation.Factory;
import io.micronaut.context.annotation.Primary;
import io.micronaut.context.annotation.Requires;
import io.micronaut.context.annotation.Value;
import io.micronaut.context.env.Environment;
import jakarta.inject.Singleton;

import javax.sql.DataSource;

/**
 * Factory que expone un DataSource segun el entorno. Es la trampa del
 * ecosistema #1: el bean activo depende del entorno.
 *
 * En ``dev`` se prefiere H2 in-memory. En cualquier otro entorno se usa
 * la URL por defecto (``jdbc:h2:mem:default`` segun application.yml), o
 * la indicada por ``JDBC_URL``. Un escaner estatico no puede deducir
 * cual se inyecta; necesita conocer el perfil activo.
 */
@Factory
public class DataSourceFactory {

    @Requires(env = Environment.DEVELOPMENT)
    @Bean
    @Primary
    @Singleton
    public DataSource devDataSource(@Value("${datasources.default.url}") String url) {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl(url);
        ds.setDriverClassName("org.h2.Driver");
        ds.setUsername("sa");
        ds.setPassword("");
        ds.setMaximumPoolSize(4);
        return ds;
    }

    @Requires(notEnv = Environment.DEVELOPMENT)
    @Bean
    @Singleton
    public DataSource prodDataSource(@Value("${datasources.default.url}") String url) {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl(url);
        ds.setDriverClassName("org.h2.Driver");
        ds.setUsername("sa");
        ds.setPassword("");
        ds.setMaximumPoolSize(8);
        return ds;
    }
}
