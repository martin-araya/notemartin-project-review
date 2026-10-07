// Package main contiene el entry point de fx-go-service.
//
// Trampa E04: arranca el worker pool en background y monta el router
// chi para servir HTTP.
package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	"fx-go-service/internal/config"
	"fx-go-service/internal/http"
	"fx-go-service/internal/repo/sqlite"
	"fx-go-service/internal/service"
	"fx-go-service/internal/worker"

	_ "github.com/mattn/go-sqlite3"
)

func main() {
	cfg := config.Load()
	log.Printf("fx-go-service: db=%s port=%d workers=%d", cfg.DatabaseURL, cfg.HTTPPort, cfg.WorkerCount)

	db, err := sql.Open("sqlite3", cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("open db: %v", err)
	}
	defer db.Close()
	db.SetMaxOpenConns(1)

	// Trampa E02: blank import registra el driver. Aqui es
	// explicito; el init() del package mattn/go-sqlite3 corre al
	// importarse.
	_ = "github.com/mattn/go-sqlite3"

	// Trampa E01: implementacion estructural de las interfaces
	// del dominio sin keyword 'implements'.
	eventRepo := sqlite.NewSQLiteEventRepository(db)
	_ = sqlite.NewSQLiteExporter(eventRepo) // exporter se exporta por interfaz

	ingestSvc := service.NewIngestService(eventRepo)
	aggSvc := service.NewAggregateService(eventRepo)
	exportSvc, err := service.NewExportService(eventRepo)
	if err != nil {
		log.Fatalf("init export: %v", err)
	}

	pool := worker.NewPool(cfg.WorkerCount, ingestSvc)
	pool.Start()
	defer pool.Stop()

	app := http.NewApp(ingestSvc, aggSvc, exportSvc, pool)
	addr := fmt.Sprintf(":%d", cfg.HTTPPort)
	app.Server().Addr = addr

	// Trampa P02: el servidor no implementa graceful shutdown
	// (ListenAndServe bloquea hasta error).
	go func() {
		err := app.Server().ListenAndServe()
		if err != nil && err.Error() != "http: Server closed" {
			log.Fatalf("listen: %v", err)
		}
	}()
	log.Printf("listening on %s", addr)

	// Espera senal de terminacion.
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)
	<-stop

	// Graceful shutdown con timeout.
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := app.Server().Shutdown(ctx); err != nil {
		log.Printf("shutdown: %v", err)
	}
}
