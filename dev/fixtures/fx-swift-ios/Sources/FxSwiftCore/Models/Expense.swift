import Foundation

/// Representa un gasto capturado por la app. Es un `Codable` para que
/// `AppGroupStore` pueda serializarlo a JSON dentro del contenedor App
/// Group. `Identifiable` + `Hashable` son requisitos del `List` + `ForEach`
/// de SwiftUI.
public struct Expense: Codable, Identifiable, Hashable, Sendable {
    public var id: UUID
    public var amount: Decimal
    public var category: ExpenseCategory
    public var note: String
    public var createdAt: Date

    public init(
        id: UUID = UUID(),
        amount: Decimal,
        category: ExpenseCategory,
        note: String = "",
        createdAt: Date = Date()
    ) {
        self.id = id
        self.amount = amount
        self.category = category
        self.note = note
        self.createdAt = createdAt
    }
}

public extension Expense {
    /// Atajo usado por las vistas y los tests para crear un gasto de prueba
    /// con un identificador estable. El `init` principal no obliga a fijar
    /// el `id` para no contaminar los call-sites de la UI.
    static func sample(
        id: UUID = UUID(),
        amount: Decimal = 9.99,
        category: ExpenseCategory = .food,
        note: String = "sample"
    ) -> Expense {
        Expense(id: id, amount: amount, category: category, note: note)
    }
}
