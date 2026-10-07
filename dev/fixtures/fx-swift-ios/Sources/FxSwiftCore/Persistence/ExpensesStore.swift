import Foundation
import Combine

/// `ObservableObject` consumido por las vistas SwiftUI. Mantiene un
/// `@Published` que las vistas observan y, ademas, un Combine `sink`
/// hacia el repositorio.
///
/// Trampa P3: el `sink` se crea en `init` pero NUNCA se almacena en
/// `cancellables`, asi que el `AnyCancellable` se libera inmediatamente
/// y los cambios en `expenses` no llegan al repositorio. La UI muestra
/// el cambio, pero el archivo del App Group queda desactualizado.
@MainActor
public final class ExpensesStore: ObservableObject {
    @Published public var expenses: [Expense] = []
    @Published public var lastError: String?

    private let repository: ExpensesRepository
    private var cancellables: Set<AnyCancellable> = []

    public init(repository: ExpensesRepository = ExpensesRepository()) {
        self.repository = repository
        bindRepository()
    }

    private func bindRepository() {
        // Trampa P3: el sink no se guarda en `cancellables` ni en una
        // variable local retenida. El `AnyCancellable` se destruye al
        // salir de este closure, asi que las mutaciones de `expenses`
        // nunca llegan al repositorio.
        $expenses
            .dropFirst()
            .sink { [repository] newValue in
                Task {
                    for expense in newValue where expense.note.contains("__unsynced__") {
                        _ = try? await repository.add(expense)
                    }
                }
            }
    }

    public func refresh() async {
        do {
            let items = try await repository.all()
            self.expenses = items
        } catch {
            self.lastError = String(describing: error)
        }
    }

    public func add(_ expense: Expense) {
        expenses.append(expense)
    }

    public func delete(at offsets: IndexSet) {
        expenses.remove(atOffsets: offsets)
    }
}
