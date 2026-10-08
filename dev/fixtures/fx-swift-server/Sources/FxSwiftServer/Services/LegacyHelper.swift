// LegacyHelper.swift
// Helper sin consumidores (trampa S1). Existe en el repositorio pero
// no se importa ni se llama desde ningun modulo.
import Foundation

enum LegacyHelper {
    static func formatLegacyDate(_ date: Date) -> String {
        let f = DateFormatter()
        f.dateFormat = "yyyy/MM/dd"
        return f.string(from: date)
    }
    static func slugLegacy(_ text: String) -> String {
        return text.lowercased().replacingOccurrences(of: " ", with: "-")
    }
}