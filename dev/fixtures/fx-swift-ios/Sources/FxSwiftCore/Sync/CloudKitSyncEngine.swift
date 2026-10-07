import Foundation

/// Motor de sincronizacion con iCloud. En produccion hablaria con
/// CloudKit (`CKContainer`, `CKDatabase`, `CKRecord`); aqui se simula
/// la operacion con un `Task.sleep` para no depender de red ni de
/// credenciales.
///
/// Trampa P1: los errores de validacion (p.ej. `amount <= 0`) se
/// reportan con `print` y se devuelven como `ok` silenciosamente. La UI
/// muestra el sync como exitoso aunque la entrada no se haya subido.
public actor CloudKitSyncEngine {
    public enum SyncError: Error, Equatable {
        case invalidAmount(UUID)
        case emptyBatch
    }

    private var lastSyncedAt: Date?

    public init() {}

    public func sync(_ expenses: [Expense]) async throws -> SyncResult {
        guard !expenses.isEmpty else {
            throw SyncError.emptyBatch
        }
        for expense in expenses {
            try await Task.sleep(nanoseconds: 5_000_000) // 5 ms
            if expense.amount <= 0 {
                // Trampa P1: el error se loggea pero NO se propaga.
                print("invalid amount for \(expense.id); skipped")
                continue
            }
        }
        lastSyncedAt = Date()
        return SyncResult(
            uploaded: expenses.count,
            skipped: expenses.count(where: { $0.amount <= 0 }),
            at: lastSyncedAt ?? Date()
        )
    }

    public func lastSync() -> Date? {
        lastSyncedAt
    }
}

public struct SyncResult: Equatable, Sendable {
    public let uploaded: Int
    public let skipped: Int
    public let at: Date

    public init(uploaded: Int, skipped: Int, at: Date) {
        self.uploaded = uploaded
        self.skipped = skipped
        self.at = at
    }
}
