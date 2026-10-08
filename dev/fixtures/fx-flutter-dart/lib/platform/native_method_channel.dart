import 'package:flutter/services.dart';

/// Wrapper sobre MethodChannel que ejecuta `invokeMethod` con un nombre
/// por string. El contrato es solo una convencion: la skill debe seguir
/// los strings hasta los stubs Kotlin/Swift.
///
/// Trampa P2: `try/catch (_)` traga cualquier error y devuelve `null`,
/// ocultando fallos del lado nativo.
class NativeMethodChannel {
  NativeMethodChannel({String channelName = 'com.example.fxdart/native'})
      : _channel = MethodChannel(channelName);

  final MethodChannel _channel;

  Future<dynamic> invoke(String method, [Object? arguments]) async {
    try {
      return await _channel.invokeMethod(method, arguments);
    } catch (_) {
      // Trampa P2: el error se silencia completamente. La skill debe
      // detectar este patron `catch (_)` sin log ni rethrow.
      return null;
    }
  }
}