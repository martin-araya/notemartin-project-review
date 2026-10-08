package com.example.fxrn.nfc

import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.bridge.ReactContextBaseJavaModule
import com.facebook.react.bridge.ReactMethod
import com.facebook.react.bridge.Promise
import com.facebook.react.bridge.WritableMap
import com.facebook.react.bridge.Arguments
import com.facebook.react.module.annotations.ReactModule

/**
 * Trampa E1: modulo nativo que se resuelve por nombre `RtcNfcManager`
 * desde JS via `NativeModules.RtcNfcManager`. El nombre esta cableado
 * por string y debe coincidir entre Dart y nativo (E1).
 */
@ReactModule(name = "RtcNfcManager")
class NfcManagerModule(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {

    override fun getName(): String = "RtcNfcManager"

    @ReactMethod
    fun start(promise: Promise) {
        promise.resolve(null)
    }

    @ReactMethod
    fun stop(promise: Promise) {
        promise.resolve(null)
    }

    @ReactMethod
    fun readTag(promise: Promise) {
        val map: WritableMap = Arguments.createMap()
        map.putString("tagId", "android-fxrn-${System.currentTimeMillis()}")
        map.putString("type", "ISO14443A")
        promise.resolve(map)
    }

    @ReactMethod
    fun requestPermissions(promise: Promise) {
        promise.resolve("granted")
    }
}