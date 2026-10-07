import Testing
import Foundation

@Suite("ObjCBridge")
struct ObjCBridgeTests {

    @Test("header declares @interface and properties")
    func header_declares_interface() throws {
        let header = try String(
            contentsOf: TestPaths.objCBridgeDir.appendingPathComponent("LegacyLogger.h"),
            encoding: .utf8
        )
        #expect(header.contains("@interface LegacyLogger"))
        #expect(header.contains("@property"))
        #expect(header.contains("NS_ASSUME_NONNULL_BEGIN"))
    }

    @Test("implementation uses @dynamic and NSNotificationCenter")
    func implementation_uses_dynamic() throws {
        let impl = try String(
            contentsOf: TestPaths.objCBridgeDir.appendingPathComponent("LegacyLogger.m"),
            encoding: .utf8
        )
        #expect(impl.contains("@implementation LegacyLogger"))
        #expect(impl.contains("@dynamic lastMessage"))
        #expect(impl.contains("NSNotificationCenter"))
    }

    @Test("bridging header imports the logger")
    func bridging_header_imports_logger() throws {
        let bridging = try String(
            contentsOf: TestPaths.objCBridgeDir.appendingPathComponent("FxSwift-Bridging-Header.h"),
            encoding: .utf8
        )
        #expect(bridging.contains("#import \"LegacyLogger.h\""))
    }

    @Test("public API of LegacyLogger")
    func logger_public_api_surface() throws {
        let header = try String(
            contentsOf: TestPaths.objCBridgeDir.appendingPathComponent("LegacyLogger.h"),
            encoding: .utf8
        )
        #expect(header.contains("- (void)log:"))
        #expect(header.contains("- (void)clear"))
        #expect(header.contains("- (void)registerForNotifications"))
        #expect(header.contains("+ (instancetype)sharedLogger"))
    }
}
