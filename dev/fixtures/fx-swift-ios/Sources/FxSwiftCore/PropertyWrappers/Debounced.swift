import Foundation

/// Property wrapper propio (trampa E1) que retrasa la escritura del valor
/// durante un intervalo. Aporta un setter `set(_:immediately:)` para
/// forzar la escritura cuando se necesita, p.ej. al cancelar un formulario.
///
/// El wrapper NO es `@MainActor` porque queremos que sea usable desde
/// `View.body` sin marcar la vista entera como aislada. La escritura
/// diferida usa un `DispatchSourceTimer` capturado por referencia.
@propertyWrapper
public final class Debounced<Value> {
    private let delay: TimeInterval
    private var pendingWorkItem: DispatchWorkItem?
    private var storedValue: Value

    public init(wrappedValue: Value, delay: TimeInterval = 0.3) {
        self.delay = delay
        self.storedValue = wrappedValue
    }

    public var wrappedValue: Value {
        get { storedValue }
        set { set(newValue) }
    }

    public func set(_ value: Value, immediately: Bool = false) {
        pendingWorkItem?.cancel()
        if immediately {
            storedValue = value
            return
        }
        let work = DispatchWorkItem { [weak self] in
            self?.storedValue = value
        }
        pendingWorkItem = work
        DispatchQueue.main.asyncAfter(deadline: .now() + delay, execute: work)
    }

    public func cancel() {
        pendingWorkItem?.cancel()
        pendingWorkItem = nil
    }
}
