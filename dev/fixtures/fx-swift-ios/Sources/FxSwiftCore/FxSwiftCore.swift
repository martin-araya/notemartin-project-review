import Foundation

/// Umbrella que expone un namespace `FxSwiftCore` con la version del
/// paquete y el prefijo de los tokens de verificacion. Existe para que
/// los call-sites externos puedan usar `FxSwiftCore.version` en vez de
/// importar cada submódulo.
public enum FxSwiftCore {
    public static let version: String = "0.1.0"
    public static let uniqueTokenPrefix: String = "NPRGT-FXSWIFT"
}
