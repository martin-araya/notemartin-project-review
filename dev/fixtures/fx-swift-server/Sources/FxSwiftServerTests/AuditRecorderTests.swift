// AuditRecorderTests.swift
// Tests para AuditRecorder actor ( de + trampa P3 silenciosa).
import XCTest
import Vapor
import Fluent
import FluentSQLiteDriver
@testable import FxSwiftServer

final class AuditRecorderTests: XCTestCase {
 func testRecordSuccess() async throws {
 let recorder = AuditRecorder(db: NoopDB())
 let ok = await recorder.record(actor: "u1", action: .create, targetId: "n1")
 XCTAssertTrue(ok)
 }

 func testRecordFailSwallowed() async throws {
 let recorder = AuditRecorder(db: FailingDB())
 let ok = await recorder.record(actor: "u1", action: .create, targetId: "n1")
 // trampa P3: error tragado -> ok=false pero no throw
 XCTAssertFalse(ok)
 }

 func testRecordActorEmpty() async throws {
 // : actor vacio -> 400
 let recorder = AuditRecorder(db: NoopDB())
 let ok = await recorder.record(actor: "", action: .create, targetId: "n1")
 XCTAssertFalse(ok)
 }
}

// MARK: - DB dummies

struct NoopDB: Database {
 var eventLoop: any EventLoop { EmbeddedEventLoop() }
 var history: any DatabaseQueryHistory { HistoryStub() }
 var logger: Logger { Logger(label: "noop") }
 func execute<E>(query: E, onRow: @escaping (any DatabaseRow) -> Void) where E: DatabaseQuery { }
 func execute(_ schema: any DatabaseSchema) -> any EventLoopFuture<Void> { eventLoop.makeSucceededFuture(()) }
 func execute<E>(query: E) -> any EventLoopFuture<Void> where E: DatabaseQuery { eventLoop.makeSucceededFuture(()) }
}

struct FailingDB: Database {
 var eventLoop: any EventLoop { EmbeddedEventLoop() }
 var history: any DatabaseQueryHistory { HistoryStub() }
 var logger: Logger { Logger(label: "failing") }
 func execute<E>(query: E, onRow: @escaping (any DatabaseRow) -> Void) where E: DatabaseQuery {
 throw TestError.databaseFailure("forced fail")
 }
 func execute(_ schema: any DatabaseSchema) -> any EventLoopFuture<Void> { eventLoop.makeFailedFuture(TestError.databaseFailure("forced fail")) }
 func execute<E>(query: E) -> any EventLoopFuture<Void> where E: DatabaseQuery { eventLoop.makeFailedFuture(TestError.databaseFailure("forced fail")) }
}

enum TestError: Error { case databaseFailure(String) }
struct HistoryStub: DatabaseQueryHistory { func append<E>(query: E) where E : DatabaseQuery { } }