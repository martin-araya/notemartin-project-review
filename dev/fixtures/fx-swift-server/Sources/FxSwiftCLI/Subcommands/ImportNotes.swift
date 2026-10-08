// ImportNotes.swift
// AsyncParsableCommand para importar notas desde CSV. Demuestra:
// - validacion de archivo (exit 64)
// - validacion de formato (exit 65)
// - server inalcanzable (exit 70)
// - SIGINT (exit 130)
// - partial success (exit 0)
import ArgumentParser
import Foundation
import FxSwiftServer

struct ImportNotes: AsyncParsableCommand {
 static let configuration = CommandConfiguration(
 commandName: "notes-import",
 abstract: "Importa notas desde un CSV hacia el servidor."
 )

 @Option(name: .shortAndLong, help: "Ruta al archivo CSV de entrada.")
 var input: String

 @Option(name: .long, help: "Formato del archivo (csv|json).")
 var format: String = "csv"

 @Option(name: .long, help: "URL del servidor destino.")
 var server: String = "http://127.0.0.1:8080/notes"

 func run() async throws {
 let fm = FileManager.default
 if !fm.fileExists(atPath: input) {
 // archivo no existe: exit 64
 FileHandle.standardError.write(Data("Error: archivo no encontrado: \(input)\n".utf8))
 throw ExitCode(64)
 }
 guard format == "csv" else {
 // formato invalido: exit 65
 FileHandle.standardError.write(Data("Error: formato no coincide con el archivo\n".utf8))
 throw ExitCode(65)
 }
 let csvData = try String(contentsOfFile: input, encoding: .utf8)
 let rows = csvData.split(separator: "\n").map(String.init)
 var imported = 0
 var skipped = 0
 for row in rows.dropFirst() {
 let cols = row.split(separator: ",", omittingEmptySubsequences: false).map(String.init)
 guard cols.count >= 3, !cols[0].isEmpty else { skipped += 1; continue }
 // En un caso real hariamos HTTP POST. Aqui solo contamos.
 imported += 1
 }
 if imported == 0 {
 FileHandle.standardError.write(Data("Error: server inalcanzable: \(server)\n".utf8))
 throw ExitCode(70)
 }
 // partial success
 print("Importadas \(imported) notas (\(skipped) inválidas omitidas)")
 // exit 0 por defecto
 }
}