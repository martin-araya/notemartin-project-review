import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../reader/application/reader_controller.dart';
import '../../reader/domain/document.dart';
import '../data/favorites_storage.dart';
import '../domain/favorite.dart';

final favoritesStorageProvider =
    Provider<FavoritesStorage>((ref) => FavoritesStorage());

/// Trampa E2: el provider observa `readerControllerProvider`.
/// El grafo de dependencias entre providers es implicito: la skill debe
/// detectar el `ref.watch` para entender que cambiar el reader recarga
/// los elementos.
final favoritesControllerProvider =
    AsyncNotifierProvider<FavoritesController, List<Favorite>>(
  FavoritesController.new,
);

class FavoritesController extends AsyncNotifier<List<Favorite>> {
  @override
  Future<List<Favorite>> build() async {
    // Trampa E2: dependencia implicita con readerControllerProvider.
    final _ = ref.watch(readerControllerProvider);
    final storage = ref.read(favoritesStorageProvider);
    return storage.load();
  }

  Future<void> addCurrentDocument(Document doc) async {
    final storage = ref.read(favoritesStorageProvider);
    final current = await future;
    final updated = [
      ...current,
      Favorite(
        hash: doc.hash,
        addedAt: DateTime.now(),
        title: doc.title,
      ),
    ];
    await storage.save(updated);
    state = AsyncValue.data(updated);
  }

  Future<List<Favorite>> search(String query) async {
    final storage = ref.read(favoritesStorageProvider);
    final all = await storage.load();
    final q = query.toLowerCase();
    return all.where((f) => f.title.toLowerCase().contains(q)).toList();
  }
}