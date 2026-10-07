import WidgetKit
import SwiftUI
import FxSwiftCore

@main
struct FxSwiftWidgetBundle: WidgetBundle {
    var body: some Widget {
        FxSwiftWidget()
    }
}

struct FxSwiftWidget: Widget {
    let kind: String = "FxSwiftWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: FxSwiftTimelineProvider()) { entry in
            WidgetEntryView(entry: entry)
        }
        .configurationDisplayName("Resumen")
        .description("Muestra el total de gastos y la categoria mas frecuente.")
    }
}

/// Conformacion `TimelineProvider` especifica del widget iOS. Existe
/// solo en el target widget (no en el paquete SPM, donde WidgetKit
/// no esta disponible). Reusa el modelo `WidgetSummaryProvider` para
/// construir entradas sin duplicar la logica de negocio.
struct FxSwiftTimelineProvider: TimelineProvider {
    func placeholder(in context: Context) -> WidgetSummaryEntry {
        WidgetSummaryProvider().placeholder()
    }

    func getSnapshot(in context: Context, completion: @escaping (WidgetSummaryEntry) -> Void) {
        Task {
            let entry = await WidgetSummaryProvider().snapshot()
            completion(entry)
        }
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<WidgetSummaryEntry>) -> Void) {
        Task {
            let entries = await WidgetSummaryProvider().timeline(limit: 3)
            let timeline = Timeline(entries: entries, policy: .atEnd)
            completion(timeline)
        }
    }
}

struct WidgetEntryView: View {
    let entry: WidgetSummaryEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Total")
                .font(.caption)
                .foregroundStyle(.secondary)
            Text("\(entry.summary.totalAmount as NSDecimalNumber)")
                .font(.title2.bold())
            Text("Top: \(entry.summary.topCategory)")
                .font(.caption2)
                .foregroundStyle(.secondary)
            Text("Gastos: \(entry.summary.expenseCount)")
                .font(.caption2)
                .foregroundStyle(.secondary)
        }
        .padding()
    }
}
