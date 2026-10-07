import Foundation

/// Actor que serializa el acceso al archivo compartido del App Group.
/// Tanto la app principal como la extension de widget lo usan para
/// leer/escribir el mismo `data.json`.
public actor AppGroupStore {
    public static let shared = AppGroupStore()

    private let fileURL: URL
    private let encoder: JSONEncoder
    private let decoder: JSONDecoder

    public init(fileURL: URL = AppGroupPaths.dataFileURL()) {
        self.fileURL = fileURL
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        self.encoder = encoder
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        self.decoder = decoder
    }

    public func loadExpenses() async -> [Expense] {
        guard let data = try? Data(contentsOf: fileURL) else {
            return []
        }
        return (try? decoder.decode([Expense].self, from: data)) ?? []
    }

    public func saveExpenses(_ expenses: [Expense]) async {
        // Trampa P4: el error se ignora silenciosamente porque el actor
        // no expone una API de errores y la app no puede hacer nada
        // util cuando el App Group no es escribible (p.ej. tests sin
        // entitlement). En produccion se deberia propagar a un canal
        // de observabilidad.
        guard let data = try? encoder.encode(expenses) else { return }
        try? data.write(to: fileURL, options: [.atomic])
    }

    public func append(_ expense: Expense) async {
        var current = await loadExpenses()
        current.append(expense)
        await saveExpenses(current)
    }

    public func clear() async {
        await saveExpenses([])
    }
}
