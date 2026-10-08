import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:fxdart/features/favorites/data/favorites_storage.dart';
import 'package:fxdart/features/favorites/domain/favorite.dart';

void main() {
  group('FavoritesStorage', () {
    setUp(() {
      SharedPreferences.setMockInitialValues({});
    });

    test('returns empty list when nothing stored', () async {
      final storage = FavoritesStorage();
      final result = await storage.load();
      expect(result, isEmpty);
    });

    test('saves and loads favorites', () async {
      final storage = FavoritesStorage();
      final favs = [
        Favorite(
          hash: 'fxd-1',
          title: 'Doc A',
          addedAt: DateTime(2026, 1, 1),
        ),
      ];
      await storage.save(favs);
      final loaded = await storage.load();
      expect(loaded.length, 1);
      expect(loaded.first.hash, 'fxd-1');
    });
  });
}