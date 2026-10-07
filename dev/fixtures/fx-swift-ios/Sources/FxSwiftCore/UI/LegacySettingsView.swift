import SwiftUI

#if canImport(UIKit)
import UIKit

/// Wrapper SwiftUI para el `UIViewController` UIKit heredado. Demuestra
/// la coexistencia SwiftUI + UIKit en una sola jerarquia. El tipo
/// `SettingsHostController` vive en el target `FxSwiftApp` (no en
/// `FxSwiftCore`) porque solo se puede compilar contra el bridging
/// header de Obj-C; para que `FxSwiftCore` siga siendo compilable en
/// host macOS, se referencia por nombre via un typealias cuando UIKit
/// esta disponible.
public struct LegacySettingsView: UIViewControllerRepresentable {
    public typealias UIViewControllerType = LegacySettingsHost

    public init() {}

    public func makeUIViewController(context: Context) -> LegacySettingsHost {
        LegacySettingsHost()
    }

    public func updateUIViewController(_ uiViewController: LegacySettingsHost, context: Context) {
        // No-op: el controlador UIKit mantiene su propio estado.
    }
}

/// Tipo vacio que sirve de placeholder cuando `FxSwiftCore` se compila
/// en un contexto que no tiene `SettingsHostController` (p.ej. los
/// tests de host). En el target iOS real, el archivo
/// `SettingsHostController.swift` aporta una extension `LegacySettingsHost`
/// que apunta al controller real con el `LegacyLogger` Obj-C.
public final class LegacySettingsHost: UIViewController {
    public override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground
    }
}
#else
/// En host macOS (donde UIKit no esta disponible) se renderiza un
/// placeholder SwiftUI para que el target SPM compile.
public struct LegacySettingsView: View {
    public init() {}
    public var body: some View {
        VStack(spacing: 8) {
            Image(systemName: "gearshape.2")
                .font(.system(size: 48))
            Text("UIKit legacy settings (only on iOS)")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding()
    }
}
#endif
