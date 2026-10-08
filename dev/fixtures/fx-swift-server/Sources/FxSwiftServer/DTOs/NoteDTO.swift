// NoteDTO.swift
// DTO `Sendable struct` (modelo de concurrencia Swift 6, trampa E5).
import Foundation
import Vapor

struct NoteDTO: Codable, Content, Sendable {
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
    func validate() throws {
        if title.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            throw ApiError.titleRequired
        }
        if body.count > 1024 {
            throw ApiError.bodyTooLong
        }
    }
}