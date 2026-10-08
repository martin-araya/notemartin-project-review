// AuditEntry.swift
// Modelo Fluent para entradas de . E4: enum AuditAction + @Field
// + migracion declarativa.
import Foundation
import Vapor
import Fluent

enum AuditAction: String, Codable, CaseIterable, Sendable {
 case create
 case update
 case delete
 case archive
 case unverified
}

final class AuditEntry: Model, Content, @unchecked Sendable {
 static let schema = "audit_entries"
 @ID(key: .id)
 var id: UUID?
 @Field(key: "actor")
 var actor: String
 @Field(key: "action")
 var actionRaw: String
 @Field(key: "target_id")
 var targetId: String
 @Timestamp(key: "created_at", on: .create)
 var createdAt: Date?
 init() {}
 init(id: UUID? = nil, actor: String, action: AuditAction, targetId: String) {
 self.id = id
 self.actor = actor
 self.actionRaw = action.rawValue
 self.targetId = targetId
 }
 var action: AuditAction {
 get { AuditAction(rawValue: actionRaw) ?? .unverified }
 set { actionRaw = newValue.rawValue }
 }
}