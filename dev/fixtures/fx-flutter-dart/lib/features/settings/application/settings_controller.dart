import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Trampa E5: el flag `enablePremium` se evalua con `bool.fromEnvironment`.
/// En tiempo de build, `--dart-define=FX_ENABLE_PREMIUM=true` lo activa.
/// Sin el flag, defaultValue=false -> modo free.
const bool enablePremium =
    bool.fromEnvironment('FX_ENABLE_PREMIUM', defaultValue: false);

/// Trampa S2: constante declarada pero nunca usada en runtime.
const String _DEFAULT_LOCALE = 'en_US';

class SettingsState {
  const SettingsState({
    required this.premiumUnlocked,
    required this.locale,
  });

  final bool premiumUnlocked;
  final String locale;

  SettingsState copyWith({bool? premiumUnlocked, String? locale}) =>
      SettingsState(
        premiumUnlocked: premiumUnlocked ?? this.premiumUnlocked,
        locale: locale ?? this.locale,
      );
}

final settingsControllerProvider =
    NotifierProvider<SettingsController, SettingsState>(SettingsController.new);

class SettingsController extends Notifier<SettingsState> {
  @override
  SettingsState build() {
    // Trampa E5: combinamos el flag de build con SharedPreferences.
    // El orden de evaluacion importa: enablePremium se lee en build time,
    // pero `premiumUnlocked` se calcula en runtime. Si el precedence es
    // incorrecto, el resultado es inesperado.
    final isPremium =
        enablePremium || (stateOrNull?.premiumUnlocked ?? false);
    return SettingsState(
      premiumUnlocked: isPremium,
      locale: _DEFAULT_LOCALE,
    );
  }

  Future<void> togglePremium() async {
    final prefs = await SharedPreferences.getInstance();
    final current = prefs.getBool('premium') ?? enablePremium;
    await prefs.setBool('premium', !current);
    state = state.copyWith(premiumUnlocked: !current);
  }
}