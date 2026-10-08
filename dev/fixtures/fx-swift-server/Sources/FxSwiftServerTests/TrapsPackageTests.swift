// TrapsPackageTests.swift
// 6 tests que verifican que cada trampa del paquete P1..P6 esta plantada.
import XCTest
@testable import FxSwiftServer

final class TrapsPackageTests: XCTestCase {
    func testP1ImportMacro() {
        // P1: macro @ImportModuleDecl aplicado en App.swift.
        let appSource = readFixtureFile("Sources/FxSwiftServer/App.swift")
        XCTAssertTrue(appSource.contains("@ImportModuleDecl"))
    }

    func testP2UncheckedSendable() {
        // P2: LegacyNoteDTO es un class @unchecked Sendable.
        let dtoSource = readFixtureFile("Sources/FxSwiftServer/DTOs/LegacyNoteDTO.swift")
        XCTAssertTrue(dtoSource.contains("class"))
        XCTAssertTrue(dtoSource.contains("@unchecked Sendable"))
    }

    func testP3SilentTry() {
        // P3: AuditRecorder usa `try?` o `return false` en el catch.
        let recorderSource = readFixtureFile("Sources/FxSwiftServer/Services/AuditRecorder.swift")
        XCTAssertTrue(recorderSource.contains("catch"))
        XCTAssertTrue(recorderSource.contains("return false"))
    }

    func testP4PluginNoopFallback() {
        // P4: el plugin genera `#else // noop` cuando FoundationNetworking no esta.
        let pluginSource = readFixtureFile("Plugins/AuditCodesPlugin/Plugins/AuditCodesPlugin.swift")
        XCTAssertTrue(pluginSource.contains("noop"))
    }

    func testP5UniqueIndexNonIdempotent() {
        // P5: migracion con .unique(on:) sin IF NOT EXISTS.
        let migrationSource = readFixtureFile("Sources/FxSwiftServer/Migrations/CreateNote.swift")
        XCTAssertTrue(migrationSource.contains(".unique(on:"))
        XCTAssertFalse(migrationSource.contains("IF NOT EXISTS"))
    }

    func testP6CatchAllBeforeSpecific() {
        // P6: AuditRoutes registra catch-all "*" antes de rutas especificas.
        let auditSource = readFixtureFile("Sources/FxSwiftServer/Routes/AuditRoutes.swift")
        let catchAllRange = auditSource.range(of: "routes.get(\"*\"")
        let codesRange = auditSource.range(of: "routes.get(\"codes\"")
        XCTAssertNotNil(catchAllRange)
        XCTAssertNotNil(codesRange)
        XCTAssertLessThan(catchAllRange!.lowerBound, codesRange!.lowerBound)
    }

    private func readFixtureFile(_ path: String) -> String {
        let fixtureRoot = ProcessInfo.processInfo.environment["FIXTURE_ROOT"] ?? "../.."
        let url = URL(fileURLWithPath: "\(fixtureRoot)/\(path)")
        return (try? String(contentsOf: url, encoding: .utf8)) ?? ""
    }
}