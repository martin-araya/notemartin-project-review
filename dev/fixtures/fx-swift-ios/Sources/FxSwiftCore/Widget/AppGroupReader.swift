import Foundation

/// Lector del App Group usado por la extension de widget. Es un
/// envoltorio sobre `AppGroupStore` para aislar la API que el widget
/// consume: solo lectura y `reload`. Mantener esta capa hace facil
/// mockear el widget en tests.
public struct AppGroupReader: Sendable {
    private let store: AppGroupStore

    public init(store: AppGroupStore = .shared) {
        self.store = store
    }

    public func currentSummary() async -> WidgetSummary {
        let expenses = await store.loadExpenses()
        let total = expenses.reduce(Decimal(0)) { $0 + $1.amount }
        let topCategory = Self.topCategoryName(in: expenses)
        return WidgetSummary(
            totalAmount: total,
            topCategory: topCategory,
            expenseCount: expenses.count,
            generatedAt: Date()
        )
    }

    private static func topCategoryName(in expenses: [Expense]) -> String {
        let counts = Dictionary(grouping: expenses, by: { $0.category })
        guard let top = counts.max(by: { $0.value.count < $1.value.count }) else {
            return "Otros"
        }
        return top.key.description
    }
}
