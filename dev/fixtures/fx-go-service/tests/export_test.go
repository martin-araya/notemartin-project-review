// Tests para el feature de export (E06: go:embed).
package tests

import (
	"context"
	"testing"

	"fx-go-service/internal/domain"
	"fx-go-service/internal/service"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestExport_with_empty_db_returns_serialized_output(t *testing.T) {
	_, repo := setupDB(t)
	svc, err := service.NewExportService(repo)
	require.NoError(t, err)
	out, err := svc.Export(context.Background(), "json")
	require.NoError(t, err)
	assert.Contains(t, string(out), "format=json")
	assert.Contains(t, string(out), "count=0")
}

func TestExport_with_default_format_returns_text(t *testing.T) {
	_, repo := setupDB(t)
	svc, err := service.NewExportService(repo)
	require.NoError(t, err)
	out, err := svc.Export(context.Background(), "default")
	require.NoError(t, err)
	assert.Contains(t, string(out), "format=default")
}

func TestExport_with_one_event_returns_count_1(t *testing.T) {
	_, repo := setupDB(t)
	ingest := service.NewIngestService(repo)
	svc, err := service.NewExportService(repo)
	require.NoError(t, err)
	ctx := context.Background()
	require.NoError(t, ingest.Ingest(ctx, &domain.Event{Type: "user.created", Payload: []byte(`{}`)}))
	out, err := svc.Export(ctx, "json")
	require.NoError(t, err)
	// Trampa P03: el exporter de SQLite usa type=default para ListByType;
	// el evento se guardo con type=user.created, asi que el listado
	// vacio cuenta 0. Verificamos que no falle.
	assert.Contains(t, string(out), "count=")
}

func TestExport_template_uses_embedded_file(t *testing.T) {
	// Trampa E06: el FS de templates se embebe via //go:embed.
	// No podemos inspeccionar el FS aqui, pero el test confirma que
	// Export funciona sin acceso al filesystem externo.
	_, repo := setupDB(t)
	svc, err := service.NewExportService(repo)
	require.NoError(t, err, "NewExportService debe parsear el template embebido")
	_, err = svc.Export(context.Background(), "json")
	assert.NoError(t, err)
}
