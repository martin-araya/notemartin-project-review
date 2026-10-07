// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "FxSwiftCore",
    platforms: [.macOS(.v13), .iOS(.v16)],
    products: [.library(name: "FxSwiftCore", targets: ["FxSwiftCore"])],
    targets: [
        .target(name: "FxSwiftCore", path: "Sources/FxSwiftCore", exclude: [
            "ObjCBridge/LegacyLogger.h", "ObjCBridge/LegacyLogger.m",
            "ObjCBridge/FxSwift-Bridging-Header.h"
        ]),
        .testTarget(name: "FxSwiftCoreTests", dependencies: ["FxSwiftCore"], path: "Sources/FxSwiftCoreTests")
    ]
)
