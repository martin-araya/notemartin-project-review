import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:fxdart/platform/native_method_channel.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('NativeMethodChannel', () {
    const channel = MethodChannel('com.example.fxdart/native');

    tearDown(() {
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
          .setMockMethodCallHandler(channel, null);
    });

    test('returns null when channel fails', () async {
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
          .setMockMethodCallHandler(channel, (call) async {
        throw PlatformException(code: 'NATIVE_FAIL', message: 'fail');
      });

      final ch = NativeMethodChannel();
      final result = await ch.invoke('scanDocument', null);
      expect(result, isNull);
    });

    test('returns value on success', () async {
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
          .setMockMethodCallHandler(channel, (call) async {
        return {'hash': 'fxd-1', 'title': 'Doc'};
      });

      final ch = NativeMethodChannel();
      final result = await ch.invoke('scanDocument', null);
      expect(result, isA<Map>());
    });
  });
}