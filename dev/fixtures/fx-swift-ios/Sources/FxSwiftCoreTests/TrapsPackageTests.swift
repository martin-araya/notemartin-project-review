import Testing
import Foundation

@Suite("TrapsPackage")
struct TrapsPackageTests {

    private func read(_ relative: String) throws -> String {
        let url = TestPaths.coreRoot.appendingPathComponent(relative)
        return try String(contentsOf: url, encoding: .utf8)
    }

    @Test("P01: sync engine swallows validation errors")
    func p01_sync_swallows_errors() throws {
        let engine = try read("Sync/CloudKitSyncEngine.swift")
        #expect(engine.contains("invalid amount"))
        #expect(engine.contains("skipped"))
        #expect(engine.contains("print(\"invalid"))
    }

    @Test("P02: widget timeline API exists")
    func p02_widget_timeline_ignores_errors() throws {
        let provider = try read("Widget/WidgetSummaryProvider.swift")
        #expect(provider.contains("timeline"))
    }

    @Test("P03: Combine sink without store(in:)")
    func p03_sink_sin_store_in() throws {
        let store = try read("Persistence/ExpensesStore.swift")
        #expect(store.contains(".sink"))
        #expect(store.contains("cancellables"))
        #expect(store.contains("Trampa P3"))
    }

    @Test("P04: AppGroup save swallows errors")
    func p04_appgroup_save_swallows_errors() throws {
        let store = try read("AppGroup/AppGroupStore.swift")
        #expect(store.contains("try? data.write"))
        #expect(store.contains("Trampa P4"))
    }

    @Test("P05: deep link UUID parse error swallowed")
    func p05_deeplink_swallows_uuid_error() throws {
        let router = try read("UI/DeepLinkRouter.swift")
        #expect(router.contains("try? UUID(uuidString:"))
        #expect(router.contains("Trampa P5"))
    }

    @Test("P06: ObjC registerForNotifications not called")
    func p6_objc_registerForNotifications_not_called() throws {
        let url = TestPaths.appDir.appendingPathComponent("SettingsHostController.swift")
        let controller = try String(contentsOf: url, encoding: .utf8)
        #expect(controller.contains("registerForNotifications"))
        #expect(controller.contains("// logger.registerForNotifications()"))
    }
}
