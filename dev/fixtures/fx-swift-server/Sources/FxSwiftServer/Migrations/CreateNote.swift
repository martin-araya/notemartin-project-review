// CreateNote.swift
// Migracion Fluent. Demuestra trampa P5: el UNIQUE index no se declara
// IF NOT EXISTS, por lo que re-ejecutar `app.migrate()` falla con
// `UNIQUE constraint failed` en SQLite.
import Fluent
import FluentSQLiteDriver

struct CreateNote: AsyncMigration {
    func prepare(on database: any Database) async throws {
        try await database.schema("notes")
            .id()
            .field("title", .string, .required)
            .field("body", .string, .required)
            .field("author_id", .string, .required)
            .field("created_at", .datetime)
            .unique(on: "title")  // trampa P5: UNIQUE no idempotente
            .create()
    }
    func revert(on database: any Database) async throws {
        try await database.schema("notes").delete()
    }
}

struct CreateAuditEntry: AsyncMigration {
    func prepare(on database: any Database) async throws {
        try await database.schema("audit_entries")
            .id()
            .field("actor", .string, .required)
            .field("action", .string, .required)
            .field("target_id", .string, .required)
            .field("created_at", .datetime)
            .create()
    }
    func revert(on database: any Database) async throws {
        try await database.schema("audit_entries").delete()
    }
}