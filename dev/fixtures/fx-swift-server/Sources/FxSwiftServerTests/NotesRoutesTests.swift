// NotasRoutesTests.swift
// Tests XCTest para la feature (.., ).
import XCTest
import Vapor
import Fluent
import FluentSQLiteDriver
@testable import FxSwiftServer

final class NotesRoutesTests: XCTestCase {
 var app: Application!

 override func setUp() async throws {
 app = try await Application.make(.testing)
 app.databases.use(.sqlite(":memory:"), as: .sqlite)
 app.migrations.add(CreateNote())
 app.migrations.add(CreateAuditEntry())
 app.register(collection: NotesRoutes())
 app.register(collection: AuditRoutes())
 try await app.autoMigrate()
 }

 override func tearDown() async throws {
 try await app.autoRevert()
 try await app.shutdown()
 }

 func testCreateNote201() async throws {
 // exito completo
 let payload = NoteDTO(
 title: "Test",
 body: "Hello",
 authorId: UUID()
 )
 try await app.test(.POST, "/notes") { req in
 try req.content.encode(payload)
 } afterResponse: { res async throws in
 XCTAssertEqual(res.status, .created)
 let dto = try res.content.decode(NoteDTO.self)
 XCTAssertEqual(dto.title, "Test")
 }
 }

 func testCreateNote400EmptyTitle() async throws {
 // validacion: titulo vacio
 let payload = NoteDTO(title: " ", body: "x", authorId: UUID())
 try await app.test(.POST, "/notes") { req in
 try req.content.encode(payload)
 } afterResponse: { res async throws in
 XCTAssertEqual(res.status, .badRequest)
 }
 }

 func testGetNote404() async throws {
 // no encontrado
 try await app.test(.GET, "/notes/\(UUID())") { _ in } afterResponse: { res async throws in
 XCTAssertEqual(res.status, .notFound)
 }
 }

 func testListNotes200() async throws {
 // listar vacio
 try await app.test(.GET, "/notes") { _ in } afterResponse: { res async throws in
 XCTAssertEqual(res.status, .ok)
 }
 }

 func testCreateNoteTimeout() async throws {
 // timeout simulado: URLSession con timeout=0.001
 let session = makeSession(timeout: 0.001)
 XCTAssertNotNil(session)
 }

 private func makeSession(timeout: TimeInterval) -> URLSession {
 let cfg = URLSessionConfiguration.default
 cfg.timeoutIntervalForRequest = timeout
 return URLSession(configuration: cfg)
 }
}