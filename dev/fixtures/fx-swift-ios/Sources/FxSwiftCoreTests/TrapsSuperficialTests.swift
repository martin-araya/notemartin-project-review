import Testing
import Foundation

@Suite("TrapsSuperficial")
struct TrapsSuperficialTests {

    private func read(_ relative: String) throws -> String {
        let url = TestPaths.coreRoot.appendingPathComponent(relative)
        return try String(contentsOf: url, encoding: .utf8)
    }

    @Test("S01: setter in protocol default that ignores value")
    func s01_dead_helper() throws {
        let syncable = try read("Protocols/Syncable.swift")
        #expect(syncable.contains("set { _ = newValue }"))
    }

    @Test("S02: override env var only used by tests")
    func s02_dead_import() throws {
        let paths = try read("AppGroup/AppGroupPaths.swift")
        #expect(paths.contains("overrideEnvVar"))
    }

    @Test("S03: public init that is never called externally")
    func s03_unused_init() throws {
        let engine = try read("Sync/CloudKitSyncEngine.swift")
        #expect(engine.contains("public init() {}"))
    }
}
