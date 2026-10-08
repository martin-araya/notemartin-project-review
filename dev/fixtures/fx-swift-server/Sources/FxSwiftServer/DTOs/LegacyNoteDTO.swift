// LegacyNoteDTO.swift
// DTO que rompe `Sendable` deliberadamente (trampa P2): un `class` con
// `@unchecked Sendable` y un `var` mutable compartido. Simula el caso
// donde alguien usa un type mutable como DTO entre tareas concurrentes.
import Foundation

final class LegacyNoteDTO: Content, @unchecked Sendable {
    var id: UUID?
    var title: String
    var body: String
    var authorId: UUID
    init(id: UUID? = nil, title: String, body: String, authorId: UUID) {
        self.id = id
        self.title = title
        self.body = body
        self.authorId = authorId
    }
}