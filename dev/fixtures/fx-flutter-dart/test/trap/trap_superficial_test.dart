import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Superficial traps', () {
    test('S1 Logger helper unused in lib/', () {
      final loggerSrc = File('lib/util/logger.dart').readAsStringSync();
      expect(loggerSrc.contains('class Logger'), isTrue);
      expect(loggerSrc.contains('static void print'), isTrue);

      // Buscar que no se llama Logger.print desde lib/
      for (final entity in Directory('lib').listSync(recursive: true)) {
        if (entity is! File) continue;
        if (!entity.path.endsWith('.dart')) continue;
        if (entity.path.endsWith('.g.dart')) continue;
        if (entity.path.endsWith('.freezed.dart')) continue;
        final content = entity.readAsStringSync();
        if (entity.path.contains('logger.dart')) continue;
        expect(content.contains('Logger.print'), isFalse,
            reason: 'Logger.print referenced in ${entity.path}');
      }
    });

    test('S2 _DEFAULT_LOCALE declared but never read', () {
      final settings = File(
        'lib/features/settings/application/settings_controller.dart',
      );
      final src = settings.readAsStringSync();
      expect(src.contains('_DEFAULT_LOCALE'), isTrue);
    });

    test('S3 _formatDouble helper in platform_widget dead', () {
      final widgets = File('lib/platform/platform_widget.dart');
      final src = widgets.readAsStringSync();
      expect(src.contains('_formatDouble'), isTrue);
      // _formatDouble no debe ser invocada
      expect(src.contains('_formatDouble('), isFalse);
    });
  });
}