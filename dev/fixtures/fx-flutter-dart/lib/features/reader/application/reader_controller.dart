import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/document_remote_source.dart';
import '../domain/document.dart';

final documentRemoteSourceProvider =
    Provider<DocumentRemoteSource>((ref) => DocumentRemoteSource());

/// Trampa P1: AsyncNotifier sin try/catch.
/// El `build()` retorna el future sin manejar errores con `AsyncValue.error`.
/// Si el canal nativo falla, el provider queda en estado loading perpetuo.
final readerControllerProvider =
    AsyncNotifierProvider<ReaderController, Document?>(ReaderController.new);

class ReaderController extends AsyncNotifier<Document?> {
  @override
  Future<Document?> build() async {
    final remote = ref.read(documentRemoteSourceProvider);
    // Trampa P1: sin try/catch. El Future se expone tal cual.
    return await remote.scanDocument();
  }

  Future<void> rescan() async {
    state = const AsyncValue.loading();
    final remote = ref.read(documentRemoteSourceProvider);
    state = await AsyncValue.guard(() => remote.scanDocument());
  }
}