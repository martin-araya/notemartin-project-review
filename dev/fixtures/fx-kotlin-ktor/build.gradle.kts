// build.gradle.kts
// Configuracion de Gradle (Kotlin DSL) para fx-kotlin-ktor.
// Trampa ecosistema #2: los plugins se instalan en orden
// especifico. auth() antes que routing() asegura que el
// AuthenticationProvider este disponible para las rutas.
val ktorVersion = "3.0.1"
val koinVersion = "4.0.0"
val exposedVersion = "1.0.0-beta01"
val coroutinesVersion = "1.8.1"
val serializationVersion = "1.7.3"
val junitVersion = "5.10.2"

plugins {
    kotlin("jvm") version "2.0.21"
    kotlin("plugin.serialization") version "2.0.21"
    application
    id("org.jetbrains.kotlin.plugin.allopen") version "2.0.21"
}

group = "com.example"
version = "1.0.0"

application {
    mainClass.set("com.example.fxktor.FxKtorApplicationKt")
}

repositories {
    mavenCentral()
}

dependencies {
    // Ktor server
    implementation("io.ktor:ktor-server-core-jvm:$ktorVersion")
    implementation("io.ktor:ktor-server-netty-jvm:$ktorVersion")
    implementation("io.ktor:ktor-server-content-negotiation-jvm:$ktorVersion")
    implementation("io.ktor:ktor-server-status-pages-jvm:$ktorVersion")
    implementation("io.ktor:ktor-server-call-logging-jvm:$ktorVersion")
    implementation("io.ktor:ktor-server-auth-jvm:$ktorVersion")
    implementation("io.ktor:ktor-serialization-kotlinx-json-jvm:$ktorVersion")

    // Koin DI
    implementation("io.insert-koin:koin-ktor:$koinVersion")
    implementation("io.insert-koin:koin-core:$koinVersion")
    implementation("io.insert-koin:koin-logger-slf4j:$koinVersion")

    // Exposed (persistencia)
    implementation("org.jetbrains.exposed:exposed-core:$exposedVersion")
    implementation("org.jetbrains.exposed:exposed-jdbc:$exposedVersion")
    implementation("org.jetbrains.exposed:exposed-java-time:$exposedVersion")

    // Coroutines + serializacion
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:$coroutinesVersion")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:$serializationVersion")

    // DB drivers
    implementation("com.h2database:h2:2.2.224")
    implementation("org.flywaydb:flyway-core:10.10.0")
    implementation("ch.qos.logback:logback-classic:1.5.6")

    // Tests
    testImplementation("io.ktor:ktor-server-test-host-jvm:$ktorVersion")
    testImplementation("io.insert-koin:koin-test:$koinVersion")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5:$junitVersion")
    testImplementation("org.junit.jupiter:junit-jupiter:$junitVersion")
}

tasks.test {
    useJUnitPlatform()
    testLogging {
        events("passed", "skipped", "failed")
        showStandardStreams = true
    }
}

kotlin {
    jvmToolchain(21)
}
