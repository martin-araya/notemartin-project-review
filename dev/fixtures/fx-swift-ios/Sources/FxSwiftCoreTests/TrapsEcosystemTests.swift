import Testing
import Foundation

@Suite("TrapsEcosystem")
struct TrapsEcosystemTests {

    private func read(_ relative: String) throws -> String {
        let url = TestPaths.coreRoot.appendingPathComponent(relative)
        return try String(contentsOf: url, encoding: .utf8)
    }

    @Test("E01: custom property wrapper")
    func e01_property_wrappers_presente() throws {
        let debounced = try read("PropertyWrappers/Debounced.swift")
        #expect(debounced.contains("@propertyWrapper"))
        #expect(debounced.contains("public final class Debounced"))
    }

    @Test("E02: navigationDestination(for:) routing")
    func e02_navigation_destination_presente() throws {
        let onboarding = try read("UI/OnboardingView.swift")
        #expect(onboarding.contains("NavigationStack"))
        #expect(onboarding.contains("navigationDestination(for: OnboardingState.self)"))
    }

    @Test("E03: protocol default implementation split across files")
    func e03_protocol_default_split_across_files() throws {
        let protocolFile = try read("Protocols/Describable.swift")
        let categoryFile = try read("Protocols/Describable+Category.swift")
        #expect(protocolFile.contains("extension Describable"))
        #expect(categoryFile.contains("extension ExpenseCategory: Describable"))
        #expect(categoryFile.contains("description"))
    }

    @Test("E04: @objc dynamic and KVO in Objective-C")
    func e04_objc_dynamic_y_kvo_presente() throws {
        let header = try read("ObjCBridge/LegacyLogger.h")
        let impl = try read("ObjCBridge/LegacyLogger.m")
        #expect(header.contains("@interface LegacyLogger"))
        #expect(impl.contains("@dynamic lastMessage"))
        #expect(impl.contains("NSNotificationCenter"))
        #expect(impl.contains("postNotificationName:LegacyLoggerDidLogNotification"))
    }

    @Test("E05: #if os(iOS) / #if DEBUG build flags")
    func e05_build_flags_presente() throws {
        let flags = try read("BuildFlags/BuildFlags.swift")
        #expect(flags.contains("#if os(iOS)"))
        #expect(flags.contains("#if DEBUG"))
        #expect(flags.contains("targetEnvironment(simulator)"))
    }

    @Test("E06: App Group container resolver")
    func e06_app_group_presente() throws {
        let paths = try read("AppGroup/AppGroupPaths.swift")
        #expect(paths.contains("group.com.example.fxswift"))
        #expect(paths.contains("containerURL(forSecurityApplicationGroupIdentifier:"))
    }
}
