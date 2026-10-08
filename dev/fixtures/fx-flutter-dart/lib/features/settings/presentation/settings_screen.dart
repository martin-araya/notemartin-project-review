import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../platform/platform_widget.dart';
import '../application/settings_controller.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(settingsControllerProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ajustes'),
      ),
      body: ListView(
        children: [
          ListTile(
            title: const Text('Modo premium'),
            subtitle: Text(state.premiumUnlocked ? 'Activado' : 'Desactivado'),
            trailing: AdaptiveSwitch(
              value: state.premiumUnlocked,
              onChanged: (_) =>
                  ref.read(settingsControllerProvider.notifier).togglePremium(),
            ),
          ),
          ListTile(
            title: const Text('Tamano de fuente'),
            subtitle: const Text('Ajustar tamano del texto'),
            trailing: SizedBox(
              width: 200,
              child: AdaptiveSlider(
                value: 0.5,
                onChanged: (v) {},
              ),
            ),
          ),
          const Divider(),
          ListTile(
            title: const Text('Acerca de'),
            subtitle: Text(
              'FxDart v0.1.0\nPlataforma: ${describeEnum(_platformKind())}',
            ),
          ),
        ],
      ),
    );
  }
}

PlatformKind _platformKind() {
  if (kIsWeb) return PlatformKind.web;
  if (defaultTargetPlatform == TargetPlatform.iOS) return PlatformKind.ios;
  if (defaultTargetPlatform == TargetPlatform.android) return PlatformKind.android;
  return PlatformKind.desktop;
}

enum PlatformKind { web, ios, android, desktop }