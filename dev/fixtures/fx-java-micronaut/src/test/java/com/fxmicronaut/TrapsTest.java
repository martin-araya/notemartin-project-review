package com.fxmicronaut;

import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Tests que verifican la presencia y forma de las 6 trampas del ecosistema
 * (CC-06) y de las 6 trampas del paquete (CC-04) en el codigo del fixture.
 *
 * Estos tests son la version "ground-truth" de las trampas; cualquier
 * refactor que las rompa sera detectado.
 */
class TrapsTest {

    private static String read(String relativePath) throws Exception {
        Path p = Paths.get("src/main/java", relativePath);
        return Files.readString(p);
    }

    private static String readResources(String relativePath) throws Exception {
        Path p = Paths.get("src/main/resources", relativePath);
        return Files.readString(p);
    }

    // ---------- Trampas del ecosistema ----------

    @Test
    void trap_1_bean_condicional_con_requires() throws Exception {
        String src = read("com/fxmicronaut/factory/DataSourceFactory.java");
        assertThat(src).contains("@Requires");
        assertThat(src).contains("Environment.DEVELOPMENT");
        assertThat(src).contains("@Factory");
    }

    @Test
    void trap_2_client_declarativo_sin_implementacion() throws Exception {
        String src = read("com/fxmicronaut/client/ScoreClient.java");
        assertThat(src).contains("@Client");
        // Es interface, no class.
        assertThat(src).contains("public interface");
        // Solo declaracion de metodo, no hay cuerpo.
        assertThat(src).contains("Score fetch(String documento);");
    }

    @Test
    void trap_3_precedencia_yml_sobre_dev() throws Exception {
        // application.yml define defaults
        String yml = readResources("application.yml");
        // application-dev.yml define overrides
        String dev = readResources("application-dev.yml");
        // application-test.yml define overrides adicionales
        String test = readResources("application-test.yml");
        assertThat(yml).contains("base-url");
        assertThat(dev).contains("base-url: http://localhost:8081");
        assertThat(test).contains("base-url: http://localhost:0");
    }

    @Test
    void trap_4_event_publisher_y_listener_desacoplados() throws Exception {
        String publisher = read("com/fxmicronaut/services/ClienteService.java");
        String listener = read("com/fxmicronaut/services/NotifierService.java");
        String scheduler = read("com/fxmicronaut/scheduler/DailyCloseScheduler.java");
        // Emisores
        assertThat(publisher).contains("ApplicationEventPublisher");
        assertThat(scheduler).contains("ApplicationEventPublisher");
        // Receptor
        assertThat(listener).contains("@EventListener");
        // El receptor no menciona directamente al emisor.
        assertThat(listener).doesNotContain("ClienteService");
        assertThat(listener).doesNotContain("DailyCloseScheduler");
    }

    @Test
    void trap_5_scheduled_con_cron_externo() throws Exception {
        String src = read("com/fxmicronaut/scheduler/DailyCloseScheduler.java");
        assertThat(src).contains("@Scheduled");
        // La expresion es una property, no un literal.
        assertThat(src).contains("cron = \"${daily-close.cron}\"");
    }

    @Test
    void trap_6_columna_agregada_por_flyway_en_v2() throws Exception {
        // La migracion V2 crea la tabla con la columna categoria_ajustada.
        String v2 = readResources("db/migration/V2__add_score_extra.sql");
        assertThat(v2).contains("categoria_ajustada");
        // ScoreRepository consume la columna en una @Query nativa.
        String repo = read("com/fxmicronaut/repository/ScoreRepository.java");
        assertThat(repo).contains("@Query");
        assertThat(repo).contains("categoria_ajustada");
    }

    // ---------- Trampas del paquete ----------

    @Test
    void package_trap_1_timeout_ms_cero_es_sin_timeout() throws Exception {
        String src = read("com/fxmicronaut/config/ScoreClientConfig.java");
        // El record valida que timeoutMs <= 0 queda en 0 (sin timeout).
        assertThat(src).contains("if (timeoutMs <= 0)");
        assertThat(src).contains("timeoutMs = 0");
    }

    @Test
    void package_trap_2_publisher_swallows_errors() throws Exception {
        String src = read("com/fxmicronaut/services/ClienteService.java");
        // El try/catch alrededor de publisher.publishEvent traga los
        // errores de Notifier.
        assertThat(src).contains("try {");
        assertThat(src).contains("publisher.publishEvent");
        assertThat(src).contains("} catch (RuntimeException re) {");
    }

    @Test
    void package_trap_3_sin_transaccional_en_alta() throws Exception {
        String src = read("com/fxmicronaut/services/ClienteService.java");
        // El metodo alta NO es @Transactional (race condition entre
        // findByDocumento y save).
        assertThat(src).contains("public Cliente alta(");
        assertThat(src).doesNotContain("@Transactional");
    }

    @Test
    void package_trap_4_scheduler_retorna_si_disabled() throws Exception {
        String src = read("com/fxmicronaut/scheduler/DailyCloseScheduler.java");
        assertThat(src).contains("if (!config.enabled())");
        assertThat(src).contains("return;");
    }

    @Test
    void package_trap_5_sin_validacion_documento_vacio() throws Exception {
        String src = read("com/fxmicronaut/services/ScoreService.java");
        // No hay check de documento == "" o documento.isBlank().
        // El catch RuntimeException tampoco se distingue entre tipos.
        assertThat(src).doesNotContain("isBlank()");
        assertThat(src).doesNotContain("isEmpty()");
    }

    @Test
    void package_trap_6_listener_lazy_via_di() throws Exception {
        // El @EventListener se invoca en el primer evento, no al
        // arranque. No hay bean de inicializacion.
        String src = read("com/fxmicronaut/services/NotifierService.java");
        assertThat(src).contains("@EventListener");
        // No hay metodo @PostConstruct ni @Context.
        assertThat(src).doesNotContain("@PostConstruct");
    }
}
