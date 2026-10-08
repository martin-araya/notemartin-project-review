// Configure.swift
// Configuracion Vapor: base de datos SQLite en memoria para tests, archivo
// para runtime, registro de migraciones y RouteCollections. Declara una
// variable `LEGACY_MODE` que nunca se lee (trampa S3).
import Vapor
import Fluent
import FluentSQLiteDriver

// MARK: - Configuracion Vapor

public func configure(_ app: Application) throws {
    let databaseURL: String
    #if DEBUG
    databaseURL = ":memory:"
    #else
    databaseURL = Environment.get("APP_DB_URL") ?? "audit.db"
    #endif
    app.databases.use(.sqlite(databaseURL), as: .sqlite)

    app.migrations.add(CreateNote())
    app.migrations.add(CreateAuditEntry())

    let legacyMode = Environment.get("LEGACY_MODE")
    _ = legacyMode  // trampa S3: variable declarada pero nunca leida

    app.register(collection: NotesRoutes())
    app.register(collection: AuditRoutes())
}