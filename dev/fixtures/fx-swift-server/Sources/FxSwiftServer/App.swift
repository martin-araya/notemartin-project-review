// App.swift
// Entrypoint de la app Vapor. Demuestra:
//  - P1: macro `@ImportModuleDecl("FoundationNetworking")` se expande
//    a un `import` que NO aparece en el AST literal del archivo.
//  - El macro `@FxRoute` aplicado a NotesRoutes/AuditRoutes genera
//    `registerRoute(_ app:)` en codigo expandido (E1).
import Foundation
import Vapor
import Fluent
import FluentSQLiteDriver
import FxSwiftServer

// Trampa P1: el `import FoundationNetworking` se inyecta solo en el codigo
// expandido por el macro `@ImportModuleDecl`. En el AST literal este import
// no existe; la skill debe seguir la expansion para verlo.
#if canImport(FoundationNetworking)
@ImportModuleDecl("FoundationNetworking")
#endif

@main
struct App {
    static func main() {
        let app = Application()
        do {
            try configure(app)
            try app.run()
        } catch {
            print("Fallo al arrancar: \(error)")
            exit(1)
        }
    }
}

// Conformidad dummy generada por `@FxRoute`. Sirve solo como pista de tipo
// para el compiler; el cuerpo real de `registerRoute` vive en el codigo
// expandido por `RouteMacro`.
protocol RegisterableRoute {}
extension NotesRoutes: RegisterableRoute {}
extension AuditRoutes: RegisterableRoute {}