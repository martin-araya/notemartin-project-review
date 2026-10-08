import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../application/reader_controller.dart';
import '../domain/document.dart';

class ReaderScreen extends ConsumerWidget {
  const ReaderScreen({super.key, this.initialHash});

  final String? initialHash;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(readerControllerProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Lector de documentos'),
      ),
      body: switch (state) {
        AsyncData(:final value) => _ReaderBody(doc: value, hash: initialHash),
        AsyncError(:final error) => Center(
            child: Text('Canal nativo no disponible: $error'),
          ),
        _ => const Center(child: Text('Cargando documento...')),
      },
      floatingActionButton: FloatingActionButton(
        onPressed: () => ref.read(readerControllerProvider.notifier).rescan(),
        child: const Icon(Icons.refresh),
      ),
    );
  }
}

class _ReaderBody extends StatelessWidget {
  const _ReaderBody({required this.doc, this.hash});

  final Document? doc;
  final String? hash;

  @override
  Widget build(BuildContext context) {
    if (doc == null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.document_scanner_outlined, size: 64),
            const SizedBox(height: 16),
            Text(hash != null
                ? 'Documento $hash no encontrado'
                : 'Toca el boton para escanear'),
          ],
        ),
      );
    }
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(doc!.title, style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 8),
          Text(doc!.body),
          const SizedBox(height: 16),
          Text('Hash: ${doc!.hash}', style: Theme.of(context).textTheme.bodySmall),
          const SizedBox(height: 4),
          Text('Origen: ${doc!.source}', style: Theme.of(context).textTheme.bodySmall),
        ],
      ),
    );
  }
}