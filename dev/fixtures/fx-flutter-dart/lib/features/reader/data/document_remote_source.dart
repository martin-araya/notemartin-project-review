import '../../platform/native_method_channel.dart';
import '../domain/document.dart';

/// Stub de fuente remota que envuelve el MethodChannel nativo.
/// La skill debe notar que NO hay base HTTP: la fuente solo delega
/// al canal nativo (Kotlin/Swift) con un nombre de metodo por string.
class DocumentRemoteSource {
  DocumentRemoteSource({NativeMethodChannel? channel})
      : _channel = channel ?? NativeMethodChannel();

  final NativeMethodChannel _channel;

  /// Invoca el canal nativo con el metodo 'scanDocument'.
  /// El resultado se mapea a un Document.
  Future<Document?> scanDocument() async {
    final result = await _channel.invoke('scanDocument', null);
    if (result == null) return null;
    if (result is! Map) return null;
    return Document(
      hash: result['hash'] as String,
      title: result['title'] as String? ?? 'Sin titulo',
      body: result['body'] as String? ?? '',
      scannedAt: DateTime.now(),
      source: result['source'] as String? ?? 'native',
    );
  }

  Future<String?> capturePage() async {
    final result = await _channel.invoke('capturePage', null);
    return result as String?;
  }
}