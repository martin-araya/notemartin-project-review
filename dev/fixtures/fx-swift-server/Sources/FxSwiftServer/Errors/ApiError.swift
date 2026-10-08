// ApiError.swift
// Errores de dominio mapeados a respuestas HTTP via AbortError.
import Vapor

enum ApiError: AbortError, Sendable, Error {
    case titleRequired
    case bodyTooLong
    case notFound(UUID)
    case conflict(UUID)
    case timeout
    case dbUnavailable
    case auditFailed
    var status: HTTPResponseStatus {
        switch self {
        case .titleRequired, .bodyTooLong: return .badRequest
        case .notFound: return .notFound
        case .conflict: return .conflict
        case .timeout: return .gatewayTimeout
        case .dbUnavailable, .auditFailed: return .internalServerError
        }
    }
    var reason: String {
        switch self {
        case .titleRequired: return "title is required"
        case .bodyTooLong: return "body too long"
        case .notFound(let id): return "no encontrado: \(id)"
        case .conflict(let id): return "conflicto: \(id)"
        case .timeout: return "timeout"
        case .dbUnavailable: return "db unavailable"
        case .auditFailed: return "audit failed"
        }
    }
}