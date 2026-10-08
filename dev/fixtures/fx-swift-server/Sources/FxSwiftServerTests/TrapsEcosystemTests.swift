// TrapsEcosystemTests.swift
// 6 tests que verifican que cada trampa del ecosistema E1..E6 esta plantada
// en el fixture.
import XCTest
import Vapor
import Fluent
import FluentSQLiteDriver
@testable import FxSwiftServer

final class TrapsEcosystemTests: XCTestCase {
    func testE1MacrosAttached() {
        // E1: macros `@attached(member)` viven en FxSwiftMacros, no en FxSwiftServer.
        let macroSource = readFixtureFile("Sources/FxSwiftMacros/RouteMacro.swift")
        XCTAssertTrue(macroSource.contains("PeerMacro") || macroSource.contains("attached"))
    }

    func testE2BuildPluginExists() {
        // E2: build tool plugin AuditCodesPlugin existe en Plugins/AuditCodesPlugin.
        let pluginSource = readFixtureFile("Plugins/AuditCodesPlugin/Plugins/AuditCodesPlugin.swift")
        XCTAssertTrue(pluginSource.contains("BuildToolPlugin"))
        XCTAssertTrue(pluginSource.contains("createBuildCommands"))
    }

    func testE3RouteCollectionBoot() {
        // E3: RouteCollection con boot(routes:) registrado en configure.
        let notesSource = readFixtureFile("Sources/FxSwiftServer/Routes/NotesRoutes.swift")
        XCTAssertTrue(notesSource.contains("RouteCollection"))
        XCTAssertTrue(notesSource.contains("func boot(routes:"))
    }

    func testE4FluentModels() {
        // E4: modelos Fluent con @Field/@Parent/@Timestamp.
        let noteSource = readFixtureFile("Sources/FxSwiftServer/Models/Note.swift")
        XCTAssertTrue(noteSource.contains("@Field"))
        XCTAssertTrue(noteSource.contains("@Parent"))
        XCTAssertTrue(noteSource.contains("@Timestamp"))
        XCTAssertTrue(noteSource.contains("static let schema"))
    }

    func testE5SendableConcurrency() {
        // E5: actor + DTO Sendable struct.
        let recorderSource = readFixtureFile("Sources/FxSwiftServer/Services/AuditRecorder.swift")
        let dtoSource = readFixtureFile("Sources/FxSwiftServer/DTOs/NoteDTO.swift")
        XCTAssertTrue(recorderSource.contains("actor"))
        XCTAssertTrue(dtoSource.contains("Sendable"))
    }

    func testE6CanImportFoundationNetworking() {
        // E6: #if canImport(FoundationNetworking) en UrlSessionProvider.
        let urlSource = readFixtureFile("Sources/FxSwiftServer/Services/UrlSessionProvider.swift")
        XCTAssertTrue(urlSource.contains("#if canImport(FoundationNetworking)"))
        XCTAssertTrue(urlSource.contains("#endif"))
    }

    private func readFixtureFile(_ path: String) -> String {
        let fixtureRoot = ProcessInfo.processInfo.environment["FIXTURE_ROOT"] ?? "../.."
        let url = URL(fileURLWithPath: "\(fixtureRoot)/\(path)")
        return (try? String(contentsOf: url, encoding: .utf8)) ?? ""
    }
}