import Foundation

/// Snapshot inmutable que la extension de widget muestra. Se reconstruye
/// a partir de los gastos leidos del App Group.
public struct WidgetSummary: Codable, Hashable, Sendable {
    public let totalAmount: Decimal
    public let topCategory: String
    public let expenseCount: Int
    public let generatedAt: Date

    public init(
        totalAmount: Decimal,
        topCategory: String,
        expenseCount: Int,
        generatedAt: Date
    ) {
        self.totalAmount = totalAmount
        self.topCategory = topCategory
        self.expenseCount = expenseCount
        self.generatedAt = generatedAt
    }

    public static let placeholder = WidgetSummary(
        totalAmount: 123.45,
        topCategory: "Comida",
        expenseCount: 7,
        generatedAt: Date()
    )
}

public struct WidgetSummaryEntry: Identifiable, Hashable, Sendable {
    public let id: UUID
    public var date: Date
    public let summary: WidgetSummary

    public init(date: Date, summary: WidgetSummary) {
        self.id = UUID()
        self.date = date
        self.summary = summary
    }
}

#if canImport(WidgetKit)
import WidgetKit
/// Conformacion condicional a `TimelineEntry` para que el target widget
/// pueda usar `WidgetSummaryEntry` directamente. Solo se compila cuando
/// WidgetKit esta disponible (iOS, macCatalyst, visionOS).
extension WidgetSummaryEntry: TimelineEntry {}
#endif
