// main.swift
// Entrypoint de la CLI. swift-argument-parser con dos subcommands:
// `notes-import` y `audit-dump`.
import ArgumentParser
import FxSwiftServer

@main
struct FxsImport: AsyncParsableCommand {
 static let configuration = CommandConfiguration(
 commandName: "fxsimport",
 abstract: "Importa notas y vuelca (F06ab)",
 version: "0.1.0",
 subcommands: [
 ImportNotes.self,
 AuditDump.self
 ],
 defaultSubcommand: ImportNotes.self
 )
}