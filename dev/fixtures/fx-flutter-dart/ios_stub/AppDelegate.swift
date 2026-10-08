import Flutter
import UIKit

/**
 * Stubs Swift de los handlers del MethodChannel nativo.
 * Este archivo documenta el contrato que la skill debe leer como
 * evidencia textual; NO compila sin un proyecto iOS real (F06ad usa
 * platform channels solo via TestDefaultBinaryMessenger en tests).
 */
@objc public class AppDelegate: FlutterAppDelegate {
    private let CHANNEL = "com.example.fxdart/native"

    @objc public func scanDocument() -> [String: Any] {
        return [
            "hash": "fxs-\(Int(Date().timeIntervalSince1970 * 1000))",
            "title": "Documento Swift",
            "body": "Contenido capturado desde iOS nativo",
            "source": "ios-native"
        ]
    }

    @objc public func capturePage() -> String {
        return "ios-page-\(Int(Date().timeIntervalSince1970 * 1000))"
    }

    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        let controller = window?.rootViewController as! FlutterViewController
        let channel = FlutterMethodChannel(
            name: CHANNEL,
            binaryMessenger: controller.binaryMessenger
        )
        channel.setMethodCallHandler { (call, result) in
            switch call.method {
            case "scanDocument":
                result(self.scanDocument())
            case "capturePage":
                result(self.capturePage())
            default:
                result(FlutterMethodNotImplemented)
            }
        }
        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }
}