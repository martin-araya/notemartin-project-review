import Foundation
import Testing

/// Resuelve la ruta raiz del fixture de forma independiente del
/// sistema de archivos. `#filePath` apunta a este archivo
/// (`Sources/FxSwiftCoreTests/TestPaths.swift`); subiendo 3 niveles
/// llegamos a la raiz del fixture. Asi evitamos paths absolutos
/// hardcodeados que rompen CC-11.
enum TestPaths {
    static let fixtureRoot: URL = {
        let file = URL(fileURLWithPath: #filePath)
        return file
            .deletingLastPathComponent()  // FxSwiftCoreTests/
            .deletingLastPathComponent()  // Sources/
            .deletingLastPathComponent()  // <raiz del fixture>
    }()

    static let coreRoot: URL = fixtureRoot
        .appendingPathComponent("Sources")
        .appendingPathComponent("FxSwiftCore")

    static let objCBridgeDir: URL = coreRoot
        .appendingPathComponent("ObjCBridge")

    static let appDir: URL = fixtureRoot
        .appendingPathComponent("Examples")
        .appendingPathComponent("FxSwiftApp")
}
