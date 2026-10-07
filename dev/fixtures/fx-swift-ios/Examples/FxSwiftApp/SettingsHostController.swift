#if canImport(UIKit)
import UIKit
import FxSwiftCore

/// `UIViewController` real escrito en UIKit. Aqui se demuestra el
/// consumo del modulo Objective-C `LegacyLogger` via bridging header
/// (trampa E4). El controller deberia llamar a
/// `LegacyLogger.sharedLogger().registerForNotifications()` pero NO lo
/// hace: el observer nunca se registra.
@objc public final class SettingsHostController: UIViewController {

    private let logger = LegacyLogger.shared()
    private let darkModeSwitch = UISwitch()
    private let textSizeSlider = UISlider()

    public override func viewDidLoad() {
        super.viewDidLoad()
        title = "Ajustes (UIKit)"
        view.backgroundColor = .systemBackground

        darkModeSwitch.translatesAutoresizingMaskIntoConstraints = false
        darkModeSwitch.addTarget(self, action: #selector(darkModeChanged), for: .valueChanged)
        view.addSubview(darkModeSwitch)

        textSizeSlider.translatesAutoresizingMaskIntoConstraints = false
        textSizeSlider.minimumValue = 8
        textSizeSlider.maximumValue = 24
        textSizeSlider.value = 14
        textSizeSlider.addTarget(self, action: #selector(textSizeChanged), for: .valueChanged)
        view.addSubview(textSizeSlider)

        NSLayoutConstraint.activate([
            darkModeSwitch.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            darkModeSwitch.centerYAnchor.constraint(equalTo: view.centerYAnchor),
            textSizeSlider.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            textSizeSlider.topAnchor.constraint(equalTo: darkModeSwitch.bottomAnchor, constant: 24)
        ])

        // Trampa E4: el metodo `registerForNotifications` existe pero
        // nunca se invoca. Swift no recibira las notificaciones.
        // logger.registerForNotifications()
    }

    @objc private func darkModeChanged() {
        let message = "darkMode=\(darkModeSwitch.isOn ? "on" : "off")"
        logger.log(message)
    }

    @objc private func textSizeChanged() {
        let size = Int(textSizeSlider.value)
        logger.log("textSize=\(size)")
    }
}

/// Extiende el placeholder `LegacySettingsHost` declarado en
/// `FxSwiftCore/UI/LegacySettingsView.swift` para que apunte al
/// controller real con el bridging header aplicado. La logica de
/// `LegacySettingsView` (en FxSwiftCore) queda intacta: solo cambia
/// el tipo concreto del controller en runtime.
extension LegacySettingsHost {
    override public func viewDidLoad() {
        super.viewDidLoad()
        title = "Ajustes (UIKit)"
        view.backgroundColor = .systemBackground
        let logger = LegacyLogger.shared()
        let darkModeSwitch = UISwitch()
        darkModeSwitch.translatesAutoresizingMaskIntoConstraints = false
        darkModeSwitch.addTarget(self, action: #selector(forwardDarkModeChanged(_:)), for: .valueChanged)
        view.addSubview(darkModeSwitch)
        NSLayoutConstraint.activate([
            darkModeSwitch.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            darkModeSwitch.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])
        _ = logger
    }

    @objc private func forwardDarkModeChanged(_ sender: UISwitch) {
        // Trampa E4: el observer de KVO nunca se registra, asi que este
        // log aparece en la consola pero no llega a Swift.
        LegacyLogger.shared().log("darkMode=\(sender.isOn ? "on" : "off")")
    }
}
#else
import Foundation
/// Stub en host macOS: solo existe para que SwiftPM compile el target
/// cuando UIKit no esta disponible.
public final class SettingsHostController {
    public init() {}
}
#endif
