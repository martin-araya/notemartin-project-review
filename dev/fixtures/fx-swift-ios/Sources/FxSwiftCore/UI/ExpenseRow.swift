import SwiftUI

/// Fila de la lista de gastos. Usa `@AppStorage` para mostrar la
/// preferencia de moneda (E1: property wrapper de SwiftUI). El
/// `tintColor` viene del modelo.
public struct ExpenseRow: View {
    @AppStorage("currency") private var currency: String = "EUR"
    let expense: Expense

    public init(expense: Expense) {
        self.expense = expense
    }

    public var body: some View {
        HStack(spacing: 12) {
            Image(systemName: iconName)
                .foregroundStyle(expense.category.tintColor)
                .frame(width: 28)
            VStack(alignment: .leading) {
                Text(expense.category.description)
                    .font(.headline)
                Text(expense.note.isEmpty ? "Sin nota" : expense.note)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            Spacer()
            Text(formattedAmount)
                .font(.body.monospacedDigit())
        }
    }

    private var formattedAmount: String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.currencyCode = currency
        return formatter.string(from: expense.amount as NSDecimalNumber) ?? "\(expense.amount)"
    }

    private var iconName: String {
        switch expense.category {
        case .food: "fork.knife"
        case .transport: "car.fill"
        case .housing: "house.fill"
        case .leisure: "gamecontroller.fill"
        case .health: "cross.case.fill"
        case .other: "questionmark.circle.fill"
        }
    }
}
