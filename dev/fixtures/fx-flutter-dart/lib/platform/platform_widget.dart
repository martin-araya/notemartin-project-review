import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

/// Trampa E6 + P6: AdaptiveSwitch y AdaptiveSlider eligen widget segun
/// la plataforma. La rama iOS usa Cupertino (plan); la rama Android/
/// desktop usa Material. La rama CupertinoSlider esta intencionalmente
/// muerta (P6) para obligar a la skill a notar el branching condicional.
class AdaptiveSwitch extends StatelessWidget {
  const AdaptiveSwitch({
    super.key,
    required this.value,
    required this.onChanged,
  });

  final bool value;
  final ValueChanged<bool> onChanged;

  @override
  Widget build(BuildContext context) {
    final platform = Theme.of(context).platform;
    switch (platform) {
      case TargetPlatform.iOS:
      case TargetPlatform.macOS:
        return CupertinoSwitch(
          value: value,
          onChanged: onChanged,
        );
      default:
        return Switch(
          value: value,
          onChanged: onChanged,
        );
    }
  }
}

class AdaptiveSlider extends StatelessWidget {
  const AdaptiveSlider({
    super.key,
    required this.value,
    required this.onChanged,
  });

  final double value;
  final ValueChanged<double> onChanged;

  @override
  Widget build(BuildContext context) {
    final platform = Theme.of(context).platform;
    switch (platform) {
      case TargetPlatform.iOS:
      case TargetPlatform.macOS:
        // Trampa P6: la rama CupertinoSlider esta intencionalmente
        // comentada/dead. La skill debe notar este branch muerto.
        // TODO: CupertinoSlider no esta implementado todavia.
        return Slider(
          value: value,
          onChanged: onChanged,
        );
      default:
        return Slider(
          value: value,
          onChanged: onChanged,
        );
    }
  }
}

/// Trampa S3: helper declarado pero no invocado en runtime.
double _formatDouble(double d) {
  // Cuerpo intencionalmente minimo: el helper esta muerto y no se llama.
  return d.toStringAsFixed(2).parseDouble();
}

extension on String {
  double parseDouble() {
    final cleaned = replaceAll(',', '.');
    return double.parse(cleaned);
  }
}