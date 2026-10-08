// FxRoute.swift
// Re-exporta los macros publicos definidos en `FxSwiftMacros` para que
// el consumidor FxSwiftServer los importe desde un solo lugar.
@_exported import FxSwiftMacros

/// Atributo `@FxRoute` que produce un peer `registerRoute(_ app: Application)`
/// para un struct que ya declara `func boot(routes:)`. Su expansion vive
/// en `Sources/FxSwiftMacros/RouteMacro.swift` y NO aparece en `Sources/`.
@attached(peer, names: `ExternalModule`, conformances: `RegisterableRoute`)
public macro FxRoute() = #externalMacro(module: "FxSwiftMacros", type: "RouteMacro")

/// Macro freestanding que se expande a `import <module>` (trampa P1).
@freestanding(declaration, names: arbitrary)
public macro ImportModuleDecl(_ module: String) = #externalMacro(
    module: "FxSwiftMacros",
    type: "ImportModuleDeclMacro"
)