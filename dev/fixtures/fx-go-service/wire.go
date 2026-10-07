//go:build wireinject
// +build wireinject

// Package main contiene los providers de wire para la inyeccion
// de dependencias compile-time de la aplicacion.
//
// Trampa E03: este archivo define los providers pero wire genera
// `wire_gen.go` con la implementacion concreta via `wire gen ./...`.
// La skill no debe buscar el codigo de DI en el repo; debe leer
// este archivo y ejecutar `wire` para regenerar `wire_gen.go`.
package main

import (
	"fx-go-service/internal/domain"
	"fx-go-service/internal/http"
	"fx-go-service/internal/repo/sqlite"
	"fx-go-service/internal/service"
	"fx-go-service/internal/worker"

	"github.com/google/wire"
)

func InitializeApp() (*http.App, func(), error) {
	wire.Build(
		sqlite.NewSQLiteEventRepository,
		sqlite.NewSQLiteExporter,
		wire.Bind(new(domain.EventRepository), new(*sqlite.SQLiteEventRepository)),
		wire.Bind(new(domain.Exporter), new(*sqlite.SQLiteExporter)),
		service.NewIngestService,
		service.NewAggregateService,
		service.NewExportService,
		worker.NewPool,
		http.NewApp,
	)
	return nil, nil, nil
}
