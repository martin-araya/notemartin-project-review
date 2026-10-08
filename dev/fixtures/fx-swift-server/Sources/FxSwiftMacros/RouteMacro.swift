// RouteMacro.swift
// Implementacion del macro `@FxRoute` (atributo `@attached(member, names: arbitrary)`)
// que genera automaticamente un metodo `registerRoute(_ app: Application)`
// para un struct que ya declara `boot(routes:)`. El codigo expandido vive
// en `.build/<target>/<...>.swift` y NO en el repositorio.
import SwiftSyntax
import SwiftSyntaxMacros

public enum RouteMacro: PeerMacro {
    public static func expansion(
        of node: AttributeSyntax,
        providingPeersOf declaration: some DeclSyntaxProtocol,
        in context: some MacroExpansionContext
    ) throws -> [DeclSyntax] {
        // Encontramos el struct al que se le aplica el atributo.
        guard let structDecl = declaration.as(StructDeclSyntax.self) else {
            return []
        }
        let structName = structDecl.name.text
        // Generamos una declaracion "peer": una extension que registra
        // todas las rutas del struct llamando a `boot(routes:)`.
        let peerSource: DeclSyntax = """
        extension \(raw: structName) {
            public func registerRoute(_ app: Application) {
                let router = APIRouter()
                self.boot(routes: router)
                app.routes.grouped(self.path).add(routes: router)
            }
            public var path: String { "/\(raw: structName.lowercased())" }
        }
        """
        return [peerSource]
    }
}