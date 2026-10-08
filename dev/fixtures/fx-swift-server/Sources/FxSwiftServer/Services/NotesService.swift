// NotesService.swift
// Actor que envuelve Fluent para evitar races (E5).
import Foundation
import Vapor
import Fluent

actor NotesService {
    private let db: any Database
    init(db: any Database) {
        self.db = db
    }
    func create(_ note: Note) async throws -> Note {
        try await note.save(on: db)
        return note
    }
    func find(_ id: UUID) async throws -> Note {
        guard let note = try await Note.find(id, on: db) else {
            throw ApiError.notFound(id)
        }
        return note
    }
    func delete(_ id: UUID) async throws {
        let note = try await find(id)
        try await note.delete(on: db)
    }
    func list() async throws -> [Note] {
        try await Note.query(on: db).all()
    }
}