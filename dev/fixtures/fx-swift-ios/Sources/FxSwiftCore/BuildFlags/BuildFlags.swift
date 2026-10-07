import Foundation

/// Constantes que cambian segun plataforma, modo de compilacion y target.
/// Verifica la trampa E5: `#if os(iOS)`, `#if DEBUG` y
/// `#if targetEnvironment(simulator)` hacen que el codigo ejecutado por
/// la app en el dispositivo sea distinto del que corre en el simulador
/// o en macOS para tests.
public enum BuildFlags {
    public static let isDebug: Bool = {
        #if DEBUG
        return true
        #else
        return false
        #endif
    }()

    public static let platformName: String = {
        #if os(iOS)
        return "iOS"
        #elseif os(macOS)
        return "macOS"
        #elseif os(tvOS)
        return "tvOS"
        #elseif os(watchOS)
        return "watchOS"
        #else
        return "unknown"
        #endif
    }()

    public static let runsInSimulator: Bool = {
        #if targetEnvironment(simulator)
        return true
        #else
        return false
        #endif
    }()

    public static let apiBaseURL: URL = {
        #if DEBUG
        return URL(string: "http://localhost:8080/v1")!
        #else
        return URL(string: "https://api.example.com/v1")!
        #endif
    }()
}
