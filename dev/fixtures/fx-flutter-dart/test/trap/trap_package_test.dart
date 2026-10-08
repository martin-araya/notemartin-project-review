import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Package traps', () {
    test('P1 reader controller no try/catch in build', () {
      final controller = File(
        'lib/features/reader/application/reader_controller.dart',
      );
      final src = controller.readAsStringSync();
      expect(src.contains('AsyncNotifier'), isTrue);
      // build() no debe contener try/catch (P1)
      final buildIdx = src.indexOf('build()');
      final nextClassIdx = src.indexOf('class ReaderController');
      expect(buildIdx > 0, isTrue);
      // Confirmamos que entre build() y la siguiente declaracion
      // importante no haya un try/catch.
      final snippet = src.substring(buildIdx, src.length);
      expect(snippet.contains('try {'), isFalse,
          reason: 'build() should not wrap remote call in try');
    });

    test('P2 silent catch on method channel', () {
      final channel = File('lib/platform/native_method_channel.dart');
      final src = channel.readAsStringSync();
      expect(src.contains('catch (_)'), isTrue);
      expect(src.contains('return null;'), isTrue);
    });

    test('P3 router redirect ignores auth', () {
      final router = File('lib/router/app_router.dart');
      final src = router.readAsStringSync();
      expect(src.contains('redirect:'), isTrue);
      // No hay chequeo de auth
      expect(src.contains('auth'), isFalse);
    });

    test('P4 settings has dart-define + SharedPreferences', () {
      final settings = File(
        'lib/features/settings/application/settings_controller.dart',
      );
      final src = settings.readAsStringSync();
      expect(src.contains('enablePremium'), isTrue);
      expect(src.contains('SharedPreferences'), isTrue);
    });

    test('P5 freezed generates copyWith', () {
      // El package freezed genera copyWith en .freezed.dart; este test
      // verifica que el dominio lo declara.
      final docFile = File('lib/features/reader/domain/document.dart');
      final content = docFile.readAsStringSync();
      expect(content.contains('@freezed'), isTrue);
    });

    test('P6 Cupertino slider branch dead', () {
      final widgets = File('lib/platform/platform_widget.dart');
      final src = widgets.readAsStringSync();
      // La rama iOS de AdaptiveSlider usa Slider en lugar de CupertinoSlider
      expect(src.contains('TODO: CupertinoSlider'), isTrue);
    });
  });
}