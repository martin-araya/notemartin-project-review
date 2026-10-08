// NotesRoutes.swift
// RouteCollection Vapor para `notes`. Demuestra trampa E3 (wiring en
// boot(routes:)). El macro `@FxRoute` (trampa E1) genera automaticamente
// `registerRoute(_ app: Application)` y la property `path`. La skill debe
// notar que el cuerpo de `registerRoute` NO esta en `Sources/`.
import Vapor
import FxSwiftServer

@FxRoute
struct NotesRoutes: RouteCollection {
    typealias Result = Note
    func boot(routes: RoutesBuilder) throws {
        routes.post(use: create(_:))
        routes.get(use: list(_:))
        routes.get(":id", use: get(_:))
        routes.put(":id", use: update(_:))
        routes.delete(":id", use: delete(_:))
    }

    func create(_ req: Request) async throws -> NoteDTO {
        let dto = try req.content.decode(NoteDTO.self)
        try dto.validate()
        let service = NotesService(db: req.db)
        let note = Note(id: UUID(), title: dto.title, body: dto.body, authorId: dto.authorId)
        do {
            let saved = try await service.create(note)
            return NoteDTO(id: saved.id, title: saved.title, body: saved.body, authorId: saved.authorId)
        } catch let error as ApiError where {
            if case .conflict = error { return true } else { return false }
        }() {
            req.abort(.conflict)
        }
    }

    func list(_ req: Request) async throws -> [NoteDTO] {
        let service = NotesService(db: req.db)
        let notes = try await service.list()
        return notes.map { NoteDTO(id: $0.id, title: $0.title, body: $0.body, authorId: $0.authorId) }
    }

    func get(_ req: Request) async throws -> NoteDTO {
        guard let idStr = req.parameters.get("id"), let id = UUID(uuidString: idStr) else {
            throw ApiError.notFound(UUID())
        }
        let service = NotesService(db: req.db)
        let note = try await service.find(id)
        return NoteDTO(id: note.id, title: note.title, body: note.body, authorId: note.authorId)
    }

    func update(_ req: Request) async throws -> NoteDTO {
        guard let idStr = req.parameters.get("id"), let id = UUID(uuidString: idStr) else {
            throw ApiError.notFound(UUID())
        }
        let dto = try req.content.decode(NoteDTO.self)
        try dto.validate()
        let service = NotesService(db: req.db)
        var note = try await service.find(id)
        note.title = dto.title
        note.body = dto.body
        try await note.update(on: req.db)
        return NoteDTO(id: note.id, title: note.title, body: note.body, authorId: note.authorId)
    }

    func delete(_ req: Request) async throws -> HTTPStatus {
        guard let idStr = req.parameters.get("id"), let id = UUID(uuidString: idStr) else {
            throw ApiError.notFound(UUID())
        }
        let service = NotesService(db: req.db)
        try await service.delete(id)
        return .noContent
    }
}