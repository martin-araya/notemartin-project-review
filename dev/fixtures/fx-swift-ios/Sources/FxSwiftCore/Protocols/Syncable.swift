import Foundation

/// Protocolo marcador para entidades sincronizables con iCloud. La
/// implementacion por defecto vive en este archivo para mostrar el
/// patron contrario a E3: el default esta en la declaracion del protocolo.
public protocol Syncable {
    var lastSyncedAt: Date? { get set }
    var isDirty: Bool { get set }
}

public extension Syncable {
    /// Default: la entidad nunca se ha sincronizado.
    var lastSyncedAt: Date? {
        get { nil }
        set { _ = newValue }
    }

    /// Default: la entidad se considera limpia hasta que alguien la marque.
    var isDirty: Bool {
        get { false }
        set { _ = newValue }
    }
}
