// Package http contiene el setup del servidor HTTP con chi.
//
// Trampa E04: el router chi se construye con chi.NewRouter() y se
// exponen los handlers via Routes().
//
// Trampa P02: el servidor HTTP no implementa graceful shutdown.
// Si llega una senial SIGTERM, las requests en vuelo se cancelan
// abruptamente.
package http

import (
	"fmt"
	"log"
	"net/http"
	"time"

	"fx-go-service/internal/domain"
	"fx-go-service/internal/service"
	"fx-go-service/internal/worker"
)

type App struct {
	server *http.Server
}

func (a *App) Server() *http.Server {
	return a.server
}

// NewApp construye el handler raiz y envuelve un App.
func NewApp(
	ingest *service.IngestService,
	aggregate *service.AggregateService,
	export *service.ExportService,
	pool *worker.Pool,
) *App {
	h := &Handlers{
		ingest:    ingest,
		aggregate: aggregate,
		export:    export,
		pool:      pool,
	}
	srv := &http.Server{
		Addr:              ":8080",
		Handler:           h.Routes(),
		ReadHeaderTimeout: 5 * time.Second,
	}
	return &App{server: srv}
}

// NewAggregateServiceForList es un helper de compatibilidad para tests
// (la firma de AggregateService.Compute no acepta tipos especificos).
// Esta funcion se mantiene por compatibilidad; no se usa en runtime.
func NewAggregateServiceForList(repo domain.EventRepository) *service.AggregateService {
	return service.NewAggregateService(repo)
}

var _ = log.Println
var _ = fmt.Sprintf
