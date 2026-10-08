// Note.swift
// Modelo Fluent para `notes`. Demuestra:
//  - E4: @Field + @Parent + @Timestamp
//  - @ID(UUID.self) autogenerado
//  - static let schema
//  - toParameter y preparation de migracion en CreateNote.swift
import Foundation
import Vapor
import Fluent

final class Note: Model, Content, @unchecked Sendable {
    static let schema = "notes"
    @ID(key: .id)
    var id: UUID?
    @Field(key: "title")
    var title: String
    @Field(key: "body")
    var body: String
    @Parent(key: "author_id")
    var authorId: UUID
    @Timestamp(key: "created_at", on: .create)
    var createdAt: Date?
    init() {}
    init(id: UUID? = nil, title: String, body: String, authorId: UUID) {
        self.id = id
        self.title = title
        self.body = body
        self.authorId = authorId
    }
}