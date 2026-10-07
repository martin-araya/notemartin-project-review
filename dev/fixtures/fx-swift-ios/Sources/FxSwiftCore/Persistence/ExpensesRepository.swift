import Foundation

/// Repositorio de gastos. Es un `actor` para serializar las escrituras
/// entre la app principal y la extension de widget. La carga inicial se
/// hace en `init` con un `Task` separado para que el constructor no
/// bloquee; los tests usan `await loadIfNeeded()` para forzar la
/// sincronizacion.
public actor ExpensesRepository {
    private let store: AppGroupStore
    private var items: [Expense] = []
    private var didLoad = false

    public init(store: AppGroupStore = .shared) {
        self.store = store
    }

    public func loadIfNeeded() async {
        guard !didLoad else { return }
        items = await store.loadExpenses()
        didLoad = true
    }

    public func all() async -> [Expense] {
        await loadIfNeeded()
        return items
    }

    public func add(_ expense: Expense) async {
        await loadIfNeeded()
        items.append(expense)
        await store.saveExpenses(items)
    }

    public func delete(id: UUID) async {
        await loadIfNeeded()
        items.removeAll { $0.id == id }
        await store.saveExpenses(items)
    }

    public func total() async -> Decimal {
        await loadIfNeeded()
        return items.reduce(Decimal(0)) { $0 + $1.amount }
    }
}
