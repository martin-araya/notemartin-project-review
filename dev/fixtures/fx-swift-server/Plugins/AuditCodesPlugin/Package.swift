// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "FxSwiftImporterPlugin",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .plugin(name: "AuditCodesPlugin", targets: ["AuditCodesPlugin"])
    ],
    targets: [
        .plugin(
            name: "AuditCodesPlugin",
            capability: .buildTool(),
            path: "Plugins"
        )
    ]
)