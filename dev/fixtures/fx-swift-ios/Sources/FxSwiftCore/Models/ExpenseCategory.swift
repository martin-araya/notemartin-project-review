import Foundation
import SwiftUI

/// Categorias de gasto. Conforman `Describable` con una implementacion
/// por defecto que se aporta desde `Describable+Category.swift` (trampa
/// E3: la implementacion por defecto del protocolo esta en un archivo
/// separado, lo que obliga a un rastreo multi-archivo para entender el
/// comportamiento de la categoria).
public enum ExpenseCategory: String, Codable, CaseIterable, Hashable, Sendable {
    case food
    case transport
    case housing
    case leisure
    case health
    case other
}

/// Color SwiftUI asociado a cada categoria. Vive aqui, no en la extension
/// de `Describable`, para mantenerlo cerca del modelo.
public extension ExpenseCategory {
    var tintColor: Color {
        switch self {
        case .food: .orange
        case .transport: .blue
        case .housing: .green
        case .leisure: .pink
        case .health: .red
        case .other: .gray
        }
    }
}
