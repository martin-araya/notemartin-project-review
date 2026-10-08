// ImportModuleDeclMacro.swift
// Macro `@freestanding(declaration)` que se expande a `import <Module>`.
// Sirve para plantar la trampa P1: el `import` NO aparece en el AST literal
// del archivo que invoca el macro, solo en el codigo expandido en `.build`.
import SwiftSyntax
import SwiftSyntaxMacros

public enum ImportModuleDeclMacro: DeclarationMacro {
    public static func expansion(
        of node: some FreestandingMacroExpansionSyntax,
        in context: some MacroExpansionContext
    ) throws -> [DeclSyntax] {
        let moduleName = node.argumentList.first?.expression
            .as(StringLiteralExprSyntax.self)?.segments.first?.description ?? "Foundation"
        return [
            "import \(raw: moduleName)"
        ]
    }
}