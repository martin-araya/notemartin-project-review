import Foundation

/// Protocolo con implementacion por defecto. La intencion es que cualquier
/// tipo conforme reciba automaticamente una descripcion, sin obligar a
/// implementar el requisito. Ver `Describable+Category.swift` para
/// una implementacion especializada de `ExpenseCategory`.
public protocol Describable {
    var description: String { get }
}

public extension Describable {
    /// Default implementation. Si una conformance quiere sobreescribirla,
    /// debe hacerlo en su propia extension. Esta es la trampa E3: el
    /// comportamiento por defecto no esta donde se declara el protocolo.
    var description: String { "—" }
}
