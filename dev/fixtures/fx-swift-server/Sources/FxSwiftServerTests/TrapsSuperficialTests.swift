// TrapsSuperficialTests.swift
// 3 tests para trampas superficiales S1..S3.
import XCTest
@testable import FxSwiftServer

final class TrapsSuperficialTests: XCTestCase {
    func testS1LegacyHelperUnused() {
        // S1: LegacyHelper existe pero no se importa desde ningun archivo del fixture.
        let helperSource = readFixtureFile("Sources/FxSwiftServer/Services/LegacyHelper.swift")
        XCTAssertTrue(helperSource.contains("LegacyHelper"))
        // Buscar referencias a LegacyHelper en el resto del fixture: no debe haberlas.
        var found = false
        let others = [
            "Sources/FxSwiftServer/App.swift",
            "Sources/FxSwiftServer/Configure.swift",
            "Sources/FxSwiftServer/Routes/NotesRoutes.swift",
            "Sources/FxSwiftServer/Routes/AuditRoutes.swift"
        ]
        for path in others {
            let s = readFixtureFile(path)
            if s.contains("LegacyHelper") { found = true }
        }
        XCTAssertFalse(found, "LegacyHelper no debe usarse en codigo de runtime")
    }

    func testS2UnusedImportInElse() {
        // S2: rama #else tiene un import redundante.
        let urlSource = readFixtureFile("Sources/FxSwiftServer/Services/UrlSessionProvider.swift")
        // En la rama #else hay `_ = URLSession.self` y un import no usado en la rama superior.
        XCTAssertTrue(urlSource.contains("#else"))
        XCTAssertTrue(urlSource.contains("_ = URLSession.self"))
    }

    func testS3LegacyModeEnvUnused() {
        // S3: variable `legacyMode` leida de Environment pero nunca usada.
        let configureSource = readFixtureFile("Sources/FxSwiftServer/Configure.swift")
        XCTAssertTrue(configureSource.contains("LEGACY_MODE"))
        XCTAssertTrue(configureSource.contains("let legacyMode"))
        XCTAssertTrue(configureSource.contains("_ = legacyMode"))
    }

    private func readFixtureFile(_ path: String) -> String {
        let fixtureRoot = ProcessInfo.processInfo.environment["FIXTURE_ROOT"] ?? "../.."
        let url = URL(fileURLWithPath: "\(fixtureRoot)/\(path)")
        return (try? String(contentsOf: url, encoding: .utf8)) ?? ""
    }
}