// AuditRecorder.swift
// Actor `Sendable` con un metodo `record(...)` que traga el error con `try?`
// (trampa P3): la entry NO se persiste y el caller recibe un `Bool` false.
// Esto oculta errores de DB a la , dejando el sistema inconsistente.
import Foundation
import Vapor
import Fluent

actor AuditRecorder {
 private let db: any Database
 init(db: any Database) {
 self.db = db
 }
 /// Devuelve `true` si la entry se persistio, `false` si se trago el error.
 func record(actor: String, action: AuditAction, targetId: String) async -> Bool {
 let entry = AuditEntry(actor: actor, action: action, targetId: targetId)
 do {
 try await entry.save(on: db)
 return true
 } catch {
 // Trampa P3: el error se silencia con try?.
 return false
 }
 }
}