package com.example.fxandroid.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navDeepLink
import com.example.fxandroid.ui.history.HistoryScreen
import com.example.fxandroid.ui.premium.PremiumGateScreen
import com.example.fxandroid.ui.scan.ScanScreen

@Composable
fun FxNavGraph() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = Routes.SCAN) {

        composable(
            Routes.SCAN_WITH_EAN,
            deepLinks = listOf(
                navDeepLink { uriPattern = "fxandroid://scan/{ean}" }
            )
        ) { entry ->
            val ean = entry.arguments?.getString("ean")
            ScanScreen(prefilledEan = ean)
        }

        composable(
            Routes.HISTORY_WITH_FILTER,
            deepLinks = listOf(
                navDeepLink { uriPattern = "fxandroid://history/{filter}" }
            )
        ) { entry ->
            val filter = entry.arguments?.getString("filter")
            HistoryScreen(initialFilter = filter)
        }

        composable(
            Routes.PREMIUM,
            deepLinks = listOf(
                navDeepLink { uriPattern = "fxandroid://premium" }
            )
        ) {
            PremiumGateScreen()
        }
    }
}