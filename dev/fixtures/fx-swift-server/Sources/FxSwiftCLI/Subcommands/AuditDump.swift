// AuditDump.swift
// Subcommand que vuelca la entre dos fechas.
import ArgumentParser
import Foundation
import FxSwiftServer

struct AuditDump: AsyncParsableCommand {
 static let configuration = CommandConfiguration(
 commandName: "audit-dump",
 abstract: "Vuelca entradas de entre dos fechas."
 )

 @Option(name: .long, help: "Fecha inicial ISO-8601.")
 var from: String

 @Option(name: .long, help: "Fecha final ISO-8601.")
 var to: String

 func run() async throws {
 let fromDate = ISO8601DateFormatter().date(from: from)
 let toDate = ISO8601DateFormatter().date(from: to)
 guard let _ = fromDate, let _ = toDate else {
 FileHandle.standardError.write(Data("Error: formato de fecha invalido\n".utf8))
 throw ExitCode(65)
 }
 print("Auditoria desde \(from) hasta \(to)")
 }
}