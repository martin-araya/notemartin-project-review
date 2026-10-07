import Foundation

/// Constantes y resolucion de rutas del App Group compartido entre la app
/// y la extension de widget (trampa E6: el camino del contenedor no es
/// siempre el real; depende de si la entitlement esta firmada).
public enum AppGroupPaths {
    /// Identificador declarado en `*.entitlements` para el App Group.
    public static let groupIdentifier = "group.com.example.fxswift"

    /// Nombre del archivo JSON donde se serializan los gastos.
    public static let dataFileName = "data.json"

    /// Variable de entorno que el target widget usa para apuntar a un
    /// directorio de tests (los tests no pueden escribir en el App Group
    /// real porque no estan firmados con la entitlement).
    public static let overrideEnvVar = "FXSWIFT_APPGROUP_OVERRIDE"

    /// Resuelve el directorio donde se persistiran los datos compartidos.
    ///
    /// Prioridad:
    /// 1. Override por variable de entorno (tests + host SPM).
    /// 2. App Group real via `containerURL(forSecurityApplicationGroupIdentifier:)`.
    /// 3. Fallback a `NSTemporaryDirectory()/fxswift-appgroup` (unico path
    ///    siempre escribible, tambien usado por el host SPM).
    public static func appGroupContainerURL() -> URL {
        if let override = ProcessInfo.processInfo.environment[overrideEnvVar],
           !override.isEmpty {
            let url = URL(fileURLWithPath: override)
            try? FileManager.default.createDirectory(
                at: url,
                withIntermediateDirectories: true
            )
            return url
        }
        if let groupURL = FileManager.default.containerURL(
            forSecurityApplicationGroupIdentifier: groupIdentifier
        ) {
            return groupURL
        }
        let fallback = URL(fileURLWithPath: NSTemporaryDirectory())
            .appendingPathComponent("fxswift-appgroup", isDirectory: true)
        try? FileManager.default.createDirectory(
            at: fallback,
            withIntermediateDirectories: true
        )
        return fallback
    }

    /// Resuelve la URL completa del archivo de datos compartido.
    public static func dataFileURL() -> URL {
        appGroupContainerURL().appendingPathComponent(dataFileName)
    }
}
