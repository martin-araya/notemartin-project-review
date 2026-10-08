// CsvImporter.swift
// Actor `Sendable` con helper para parsear CSV.
import Foundation

actor CsvImporter {
    func parse(_ data: String) -> [[String]] {
        return data
            .split(separator: "\n")
            .map(String.init)
            .map { line in
                line.split(separator: ",", omittingEmptySubsequences: false)
                    .map(String.init)
            }
    }
}