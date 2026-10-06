plugins {
    java
    application
    id("io.micronaut.application") version "4.4.3"
}

group = "com.fxmicronaut"
version = "1.0.0"

repositories {
    mavenCentral()
}

val micronautVersion = "4.4.3"

dependencies {
    // Runtime
    implementation("io.micronaut:micronaut-http-validation:$micronautVersion")
    implementation("io.micronaut:micronaut-http-server-netty")
    implementation("io.micronaut:micronaut-http-client")
    implementation("io.micronaut:micronaut-jackson-databind")
    implementation("io.micronaut.serde:micronaut-serde-jackson")
    implementation("io.micronaut.validation:micronaut-validation")
    implementation("io.micronaut.data:micronaut-data-jdbc")
    implementation("io.micronaut.sql:micronaut-jdbc-hikari")
    implementation("io.micronaut.flyway:micronaut-flyway")
    implementation("org.flywaydb:flyway-core")
    implementation("ch.qos.logback:logback-classic")
    implementation("jakarta.annotation:jakarta.annotation-api")
    runtimeOnly("org.yaml:snakeyaml")

    // Runtime only - H2 (usado en tests; tambien queda disponible si se ejecuta
    // la app en modo dev sin Postgres).
    runtimeOnly("com.h2database:h2")

    // Test
    testImplementation("io.micronaut.test:micronaut-test-junit5")
    testImplementation("org.junit.jupiter:junit-jupiter-api")
    testImplementation("org.junit.jupiter:junit-jupiter-engine")
    testImplementation("org.mockito:mockito-core:5.11.0")
    testImplementation("org.assertj:assertj-core:3.25.3")
}

application {
    mainClass.set("com.fxmicronaut.Application")
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

micronaut {
    runtime("netty")
    testRuntime("junit5")
    processing {
        incremental(true)
        annotations("com.fxmicronaut.*")
    }
}

tasks.named<Test>("test") {
    useJUnitPlatform()
    // Mostrar summary claro en CI
    testLogging {
        events("passed", "skipped", "failed")
        showStandardStreams = false
        exceptionFormat = org.gradle.api.tasks.testing.logging.TestExceptionFormat.FULL
    }
}
