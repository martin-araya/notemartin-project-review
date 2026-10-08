import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Ecosystem traps', () {
    test('E1 freezed part directives exist', () {
      final docFile = File('lib/features/reader/domain/document.dart');
      final content = docFile.readAsStringSync();
      expect(content.contains("part 'document.freezed.dart';"), isTrue);
      expect(content.contains("part 'document.g.dart';"), isTrue);
    });

    test('E2 riverpod ref.watch cross-provider', () {
      final favController = File(
        'lib/features/favorites/application/favorites_controller.dart',
      );
      final content = favController.readAsStringSync();
      expect(content.contains('ref.watch(readerControllerProvider)'), isTrue);
    });

    test('E3 platform channel strings + native stubs', () {
      final channel = File('lib/platform/native_method_channel.dart');
      final android = File('android_stub/MainActivity.kt');
      final ios = File('ios_stub/AppDelegate.swift');
      expect(channel.readAsStringSync().contains('scanDocument'), isTrue);
      expect(android.readAsStringSync().contains('scanDocument'), isTrue);
      expect(ios.readAsStringSync().contains('scanDocument'), isTrue);
    });

    test('E4 go_router redirect', () {
      final router = File('lib/router/app_router.dart');
      expect(router.readAsStringSync().contains('redirect:'), isTrue);
    });

    test('E5 dart-define enablePremium', () {
      final settings = File(
        'lib/features/settings/application/settings_controller.dart',
      );
      final src = settings.readAsStringSync();
      expect(src.contains('bool.fromEnvironment'), isTrue);
      expect(src.contains('FX_ENABLE_PREMIUM'), isTrue);
    });

    test('E6 adaptive widgets by platform', () {
      final widgets = File('lib/platform/platform_widget.dart');
      final src = widgets.readAsStringSync();
      expect(src.contains('TargetPlatform.iOS'), isTrue);
      expect(src.contains('CupertinoSwitch'), isTrue);
    });
  });
}