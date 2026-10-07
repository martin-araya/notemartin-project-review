import Testing
import Foundation
@testable import FxSwiftCore

@Suite("WidgetSummary")
struct WidgetSummaryTests {

    private static func makeStore() throws -> (AppGroupStore, URL) {
        let url = URL(fileURLWithPath: NSTemporaryDirectory())
            .appendingPathComponent("fxswift-widget-\(UUID().uuidString)")
        try FileManager.default.createDirectory(
            at: url,
            withIntermediateDirectories: true
        )
        setenv(AppGroupPaths.overrideEnvVar, url.path, 1)
        return (AppGroupStore(), url)
    }

    private static func cleanup(_ url: URL) {
        try? FileManager.default.removeItem(at: url)
        unsetenv(AppGroupPaths.overrideEnvVar)
    }

    @Test("placeholder is stable")
    func placeholderIsStable() throws {
        let (store, url) = try Self.makeStore()
        defer { Self.cleanup(url) }
        let entry = WidgetSummaryProvider(reader: AppGroupReader(store: store)).placeholder()
        #expect(entry.summary.expenseCount == 7)
        #expect(entry.summary.topCategory == "Comida")
    }

    @Test("empty store produces empty summary")
    func emptyStoreProducesEmptySummary() async throws {
        let (store, url) = try Self.makeStore()
        defer { Self.cleanup(url) }
        let provider = WidgetSummaryProvider(reader: AppGroupReader(store: store))
        let entry = await provider.snapshot()
        #expect(entry.summary.expenseCount == 0)
        #expect(entry.summary.totalAmount == Decimal(0))
    }

    @Test("timeline produces the requested number of entries")
    func timelineProducesRequestedEntries() async throws {
        let (store, url) = try Self.makeStore()
        defer { Self.cleanup(url) }
        let provider = WidgetSummaryProvider(reader: AppGroupReader(store: store))
        let entries = await provider.timeline(limit: 3)
        #expect(entries.count == 3)
    }
}
