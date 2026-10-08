// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "FxSwiftServer",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .library(name: "FxSwiftServer", targets: ["FxSwiftServer"]),
        .library(name: "FxSwiftMacros", targets: ["FxSwiftMacros"]),
        .executable(name: "fxsimport", targets: ["FxSwiftCLI"])
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", from: "4.92.0"),
        .package(url: "https://github.com/apple/swift-argument-parser.git", from: "1.3.0"),
        .package(url: "https://github.com/apple/swift-syntax.git", from: "510.0.0")
    ],
    targets: [
        // Plugin consumidor (build tool): genera Generated/AuditCodes.swift
        .executableTarget(
            name: "FxSwiftServer",
            dependencies: [
                "FxSwiftMacros",
                .product(name: "Vapor", package: "vapor"),
                .product(name: "Fluent", package: "vapor"),
                .product(name: "FluentSQLiteDriver", package: "vapor")
            ],
            path: "Sources/FxSwiftServer",
            exclude: ["Migrations/Migrations.ts"],
            plugins: [
                .plugin(name: "AuditCodesPlugin", package: "FxSwiftImporterPlugin")
            ]
        ),
        .target(
            name: "FxSwiftMacros",
            dependencies: [
                .product(name: "SwiftSyntax", package: "swift-syntax"),
                .product(name: "SwiftSyntaxMacros", package: "swift-syntax")
            ],
            path: "Sources/FxSwiftMacros"
        ),
        .executableTarget(
            name: "FxSwiftCLI",
            dependencies: [
                .product(name: "ArgumentParser", package: "swift-argument-parser")
            ],
            path: "Sources/FxSwiftCLI"
        ),
        .testTarget(
            name: "FxSwiftServerTests",
            dependencies: [
                "FxSwiftServer",
                .product(name: "Vapor", package: "vapor")
            ],
            path: "Sources/FxSwiftServerTests"
        )
    ]
)