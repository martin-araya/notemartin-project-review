import Foundation

/// Router de deep links declarados en `Info.plist` con URL scheme
/// `fxswift://` (trampa E6). Trampa P5: el `try?` que se usa al
/// parsear el path de la URL traga cualquier error de conversion y
/// el handler retorna como si nada hubiera pasado.
public struct DeepLinkRoute: Equatable, Sendable {
    public enum Destination: Equatable, Sendable {
        case onboarding
        case expenseDetail(id: UUID)
        case sync
        case unknown(host: String, path: String)
    }

    public let destination: Destination

    public init(destination: Destination) {
        self.destination = destination
    }

    public static func parse(_ url: URL) -> DeepLinkRoute? {
        guard url.scheme == "fxswift" else { return nil }
        let host = url.host ?? ""
        switch host {
        case "onboarding":
            return DeepLinkRoute(destination: .onboarding)
        case "sync":
            return DeepLinkRoute(destination: .sync)
        case "expense":
            // Trampa P5: el UUID puede no parsearse (URL malformada,
            // query vacia, etc.). `try?` se traga el error y devuelve
            // nil silenciosamente; el handler retorna como si la URL
            // no existiera.
            let raw = url.query?.replacingOccurrences(of: "id=", with: "") ?? ""
            if let uuid = try? UUID(uuidString: raw) {
                return DeepLinkRoute(destination: .expenseDetail(id: uuid))
            }
            return DeepLinkRoute(destination: .unknown(host: host, path: url.path))
        default:
            return DeepLinkRoute(destination: .unknown(host: host, path: url.path))
        }
    }
}

public enum DeepLinkRouter {
    /// Singleton accesible desde `onOpenURL { router.handle($0) }` en
    /// `AppMain`. Se mantiene como `struct` con un static para no
    /// arrastrar estado entre invocaciones.
    public static func handle(_ url: URL) -> DeepLinkRoute? {
        DeepLinkRoute.parse(url)
    }
}
