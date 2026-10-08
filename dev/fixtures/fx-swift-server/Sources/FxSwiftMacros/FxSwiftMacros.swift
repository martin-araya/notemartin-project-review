// FxSwiftMacros.swift
// Libreria de macros Swift (SwiftSyntax) que el fixture expone al consumidor
// FxSwiftServer. Esta libreria es la unica fuente de codigo generado por
// macros en el repositorio; el codigo expandido vive en `.build/...` y la
// skill debe seguir el `@attached`/`@freestanding` hasta el expansion
// para entender el wiring real de las rutas (trampa E1 del ecosistema).
import SwiftCompilerPlugin
import SwiftSyntax
import SwiftSyntaxMacros

@main
struct FxSwiftMacros: CompilerPlugin {
    let providingMacros: [Macro.Type] = [
        RouteMacro.self,
        ImportModuleDeclMacro.self
    ]
}