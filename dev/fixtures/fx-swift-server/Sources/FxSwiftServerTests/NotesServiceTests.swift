// NotesServiceTests.swift
// Tests para el actor NotesService.
import XCTest
import Vapor
import Fluent
import FluentSQLiteDriver
@testable import FxSwiftServer

final class NotesServiceTests: XCTestCase {
    func testFindThrowsNotFound() async throws {
        let service = NotesService(db: NoopDBStub())
        do {
            _ = try await service.find(UUID())
            XCTFail("deberia lanzar ApiError.notFound")
        } catch let e as ApiError {
            switch e {
            case .notFound: break
            default: XCTFail("error inesperado: \(e)")
            }
        } catch {
            XCTFail("tipo de error inesperado: \(error)")
        }
    }
}

struct NoopDBStub: Database {
    var eventLoop: any EventLoop { EmbeddedEventLoop() }
    var history: any DatabaseQueryHistory { StubHistory() }
    var logger: Logger { Logger(label: "noop") }
    func execute<E>(_ query: E, onRow: @escaping (any DatabaseRow) -> Void) where E: DatabaseQuery { }
    func execute(_ schema: any DatabaseSchema) -> any EventLoopFuture<Void> { eventLoop.makeSucceededFuture(()) }
    func execute<E>(_ query: E) -> any EventLoopFuture<Void> where E: DatabaseQuery { eventLoop.makeSucceededFuture(()) }
}

struct StubHistory: DatabaseQueryHistory { func append<E>(_ query: E) where E: DatabaseQuery { } }