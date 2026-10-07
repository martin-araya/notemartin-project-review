import Foundation

/// Estado del flujo de bienvenida. Cada caso tiene un associated value
/// que el `NavigationStack` usa para `navigationDestination(for:)` (trampa
/// E2: el routing se hace por tipo y no por string).
public enum OnboardingState: Codable, Hashable, Sendable {
    case intro
    case permissions(askNotifications: Bool)
    case iCloud(available: Bool)
    case done(completedAt: Date)
}

public extension OnboardingState {
    /// Devuelve el siguiente paso en el flujo. La intencion es que la vista
    /// llame a esta funcion para empujar el `NavigationPath`. La logica
    /// centralizada en el modelo hace que un cambio de orden toque un
    /// unico punto.
    func next() -> OnboardingState? {
        switch self {
        case .intro:
            return .permissions(askNotifications: true)
        case .permissions:
            return .iCloud(available: true)
        case .iCloud:
            return .done(completedAt: Date())
        case .done:
            return nil
        }
    }
}
