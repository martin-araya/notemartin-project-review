// AuditRoutes.swift
// RouteCollection Vapor para `audit`. Demuestra trampa P6: el catch-all
// `*` se registra ANTES de las rutas especificas, por lo que un GET a
// `/audit/foo/bar/baz` matchea el wildcard y devuelve 200 en lugar de 404.
import Vapor
import FxSwiftServer

@FxRoute
struct AuditRoutes: RouteCollection {
    func boot(routes: RoutesBuilder) throws {
        // Trampa P6: catch-all registrado ANTES de las rutas especificas.
        routes.get("*", use: catchAll(_:))
        routes.post(use: create(_:))
        routes.get("codes", use: codes(_:))
    }

    func catchAll(_ req: Request) -> [String: Bool] {
        return ["matched": true]
    }

    func create(_ req: Request) async throws -> AuditEntry {
        struct Body: Content { var actor: String; var action: AuditAction; var targetId: String }
        let body = try req.content.decode(Body.self)
        guard !body.actor.isEmpty else { throw ApiError.titleRequired }
        let recorder = AuditRecorder(db: req.db)
        // P3: si record() devuelve false, el caller sigue adelante y devuelve 201.
        _ = await recorder.record(actor: body.actor, action: body.action, targetId: body.targetId)
        let entry = AuditEntry(actor: body.actor, action: body.action, targetId: body.targetId)
        try await entry.save(on: req.db)
        return entry
    }

    func codes(_ req: Request) async throws -> [String: [String]] {
        // P4: si el plugin no genero `AuditCode.all`, devolvemos un array vacio.
        return ["codes": AuditCode.allCases.map { $0.rawValue }]
    }
}