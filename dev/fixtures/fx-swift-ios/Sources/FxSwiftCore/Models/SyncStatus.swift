import Foundation

/// Estado observable del sync con iCloud. `success(...)` y `failure(...)`
/// dejan un timestamp y un mensaje para que la UI pueda mostrarlo. El sync
/// engine reporta este estado via `SyncCoordinator`.
public enum SyncStatus: Codable, Hashable, Sendable {
    case idle
    case syncing(since: Date)
    case success(at: Date, count: Int)
    case failure(at: Date, message: String)

    public var isInProgress: Bool {
        if case .syncing = self { return true }
        return false
    }
}
