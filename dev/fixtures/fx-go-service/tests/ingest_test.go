// Test del feature de ingesta de eventos.
//
// Los tests usan una DB SQLite en memoria con el driver
// mattn/go-sqlite3. Cada test crea su propio repositorio.
package tests

import (
	"context"
	"database/sql"
	"testing"
	"time"

	"fx-go-service/internal/domain"
	"fx-go-service/internal/repo/sqlite"
	"fx-go-service/internal/service"

	_ "github.com/mattn/go-sqlite3"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func setupDB(t *testing.T) (*sql.DB, domain.EventRepository) {
	t.Helper()
	db, err := sql.Open("sqlite3", ":memory:")
	require.NoError(t, err)
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS events (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		type TEXT NOT NULL,
		payload BLOB NOT NULL,
		created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
	)`)
	require.NoError(t, err)
	t.Cleanup(func() { db.Close() })
	return db, sqlite.NewSQLiteEventRepository(db)
}

func TestIngestEvent_with_valid_type_returns_no_error(t *testing.T) {
	_, repo := setupDB(t)
	svc := service.NewIngestService(repo)
	err := svc.Ingest(context.Background(), &domain.Event{
		Type:    "user.created",
		Payload: []byte(`{"id":1}`),
	})
	assert.NoError(t, err)
}

func TestIngestEvent_with_empty_type_returns_error(t *testing.T) {
	_, repo := setupDB(t)
	svc := service.NewIngestService(repo)
	err := svc.Ingest(context.Background(), &domain.Event{
		Type:    "",
		Payload: []byte(`{}`),
	})
	assert.Error(t, err)
}

func TestIngestEvent_with_two_events_list_returns_two(t *testing.T) {
	_, repo := setupDB(t)
	svc := service.NewIngestService(repo)
	ctx := context.Background()
	require.NoError(t, svc.Ingest(ctx, &domain.Event{Type: "x.y", Payload: []byte(`{}`)}))
	require.NoError(t, svc.Ingest(ctx, &domain.Event{Type: "x.y", Payload: []byte(`{}`)}))

	events, err := repo.ListByType(ctx, "x.y", 50, 0)
	require.NoError(t, err)
	assert.Len(t, events, 2)
}

func TestIngestEvent_count_by_type_returns_count(t *testing.T) {
	_, repo := setupDB(t)
	svc := service.NewIngestService(repo)
	ctx := context.Background()
	require.NoError(t, svc.Ingest(ctx, &domain.Event{Type: "a.b", Payload: []byte(`{}`)}))
	require.NoError(t, svc.Ingest(ctx, &domain.Event{Type: "a.b", Payload: []byte(`{}`)}))
	require.NoError(t, svc.Ingest(ctx, &domain.Event{Type: "a.b", Payload: []byte(`{}`)}))

	n, err := repo.CountByType(ctx, "a.b")
	require.NoError(t, err)
	assert.Equal(t, int64(3), n)
}

// Trampa P04: el init() del driver se ejecuta al importar.
// Verificar que un test que solo importa el package no causa side
// effects observables mas alla de la salida a stdout.
func TestIngestEvent_init_side_effects_documented(t *testing.T) {
	db, err := sql.Open("sqlite3", ":memory:")
	require.NoError(t, err)
	defer db.Close()
	_, err = db.Exec("SELECT 1")
	assert.NoError(t, err, "init() del driver debe haber registrado sqlite3")
}

var _ = time.Now // suprime warning
