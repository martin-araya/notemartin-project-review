import Foundation

/// Wrapper de `CloudKitSyncEngine` que traduce el resultado a `SyncStatus`
/// para que las vistas lo observen. Se inyecta como `@StateObject` en la
/// vista de configuracion.
@MainActor
public final class SyncCoordinator: ObservableObject {
    @Published public private(set) var status: SyncStatus = .idle

    private let engine: CloudKitSyncEngine

    public init(engine: CloudKitSyncEngine = CloudKitSyncEngine()) {
        self.engine = engine
    }

    public func sync(_ expenses: [Expense]) async {
        status = .syncing(since: Date())
        do {
            let result = try await engine.sync(expenses)
            status = .success(at: result.at, count: result.uploaded)
        } catch {
            status = .failure(at: Date(), message: String(describing: error))
        }
    }

    public func reset() {
        status = .idle
    }
}
