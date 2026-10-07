import Testing
import Foundation
@testable import FxSwiftCore

@Suite("ExpensesRepository")
struct ExpensesRepositoryTests {

    private static func makeStore() throws -> (AppGroupStore, URL) {
        let url = URL(fileURLWithPath: NSTemporaryDirectory())
            .appendingPathComponent("fxswift-tests-\(UUID().uuidString)")
        try FileManager.default.createDirectory(
            at: url,
            withIntermediateDirectories: true
        )
        setenv(AppGroupPaths.overrideEnvVar, url.path, 1)
        return (AppGroupStore(), url)
    }

    private static func cleanup(_ url: URL) {
        try? FileManager.default.removeItem(at: url)
        unsetenv(AppGroupPaths.overrideEnvVar)
    }

    @Test("add then all returns the expense")
    func addThenAllReturnsExpense() async throws {
        let (store, url) = try Self.makeStore()
        defer { Self.cleanup(url) }
        let repository = ExpensesRepository(store: store)
        let expense = Expense.sample(amount: 12.5, note: "almuerzo")
        await repository.add(expense)
        let items = await repository.all()
        #expect(items.count == 1)
        #expect(items.first?.note == "almuerzo")
    }

    @Test("delete removes by id")
    func deleteRemovesById() async throws {
        let (store, url) = try Self.makeStore()
        defer { Self.cleanup(url) }
        let repository = ExpensesRepository(store: store)
        let id = UUID()
        await repository.add(Expense.sample(id: id, note: "k"))
        await repository.add(Expense.sample(note: "l"))
        await repository.delete(id: id)
        let items = await repository.all()
        #expect(items.count == 1)
        #expect(items.first?.id != id)
    }

    @Test("total sums amounts")
    func totalSumsAmounts() async throws {
        let (store, url) = try Self.makeStore()
        defer { Self.cleanup(url) }
        let repository = ExpensesRepository(store: store)
        await repository.add(Expense.sample(amount: 10))
        await repository.add(Expense.sample(amount: 20.5))
        let total = await repository.total()
        #expect(total == Decimal(30.5))
    }

    @Test("clear empties the store on disk")
    func clearEmptiesRepository() async throws {
        let (store, url) = try Self.makeStore()
        defer { Self.cleanup(url) }
        let repository = ExpensesRepository(store: store)
        await repository.add(Expense.sample())
        await repository.add(Expense.sample())
        await store.clear()
        let reloaded = await store.loadExpenses()
        #expect(reloaded.isEmpty)
        _ = repository
    }
}
