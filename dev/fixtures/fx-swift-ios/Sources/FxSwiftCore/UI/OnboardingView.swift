import SwiftUI

/// Pantalla de bienvenida de 4 pasos. Demuestra la trampa E2:
/// `NavigationStack` + `navigationDestination(for:)` enruta por tipo,
/// no por string. La pila vive en `@State path` y la mutamos llamando
/// `OnboardingState.next()` sobre el caso actual.
public struct OnboardingView: View {
    @State private var path: [OnboardingState] = [.intro]
    @State private var askNotifications: Bool = true

    public init() {}

    public var body: some View {
        NavigationStack(path: $path) {
            introStep
                .navigationDestination(for: OnboardingState.self) { state in
                    switch state {
                    case .intro:
                        introStep
                    case .permissions(let ask):
                        permissionsStep(askNotifications: ask)
                    case .iCloud(let available):
                        iCloudStep(available: available)
                    case .done(let completedAt):
                        doneStep(completedAt: completedAt)
                    }
                }
        }
    }

    private var introStep: some View {
        VStack(spacing: 24) {
            Image(systemName: "sparkles")
                .font(.system(size: 64))
                .foregroundStyle(.tint)
            Text("Bienvenido")
                .font(.largeTitle.bold())
            Text("Registra tus gastos y sincroniza con iCloud.")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)
            Button("Empezar") {
                path.append(.permissions(askNotifications: askNotifications))
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }

    private func permissionsStep(askNotifications: Bool) -> some View {
        VStack(spacing: 16) {
            Text("Permisos")
                .font(.title2.bold())
            Toggle("Recibir avisos", isOn: .constant(askNotifications))
                .disabled(true)
            Button("Continuar") {
                path.append(.iCloud(available: true))
            }
            .buttonStyle(.bordered)
        }
        .padding()
    }

    private func iCloudStep(available: Bool) -> some View {
        VStack(spacing: 16) {
            Text("iCloud")
                .font(.title2.bold())
            HStack {
                Image(systemName: available ? "checkmark.circle.fill" : "xmark.octagon.fill")
                    .foregroundStyle(available ? .green : .red)
                Text(available ? "iCloud disponible" : "iCloud no disponible")
            }
            Button("Finalizar") {
                path.append(.done(completedAt: Date()))
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }

    private func doneStep(completedAt: Date) -> some View {
        VStack(spacing: 16) {
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 64))
                .foregroundStyle(.green)
            Text("Listo")
                .font(.largeTitle.bold())
            Text("Onboarding completado el \(completedAt.formatted(date: .abbreviated, time: .shortened))")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)
        }
        .padding()
    }
}
