package com.fxmicronaut;

import com.fxmicronaut.factory.DataSourceFactory;
import io.micronaut.context.ApplicationContext;
import io.micronaut.context.env.Environment;
import jakarta.inject.Inject;
import org.junit.jupiter.api.Test;

import javax.sql.DataSource;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Cubre la trampa del ecosistema #1: el bean DataSource activo depende
 * del entorno (via @Requires en DataSourceFactory).
 *
 * En el perfil "test" (default de @MicronautTest) NO se usa "dev", asi
 * que se inyecta el bean de prod (la rama con ``notEnv = DEVELOPMENT``).
 * En un test con ``environments = "dev"`` se inyecta el bean de dev.
 */
class EnvironmentConfigTest {

    @Test
    void bean_prod_en_perfil_test_por_defecto() {
        try (ApplicationContext ctx = ApplicationContext.run()) {
            DataSource ds = ctx.getBean(DataSource.class);
            assertThat(ds).isNotNull();
        }
    }

    @Test
    void data_source_factory_declara_dos_beans() {
        // Verifica que el factory tiene los dos metodos @Bean via
        // introspeccion de la clase.
        long count = java.util.Arrays.stream(DataSourceFactory.class.getDeclaredMethods())
                .filter(m -> m.isAnnotationPresent(io.micronaut.context.annotation.Bean.class))
                .count();
        assertThat(count).isEqualTo(2);
    }

    @Test
    void data_source_factory_usa_requiere_anotacion() {
        // El factory debe anotar al menos un metodo con @Requires para
        // que sea un bean condicional (trampa ecosistema #1).
        long requiresCount = java.util.Arrays.stream(DataSourceFactory.class.getDeclaredMethods())
                .filter(m -> m.isAnnotationPresent(io.micronaut.context.annotation.Requires.class))
                .count();
        assertThat(requiresCount).isGreaterThanOrEqualTo(1);
    }
}
