import Foundation

/**
 * Trampa E1: modulo nativo Objective-C que se resuelve por nombre
 * `RtcNfcManager` desde JS via `NativeModules`. Compatible con el
 * bridge de React Native.
 */
@objc(RtcNfcManager)
class RtcNfcManager: NSObject {
  @objc func start(_ resolve: RCTPromiseResolveBlock, rejecter reject: RCTPromiseRejectBlock) {
    resolve(nil)
  }

  @objc func stop(_ resolve: RCTPromiseResolveBlock, rejecter reject: RCTPromiseRejectBlock) {
    resolve(nil)
  }

  @objc func readTag(_ resolve: RCTPromiseResolveBlock, rejecter reject: RCTPromiseRejectBlock) {
    let timestamp = Int(Date().timeIntervalSince1970 * 1000)
    let dict: [String: Any] = [
      "tagId": "ios-fxrn-\(timestamp)",
      "type": "ISO14443A"
    ]
    resolve(dict)
  }

  @objc func requestPermissions(_ resolve: RCTPromiseResolveBlock, rejecter reject: RCTPromiseRejectBlock) {
    resolve("granted")
  }

  @objc static func requiresMainQueueSetup() -> Bool {
    return false
  }
}