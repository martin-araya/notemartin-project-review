import SwiftUI

/// Vista de lista de gastos. Demuestra `@StateObject` + `@Published` con
/// la trampa P3: el `sink` de Combine en `ExpensesStore` se destruye al
/// terminar el closure de `init`, asi que las mutaciones de `expenses`
/// no se persisten en el App Group.
public struct ExpenseListView: View {
    @StateObject private var store = ExpensesStore()
    @State private var newAmount: String = ""

    public init() {}

    public var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                List {
                    ForEach(store.expenses) { expense in
                        ExpenseRow(expense: expense)
                    }
                    .onDelete(perform: store.delete)
                }
                inputBar
            }
            .navigationTitle("Gastos")
            .task { await store.refresh() }
        }
    }

    private var inputBar: some View {
        HStack {
            inputField
            Button("Anadir") {
                guard let value = Decimal(string: newAmount) else { return }
                let expense = Expense(amount: value, category: .food, note: "")
                store.add(expense)
                newAmount = ""
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }

    @ViewBuilder
    private var inputField: some View {
        #if os(iOS)
        TextField("Importe", text: $newAmount)
            .keyboardType(.decimalPad)
            .textFieldStyle(.roundedBorder)
        #else
        TextField("Importe", text: $newAmount)
            .textFieldStyle(.roundedBorder)
        #endif
    }
}
