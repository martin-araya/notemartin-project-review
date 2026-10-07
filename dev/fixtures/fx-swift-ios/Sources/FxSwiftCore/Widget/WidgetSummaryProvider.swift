import Foundation

/// Implementacion host-testable del `TimelineProvider` de WidgetKit.
/// En el target real (`FxSwiftWidget`) se conforma a
/// `TimelineProvider` importando `WidgetKit`; aqui exponemos solo la
/// funcion que produce entradas, para poder testearla en `swift test`
/// sin necesidad del framework de widgets.
public struct WidgetSummaryProvider: Sendable {
    private let reader: AppGroupReader
    private let now: @Sendable () -> Date

    public init(
        reader: AppGroupReader = AppGroupReader(),
        now: @escaping @Sendable () -> Date = { Date() }
    ) {
        self.reader = reader
        self.now = now
    }

    public func placeholder() -> WidgetSummaryEntry {
        WidgetSummaryEntry(date: now(), summary: .placeholder)
    }

    public func snapshot() async -> WidgetSummaryEntry {
        let summary = await reader.currentSummary()
        return WidgetSummaryEntry(date: now(), summary: summary)
    }

    public func timeline(limit: Int = 3) async -> [WidgetSummaryEntry] {
        var entries: [WidgetSummaryEntry] = []
        for offset in 0..<limit {
            let summary = await reader.currentSummary()
            let date = now().addingTimeInterval(Double(offset) * 600)
            entries.append(WidgetSummaryEntry(date: date, summary: summary))
        }
        return entries
    }
}
