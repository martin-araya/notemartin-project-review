// plugins/Routing.kt
// Extension function sobre Route que instala las 3 features
// como sub-routes. Trampa ecosistema #1: el DSL se reparte
// entre 3 archivos (InventarioRoutes, ReservasRoutes,
// AlertasRoutes), cada uno exponiendo una extension function
// sobre Route. La skill debe entender como el bloque
// `routing { routes() }` los une.
package com.example.fxktor.plugins

import com.example.fxktor.routes.alertas
import com.example.fxktor.routes.inventario
import com.example.fxktor.routes.reservas
import io.ktor.server.routing.Route

fun Route.routes() {
    inventario()
    reservas()
    alertas()
}
