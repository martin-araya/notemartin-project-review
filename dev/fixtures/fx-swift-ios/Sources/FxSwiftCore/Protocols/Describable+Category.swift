import Foundation

/// Conformancia especializada de `Describable` para `ExpenseCategory`.
///
/// Vive en un archivo separado del protocolo (trampa E3: implementacion
/// por defecto repartida entre varios archivos). Un agente que solo
/// lea `Describable.swift` pensara que la descripcion por defecto es
/// "—", pero la app real muestra el nombre legible de la categoria.
extension ExpenseCategory: Describable {
    public var description: String {
        switch self {
        case .food: "Comida"
        case .transport: "Transporte"
        case .housing: "Hogar"
        case .leisure: "Ocio"
        case .health: "Salud"
        case .other: "Otros"
        }
    }
}
