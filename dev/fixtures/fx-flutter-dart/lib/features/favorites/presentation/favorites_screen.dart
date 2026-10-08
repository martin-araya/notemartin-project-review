import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../application/favorites_controller.dart';
import '../domain/favorite.dart';

class FavoritesScreen extends ConsumerStatefulWidget {
  const FavoritesScreen({super.key, this.initialFilter});

  final String? initialFilter;

  @override
  ConsumerState<FavoritesScreen> createState() => _FavoritesScreenState();
}

class _FavoritesScreenState extends ConsumerState<FavoritesScreen> {
  final _searchController = TextEditingController();
  String? _activeFilter;

  @override
  void initState() {
    super.initState();
    _activeFilter = widget.initialFilter;
    if (_activeFilter != null) {
      _searchController.text = _activeFilter!;
    }
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(favoritesControllerProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Favoritos'),
      ),
      floatingActionButton: Padding(
        padding: const EdgeInsets.all(8),
        child: TextField(
          controller: _searchController,
          decoration: const InputDecoration(
            hintText: 'Buscar por titulo...',
            prefixIcon: Icon(Icons.search),
          ),
          onSubmitted: (value) async {
            if (value.isEmpty) return;
            final results = await ref
                .read(favoritesControllerProvider.notifier)
                .search(value);
            setState(() => _activeFilter = value);
            if (mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('${results.length} resultados')),
              );
            }
          },
        ),
      ),
      body: switch (state) {
        AsyncData(:final value) => _buildList(value),
        AsyncError(:final error) => Center(
            child: Text('No se pudieron cargar favoritos: $error'),
          ),
        _ => const Center(child: CircularProgressIndicator()),
      },
    );
  }

  Widget _buildList(List<Favorite> favorites) {
    if (favorites.isEmpty) {
      return const Center(
        child: Text('Aun no tienes favoritos'),
      );
    }
    return ListView.builder(
      itemCount: favorites.length,
      itemBuilder: (context, i) {
        final f = favorites[i];
        return ListTile(
          leading: const Icon(Icons.star),
          title: Text(f.title),
          subtitle: Text('Hash: ${f.hash}'),
          trailing: Text(f.addedAt.toIso8601String().substring(0, 10)),
        );
      },
    );
  }
}