// UrlSessionProvider.swift
// Demuestra la trampa E6: `#if canImport(FoundationNetworking)` cambia
// el `URLSession` que se devuelve. En Linux devuelve `.default` con
// `timeoutIntervalForRequest = 0.001`; en macOS devuelve `.shared`.
// Ademas la rama `#else` tiene un import redundante (trampa S2).
import Foundation
#if canImport(FoundationNetworking)
import FoundationNetworking
#endif

enum UrlSessionProvider {
    static func makeSession(timeout: TimeInterval = 30.0) -> URLSession {
        #if canImport(FoundationNetworking)
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 0.001
        config.timeoutIntervalForResource = 60.0
        return URLSession(configuration: config)
        #else
        // macOS: import redundante no usado aqui (S2).
        _ = URLSession.self
        return URLSession.shared
        #endif
    }
}