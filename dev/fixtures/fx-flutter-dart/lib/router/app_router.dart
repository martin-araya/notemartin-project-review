import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../features/favorites/presentation/favorites_screen.dart';
import '../features/reader/presentation/reader_screen.dart';
import '../features/settings/presentation/settings_screen.dart';
import 'routes.dart';

final GoRouter appRouter = GoRouter(
  initialLocation: Routes.reader,
  // Trampa P3: el redirect ignora auth y siempre permite acceso.
  // No hay chequeo de autenticacion, por lo que un deep link invalido
  // redirige al reader sin validar identidad.
  redirect: (BuildContext context, GoRouterState state) {
    return state.matchedLocation == '/' ? Routes.reader : null;
  },
  routes: [
    GoRoute(
      path: Routes.reader,
      builder: (context, state) => const ReaderScreen(),
    ),
    GoRoute(
      path: Routes.readerWithDoc,
      builder: (context, state) {
        final hash = state.pathParameters['hash'];
        return ReaderScreen(initialHash: hash);
      },
    ),
    GoRoute(
      path: Routes.favorites,
      builder: (context, state) => const FavoritesScreen(),
    ),
    GoRoute(
      path: Routes.favoritesWithFilter,
      builder: (context, state) {
        final filter = state.pathParameters['filter'];
        return FavoritesScreen(initialFilter: filter);
      },
    ),
    GoRoute(
      path: Routes.settings,
      builder: (context, state) => const SettingsScreen(),
    ),
  ],
);