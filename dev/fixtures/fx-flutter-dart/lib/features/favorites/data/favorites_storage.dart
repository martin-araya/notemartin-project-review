import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../domain/favorite.dart';

/// Wrapper de SharedPreferences para persistir la lista del feature.
class FavoritesStorage {
  static const String _kFavoritesKey = 'fxd_favorites_v1';

  Future<List<Favorite>> load() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getStringList(_kFavoritesKey) ?? const [];
    return raw
        .map((s) {
          try {
            return Favorite.fromJson(jsonDecode(s) as Map<String, dynamic>);
          } catch (_) {
            return null;
          }
        })
        .whereType<Favorite>()
        .toList();
  }

  Future<void> save(List<Favorite> favorites) async {
    final prefs = await SharedPreferences.getInstance();
    final raw = favorites.map((f) => jsonEncode(f.toJson())).toList();
    await prefs.setStringList(_kFavoritesKey, raw);
  }
}