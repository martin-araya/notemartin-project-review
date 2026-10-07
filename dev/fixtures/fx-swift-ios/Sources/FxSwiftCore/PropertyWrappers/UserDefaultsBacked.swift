import Foundation

/// Property wrapper que persiste su valor en `UserDefaults` con un nombre
/// de clave configurable. Equivalente a `@AppStorage` pero usable desde
/// tipos no-View (modelos, services, contexts de SwiftData).
///
/// Nota: la diferencia con `@AppStorage` es que este wrapper no esta
/// atado a una vista; el valor se lee y se escribe de forma sincrona.
/// Para bindings reactivos en SwiftUI se sigue recomendando `@AppStorage`.
@propertyWrapper
public final class UserDefaultsBacked<Value> {
    private let key: String
    private let defaultValue: Value
    private let store: UserDefaults
    private var storedValue: Value

    public init(
        wrappedValue defaultValue: Value,
        _ key: String,
        store: UserDefaults = .standard
    ) {
        self.key = key
        self.defaultValue = defaultValue
        self.store = store
        self.storedValue = store.object(forKey: key) as? Value ?? defaultValue
    }

    public var wrappedValue: Value {
        get { storedValue }
        set {
            storedValue = newValue
            store.set(newValue, forKey: key)
        }
    }

    public func reset() {
        wrappedValue = defaultValue
    }
}
